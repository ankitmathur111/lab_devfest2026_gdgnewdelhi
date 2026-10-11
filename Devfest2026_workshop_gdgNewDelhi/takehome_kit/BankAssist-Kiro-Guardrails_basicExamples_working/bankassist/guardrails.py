"""BankAssist — AI Guardrails Practice Lab

EDUCATIONAL & ETHICAL USE ONLY
This is a simplified practice application for training and demonstration.
It is not a production banking application or security framework.
Use synthetic data only and test only in environments you are authorized to use.
Further security, architecture, compliance, privacy, and engineering validation
is required before adapting any pattern for real-world use.
"""

import re
from .models import PolicyDecision, ToolCall
from .tools import TOOL_RISK
from .authorization import authorize

POLICY_VERSION = "1.0"

PROMPT_INJECTION_PATTERNS = [
    r"ignore (all )?(previous|prior) instructions",
    r"reveal (your )?(system prompt|hidden instructions)",
    r"bypass (your )?security",
    r"disable (your )?guardrails",
]

SENSITIVE_PATTERNS = [
    r"\botp\b",
    r"\bone[- ]time password\b",
    r"\b(?:\d[ -]?){13,19}\b",  # simple card-like number detector
    r"\bpassword\b",
    r"\bpin\b",
]

def input_guardrail(text: str) -> PolicyDecision:
    lowered = text.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, lowered):
            return PolicyDecision(
                "BLOCK", "HIGH", ["PROMPT_INJECTION"],
                "The request attempts to override or expose internal instructions."
            )

    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, lowered):
            return PolicyDecision(
                "BLOCK", "HIGH", ["SENSITIVE_DATA"],
                "The request contains or requests authentication secrets/sensitive credentials."
            )

    return PolicyDecision("ALLOW", "LOW", [], "Input passed initial policy checks.")

def tool_guardrail(user_id: str, call: ToolCall) -> PolicyDecision:
    risk = TOOL_RISK.get(call.name, "HIGH")

    if call.name not in TOOL_RISK:
        return PolicyDecision(
            "BLOCK", "HIGH", ["UNKNOWN_TOOL"],
            f"Tool '{call.name}' is not on the approved tool allowlist."
        )

    requested_customer_id = call.arguments.get("requested_customer_id")
    allowed, reason = authorize(user_id, requested_customer_id)

    if not allowed:
        return PolicyDecision(
            "BLOCK", "HIGH", ["RESOURCE_AUTHORIZATION"],
            reason
        )

    if call.name == "transfer_money":
        amount = float(call.arguments.get("amount", 0))
        beneficiary_id = call.arguments.get("beneficiary_id")

        if amount <= 0:
            return PolicyDecision(
                "BLOCK", "HIGH", ["INVALID_TRANSFER"],
                "Transfer amount must be positive."
            )

        return PolicyDecision(
            "ESCALATE", "HIGH",
            ["HIGH_IMPACT_ACTION", "HUMAN_APPROVAL_REQUIRED"],
            f"Transfer of ₹{amount:,.2f} to {beneficiary_id} requires human approval."
        )

    if risk == "MEDIUM":
        return PolicyDecision(
            "ALLOW", "MEDIUM", ["MEDIUM_RISK_MONITORED"],
            "Medium-risk tool permitted after authorization."
        )

    return PolicyDecision("ALLOW", "LOW", [], "Low-risk tool permitted.")

def output_guardrail(output: str) -> PolicyDecision:
    lowered = output.lower()

    leakage_terms = [
        "system prompt:",
        "internal instruction:",
        "customer password",
        "otp:",
    ]

    for term in leakage_terms:
        if term in lowered:
            return PolicyDecision(
                "BLOCK", "HIGH", ["OUTPUT_DATA_LEAKAGE"],
                "Output appears to contain internal or sensitive information."
            )

    unsafe_advice_terms = [
        "guaranteed return",
        "guaranteed profit",
        "you should invest all",
    ]

    for term in unsafe_advice_terms:
        if term in lowered:
            return PolicyDecision(
                "BLOCK", "HIGH", ["UNCONTROLLED_FINANCIAL_ADVICE"],
                "Output contains an unsafe or overly certain financial recommendation."
            )

    return PolicyDecision("ALLOW", "LOW", [], "Output passed validation.")

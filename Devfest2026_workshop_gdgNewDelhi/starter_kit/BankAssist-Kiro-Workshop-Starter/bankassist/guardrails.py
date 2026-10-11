"""BankAssist — AI Guardrails Practice Lab

Presenter: Ankit Mathur

EDUCATIONAL & ETHICAL USE ONLY
This is a simplified practice application for training and demonstration.
It is not a production banking application or security framework.
Use synthetic data only and test only in environments you are authorized to use.
Further security, architecture, compliance, privacy, and engineering validation
is required before adapting any pattern for real-world use.
"""

from .models import PolicyDecision, ToolCall

POLICY_VERSION = "0.1-STARTER"

# TODO 1: Add prompt-injection patterns.
# TODO 2: Add sensitive-data patterns.
# TODO 3: Add input guardrails.
# TODO 4: Add an explicit tool allowlist and risk classification.
# TODO 5: Enforce authorization before tool execution.
# TODO 6: Escalate high-impact financial actions.
# TODO 7: Add output validation.

def input_guardrail(text: str) -> PolicyDecision:
    return PolicyDecision("ALLOW", "LOW", [], "STARTER: input guardrails not implemented.")

def tool_guardrail(user_id: str, call: ToolCall) -> PolicyDecision:
    return PolicyDecision("ALLOW", "LOW", [], "STARTER: tool policy not implemented.")

def output_guardrail(output: str) -> PolicyDecision:
    return PolicyDecision("ALLOW", "LOW", [], "STARTER: output guardrails not implemented.")

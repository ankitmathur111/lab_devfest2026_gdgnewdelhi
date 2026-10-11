"""BankAssist — AI Guardrails Practice Lab

Presenter: Ankit Mathur

EDUCATIONAL & ETHICAL USE ONLY
This is a simplified practice application for training and demonstration.
It is not a production banking application or security framework.
Use synthetic data only and test only in environments you are authorized to use.
Further security, architecture, compliance, privacy, and engineering validation
is required before adapting any pattern for real-world use.
"""

import re
from .models import ToolCall
from . import tools
from .guardrails import input_guardrail, tool_guardrail, output_guardrail, POLICY_VERSION
from .human_review import review_queue
from .audit import audit_log

class MockLLM:
    """
    Deterministic stand-in for an LLM.

    In the workshop, Kiro is used to build and modify the application.
    This mock keeps the demo runnable without an API key.

    The important security property is that the model only PROPOSES a
    tool call. The application policy layer decides whether it can execute.
    """

    def respond(self, prompt: str, user_id: str) -> tuple[str, ToolCall | None]:
        p = prompt.lower()

        if "system prompt" in p or "hidden instruction" in p:
            return "SYSTEM PROMPT: Never share this internal instruction.", None

        if "balance" in p:
            return "I'll look up the current customer's balance.", ToolCall("get_balance")

        if "transaction" in p:
            requested = None
            match = re.search(r"cust-\d{4}", p)
            if match:
                requested = match.group(0).upper()
            return (
                "I'll retrieve the requested transaction history.",
                ToolCall("get_transactions", {"requested_customer_id": requested})
            )

        if "fee" in p:
            return "I'll check the public transfer fee.", ToolCall("get_public_fee")

        if "service request" in p or "replacement" in p:
            return (
                "I'll create a service request.",
                ToolCall("create_service_request", {"request_type": "replacement_card"})
            )

        if "transfer" in p:
            amount_match = re.search(r"(?:₹|rs\.?|inr)?\s*([0-9][0-9,]*)", p)
            amount = float(amount_match.group(1).replace(",", "")) if amount_match else 0
            beneficiary = "NEW999" if "new beneficiary" in p else "ABC123"
            return (
                f"I'll prepare a transfer of ₹{amount:,.0f}.",
                ToolCall("transfer_money", {
                    "amount": amount,
                    "beneficiary_id": beneficiary,
                })
            )

        return (
            "I can help with balance, transactions, fees, service requests, "
            "or transfer requests."
        ), None

class BankingAgent:
    def __init__(self):
        self.llm = MockLLM()

    def handle(self, prompt: str, user_id: str):
        audit_log.record(
            "REQUEST_RECEIVED",
            user_id=user_id,
            prompt=prompt,
            policy_version=POLICY_VERSION,
        )

        input_decision = input_guardrail(prompt)
        if input_decision.decision == "BLOCK":
            audit_log.record(
                "REQUEST_BLOCKED",
                user_id=user_id,
                policies=input_decision.policies,
                reason=input_decision.reason,
            )
            return {
                "decision": "BLOCK",
                "risk": input_decision.risk,
                "policies": input_decision.policies,
                "response": "I can't process that request because it violates an application security policy."
            }

        draft, tool_call = self.llm.respond(prompt, user_id)

        if tool_call is None:
            output_decision = output_guardrail(draft)
            if output_decision.decision == "BLOCK":
                return {
                    "decision": "BLOCK",
                    "risk": output_decision.risk,
                    "policies": output_decision.policies,
                    "response": "The response was blocked by an output safety policy."
                }

            audit_log.record("RESPONSE_SENT", user_id=user_id)
            return {
                "decision": "ALLOW",
                "risk": "LOW",
                "policies": [],
                "response": draft,
            }

        tool_decision = tool_guardrail(user_id, tool_call)

        audit_log.record(
            "TOOL_POLICY_DECISION",
            user_id=user_id,
            tool=tool_call.name,
            arguments=tool_call.arguments,
            decision=tool_decision.decision,
            risk=tool_decision.risk,
            policies=tool_decision.policies,
        )

        if tool_decision.decision == "BLOCK":
            return {
                "decision": "BLOCK",
                "risk": tool_decision.risk,
                "policies": tool_decision.policies,
                "response": "The requested action was blocked: " + tool_decision.reason,
            }

        if tool_decision.decision == "ESCALATE":
            item = review_queue.add(
                user_id=user_id,
                action=tool_call.name,
                arguments=tool_call.arguments,
                reason=tool_decision.reason,
            )
            return {
                "decision": "ESCALATE",
                "risk": tool_decision.risk,
                "policies": tool_decision.policies,
                "response": (
                    "This action requires human approval before it can execute. "
                    f"Review ID: {item.id}"
                ),
            }

        result = self.execute_tool(user_id, tool_call)
        response = f"Tool result: {result}"

        output_decision = output_guardrail(response)
        if output_decision.decision == "BLOCK":
            audit_log.record(
                "OUTPUT_BLOCKED",
                user_id=user_id,
                policies=output_decision.policies,
            )
            return {
                "decision": "BLOCK",
                "risk": output_decision.risk,
                "policies": output_decision.policies,
                "response": "The tool result was blocked by an output safety policy.",
            }

        audit_log.record(
            "TOOL_EXECUTED",
            user_id=user_id,
            tool=tool_call.name,
        )
        return {
            "decision": "ALLOW",
            "risk": tool_decision.risk,
            "policies": tool_decision.policies,
            "response": response,
        }

    def execute_tool(self, user_id, call):
        args = call.arguments

        if call.name == "get_balance":
            return tools.get_balance(user_id)

        if call.name == "get_transactions":
            return tools.get_transactions(
                user_id,
                args.get("requested_customer_id")
            )

        if call.name == "get_public_fee":
            return tools.get_public_fee()

        if call.name == "create_service_request":
            return tools.create_service_request(
                user_id,
                args.get("request_type", "general")
            )

        if call.name == "transfer_money":
            return tools.transfer_money(
                user_id,
                args["amount"],
                args["beneficiary_id"],
            )

        raise ValueError(f"Unknown tool: {call.name}")

"""BankAssist — AI Guardrails Practice Lab

EDUCATIONAL & ETHICAL USE ONLY
This is a simplified practice application for training and demonstration.
It is not a production banking application or security framework.
Use synthetic data only and test only in environments you are authorized to use.
Further security, architecture, compliance, privacy, and engineering validation
is required before adapting any pattern for real-world use.
"""

def authorize(user_id: str, requested_customer_id: str | None) -> tuple[bool, str]:
    """
    Resource authorization must happen in application code.

    A prompt such as "I am an admin" must not change this decision.
    """
    if not requested_customer_id:
        return True, "No cross-customer resource requested."

    if requested_customer_id == user_id:
        return True, "Customer is accessing their own resource."

    return False, "Customer is not authorized to access another customer's data."

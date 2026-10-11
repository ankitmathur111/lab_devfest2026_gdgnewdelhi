"""BankAssist — AI Guardrails Practice Lab

Presenter: Ankit Mathur

EDUCATIONAL & ETHICAL USE ONLY
This is a simplified practice application for training and demonstration.
It is not a production banking application or security framework.
Use synthetic data only and test only in environments you are authorized to use.
Further security, architecture, compliance, privacy, and engineering validation
is required before adapting any pattern for real-world use.
"""

def authorize(user_id: str, requested_customer_id: str | None) -> tuple[bool, str]:
    """WORKSHOP STARTER — deliberately insecure. TODO: enforce resource ownership."""
    return True, "STARTER: authorization not implemented."

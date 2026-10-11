from dataclasses import dataclass, field
from typing import Any, Literal

Decision = Literal["ALLOW", "BLOCK", "ESCALATE"]
Risk = Literal["LOW", "MEDIUM", "HIGH"]

@dataclass
class ToolCall:
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)

@dataclass
class PolicyDecision:
    decision: Decision
    risk: Risk
    policies: list[str] = field(default_factory=list)
    reason: str = ""

@dataclass
class ReviewItem:
    id: str
    user_id: str
    action: str
    arguments: dict[str, Any]
    reason: str
    status: str = "PENDING"

# Instructor Runbook — 60 Minutes

## 0–5 min — Scenario

"You are building an AI banking assistant. It can read customer data and initiate banking actions."

Ask:

> What is the dangerous part?

Expected insight:

> The dangerous part is not only what the AI says. It is what the AI can cause the system to do.

## 5–12 min — Build with Kiro

Give participants the starter requirements and ask Kiro to implement the agent.

## 12–17 min — Run

Show:

- balance
- transactions
- service request
- transfer request

## 17–22 min — Break

Attack:

- reveal system prompt
- access CUST-2002
- claim to be admin
- request transfer
- provide OTP

## 22–27 min — Introduce control plane

Show:

Input → Agent → Tool Policy → Tool → Output Policy

Explain that authorization is not delegated to the model.

## 27–42 min — Build guardrails

Participants implement:

1. authorization
2. tool allowlist
3. risk classification
4. human escalation
5. output checks
6. audit events

## 42–50 min — Red team

Participants attack another participant's app or their own implementation.

## 50–55 min — Human-in-loop

Demonstrate a pending transfer and approval/rejection.

## 55–58 min — Audit

Show the audit trail and ask:

> Can you explain why this action was blocked?

## 58–60 min — Take-home

Give everyone the completed reference repository.

Emphasize:

- The workshop is the starting point.
- The reference project is intentionally small.
- They should extend the guardrails after the session.

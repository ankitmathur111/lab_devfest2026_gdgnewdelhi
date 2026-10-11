# Guardrails Lab Specification

## Goal

Build a controlled banking AI assistant where the model can propose actions but cannot independently override application policy.

## Functional requirements

- Balance lookup
- Transaction lookup
- Service request
- Transfer request
- Human review queue
- Audit trail

## Security requirements

- Detect prompt injection
- Protect sensitive credentials
- Enforce resource authorization
- Allowlist tools
- Classify tool risk
- Escalate high-impact actions
- Validate output
- Log policy decisions

## Acceptance tests

A correct implementation must:

- block system-prompt extraction
- block cross-customer transaction access
- block unknown tools
- escalate transfers
- block sensitive output
- allow legitimate balance lookup
- preserve an audit event for security decisions

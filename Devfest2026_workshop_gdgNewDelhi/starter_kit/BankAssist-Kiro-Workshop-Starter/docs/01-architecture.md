# Architecture Walkthrough

## 1. Agent layer

`bankassist/agent.py`

The agent asks the model what it thinks should happen.

The model is allowed to propose:

    get_balance
    get_transactions
    get_public_fee
    create_service_request
    transfer_money

The model does **not** get to decide whether a tool call is authorized.

## 2. Input guardrails

`bankassist/guardrails.py`

The application checks for:

- prompt injection
- credential/secret requests
- card-like numbers
- attempts to disable security controls

## 3. Authorization

`authorization.py`

Authorization is based on application identity and requested resource.

This is deliberately outside the prompt.

## 4. Tool policy

`tool_guardrail()` determines:

- Is the tool on the allowlist?
- Is the user authorized?
- What is the risk?
- Does the action require human approval?

## 5. Human review

`human_review.py`

High-impact actions are converted into a review item.

The action does not execute just because the model requested it.

## 6. Output guardrail

`output_guardrail()` checks the generated/tool response before it reaches the user.

This gives two control points:

    before tool execution
    after model/tool output

## 7. Audit

`audit.py`

Important events are recorded with timestamps and policy decisions.

In a real system this would normally be sent to a durable, access-controlled logging/monitoring platform.

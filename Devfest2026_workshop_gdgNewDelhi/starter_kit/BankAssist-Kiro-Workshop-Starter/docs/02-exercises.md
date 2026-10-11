# Take-home Exercises

Open the project in Kiro and work through these exercises.

## Exercise 1 — Change the transfer threshold

Currently every transfer is escalated.

Change the policy so:

- transfers <= ₹25,000 require step-up authentication
- transfers > ₹25,000 require human approval

Do not remove the audit event.

Ask Kiro:

> Modify the transfer policy as described. Add tests for the boundary values ₹25,000 and ₹25,001. Do not change unrelated behavior.

## Exercise 2 — Add beneficiary risk

Make a transfer to `NEW999` automatically escalate even when the amount is small.

## Exercise 3 — Add rate limiting

Block a user after 5 blocked requests within 60 seconds.

## Exercise 4 — Add PII redaction

Instead of simply blocking a full account number in output, experiment with redaction:

    1234567890123456

becomes:

    ************3456

Think carefully about when redaction is appropriate and when blocking is safer.

## Exercise 5 — Add role-based access

Create:

- CUSTOMER
- SUPPORT
- ADMIN

Then define which tools each role may call.

Important: keep authorization outside the LLM prompt.

## Exercise 6 — Add a policy configuration file

Move risk thresholds into `policy.json`.

Then validate the configuration at application startup.

## Exercise 7 — Add adversarial tests

Create tests for:

- prompt injection
- indirect prompt injection
- cross-customer access
- unknown tools
- high-value transfers
- new beneficiaries
- sensitive output
- malicious tool arguments

## Exercise 8 — Replace the mock model

Create a model adapter interface:

    generate(prompt) -> model response

Keep the guardrails unchanged.

The objective is to demonstrate that changing the LLM does not remove the application's security boundary.

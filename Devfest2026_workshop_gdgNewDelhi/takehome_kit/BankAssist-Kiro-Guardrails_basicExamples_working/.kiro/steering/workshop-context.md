# Workshop Context

This repository is an educational banking AI-agent project.

Rules for changes:

1. Use synthetic data only.
2. Never place authorization solely in an LLM prompt.
3. Treat model output as untrusted input.
4. Tool access must be explicitly allowlisted.
5. High-impact financial actions must have a policy decision before execution.
6. Security decisions should be auditable.
7. Every guardrail change should have regression tests.
8. Prefer small, explainable policy functions over hidden magic.

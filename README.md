# viernes-ai-policies

A Python package that ships the guardrail policy configuration for the **Viernes AI Emma** agent — a conversational sales assistant for a residential real estate development.

The package exposes a single `GUARDRAILS_CONFIG` dict that can be consumed by any guardrail runtime to enforce safety and relevance rules at three stages of the conversation pipeline: pre-flight, input, and output.

---

## Installation

```bash
pip install git+https://github.com/Grupo-Guia/viernes-ai-policies.git
```

Or, from source:

```bash
git clone https://github.com/viernes-ai/viernes-ai-policies.git
cd viernes-ai-policies
pip install .
```

## Usage

```python
from viernes_ai_policies import GUARDRAILS_CONFIG

# Pass the config to your guardrail runtime
runtime.load_policy(GUARDRAILS_CONFIG)
```

`GUARDRAILS_CONFIG` is a plain Python dict deserialized from `viernes-ai-policies/config.json` at import time. No network calls are made.

---

## Package structure

```
viernes-ai-policies/
├── viernes-ai-policies/
│   ├── __init__.py      # Loads config.json and exports GUARDRAILS_CONFIG
│   └── config.json      # Policy definition (pre_flight / input / output)
├── pyproject.toml
├── README.md
└── POLICY.md            # Detailed explanation of every guardrail rule
```

---

## Policy overview

The config defines three pipeline stages, each with one or more guardrails:

| Stage | Guardrail | Purpose |
|---|---|---|
| `pre_flight` | Moderation | Block harmful content categories before processing |
| `pre_flight` | Prompt Injection Detection | Detect attempts to hijack the agent's instructions |
| `input` | Jailbreak | Detect attempts to bypass safety constraints |
| `input` | Off Topic Prompts | Keep the conversation scoped to real estate sales |
| `output` | Contains PII | Prevent the agent from leaking sensitive financial identifiers |
| `output` | NSFW Text | Block inappropriate language in agent responses |

See [POLICY.md](POLICY.md) for a full description of every guardrail, its parameters, and the reasoning behind each configuration choice.

---

## Contributing

1. Edit `viernes-ai-policies/config.json` to change policy rules.
2. Update `POLICY.md` to reflect any changes.
3. Bump `version` in `pyproject.toml` following [semver](https://semver.org/).
4. Open a pull request with a description of what changed and why.

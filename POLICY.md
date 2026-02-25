# Guardrail Policy Reference

This document describes every guardrail rule defined in `viernes-ai-policies/config.json` for the **Viernes AI Emma** agent — a Spanish-language sales assistant for a residential real estate development.

The policy is applied at three stages of each conversation turn:

```
User message
    └─► pre_flight  (always runs first, before any context is built)
    └─► input       (runs on the full user turn in context)
    └─► [agent processing]
    └─► output      (runs on the agent's response before delivery)
```

---

## Pre-flight guardrails

Pre-flight checks run on every incoming message before any agent logic executes. A failure here short-circuits the entire turn.

### Moderation

**Purpose:** Block messages that contain harmful or illegal content across a predefined set of categories.

**Categories enforced:**

| Category | Description |
|---|---|
| `sexual` | Sexually explicit content |
| `sexual/minors` | Sexual content involving minors |
| `hate` | Hate speech targeting protected groups |
| `hate/threatening` | Threatening hate speech |
| `harassment` | Harassment of individuals |
| `harassment/threatening` | Threatening harassment |
| `self-harm` | Content promoting self-harm |
| `self-harm/intent` | Expressed intent to self-harm |
| `self-harm/instructions` | Instructions for self-harm |
| `violence` | Violent content |
| `violence/graphic` | Graphic violence |
| `illicit` | Content related to illegal activities |
| `illicit/violent` | Violent illegal activities |

**Behavior:** If any category is detected, the message is blocked and the turn is terminated before the agent processes it.

---

### Prompt Injection Detection

**Purpose:** Detect attempts by malicious content (e.g., hidden instructions in user-supplied text) to override the agent's system prompt or alter its behavior.

| Parameter | Value | Notes |
|---|---|---|
| `model` | `gpt-4.1-mini` | Lightweight model used for fast classification |
| `confidence_threshold` | `0.7` | Messages scoring ≥ 0.7 are blocked |
| `include_reasoning` | `false` | Reasoning trace is not logged |

**Behavior:** Messages classified as prompt injection with confidence ≥ 0.7 are blocked before the agent sees them.

---

## Input guardrails

Input guardrails run on the user's message within the full conversation context (including prior turns up to `max_turns`).

### Jailbreak

**Purpose:** Detect attempts to bypass the agent's safety constraints or manipulate it into producing disallowed outputs through social engineering, role-play prompts, or other adversarial techniques.

| Parameter | Value | Notes |
|---|---|---|
| `model` | `gpt-4.1-mini` | Lightweight model used for fast classification |
| `confidence_threshold` | `0.7` | Messages scoring ≥ 0.7 are blocked |
| `max_turns` | `10` | Number of recent turns included in context for classification |
| `include_reasoning` | `false` | Reasoning trace is not logged |

**Behavior:** If a jailbreak attempt is detected with confidence ≥ 0.7, the message is blocked and the agent does not respond.

---

### Off Topic Prompts

**Purpose:** Keep the conversation scoped to the residential real estate development. Emma is a sales assistant and should not engage with unrelated requests.

| Parameter | Value | Notes |
|---|---|---|
| `model` | `gpt-4.1-mini` | Lightweight model used for fast classification |
| `confidence_threshold` | `0.7` | Messages scoring ≥ 0.7 are blocked as off-topic |
| `max_turns` | `10` | Number of recent turns included in context |
| `include_reasoning` | `false` | Reasoning trace is not logged |

**Scope definition (`system_prompt_details`):**

> Asistente de ventas de un desarrollo inmobiliario residencial.
> **PERMITIDO:** precios, unidades, amenidades, ubicación, planes de pago, citas y visitas, proceso de compra.
> **NO PERMITIDO:** política, consejos médicos o legales ajenos a la compra, temas sin relación al proyecto.

In English: Emma may discuss prices, available units, amenities, location, payment plans, appointments/visits, and the purchase process. She must not engage with politics, medical or legal advice unrelated to the purchase, or any topic unrelated to the development.

**Behavior:** Off-topic messages are blocked and the agent does not respond.

---

## Output guardrails

Output guardrails run on the agent's generated response before it is delivered to the user.

### Contains PII

**Purpose:** Prevent the agent from inadvertently leaking sensitive financial identifiers in its responses.

**Entities detected and blocked:**

| Entity | Description |
|---|---|
| `CREDIT_CARD` | Credit card numbers |
| `CVV` | Card verification values |
| `CRYPTO` | Cryptocurrency wallet addresses |
| `IBAN_CODE` | International bank account numbers |
| `BIC_SWIFT` | Bank identifier / SWIFT codes |
| `US_BANK_NUMBER` | US bank account numbers |
| `US_SSN` | US Social Security numbers |
| `US_ITIN` | US Individual Taxpayer Identification numbers |

| Parameter | Value | Notes |
|---|---|---|
| `detect_encoded_pii` | `false` | Encoded/obfuscated PII variants are not detected |
| `block` | `true` | Responses containing detected entities are blocked entirely |

**Behavior:** If any of the above entities are found in the agent's response, the response is suppressed and not delivered to the user.

---

### NSFW Text

**Purpose:** Ensure the agent's responses remain professional and appropriate, blocking any output that contains sexually explicit or otherwise inappropriate language.

| Parameter | Value | Notes |
|---|---|---|
| `model` | `gpt-4.1-mini` | Lightweight model used for fast classification |
| `confidence_threshold` | `0.7` | Responses scoring ≥ 0.7 are blocked |
| `max_turns` | `10` | Number of recent turns included in context |
| `include_reasoning` | `false` | Reasoning trace is not logged |

**Behavior:** Responses classified as NSFW with confidence ≥ 0.7 are suppressed and not delivered to the user.

---

## Versioning

The top-level config object and each pipeline stage carry an independent `version` field. Increment the relevant version when making changes so that consuming runtimes can detect and handle policy updates.

| Field | Current version |
|---|---|
| Root config | `1` |
| `pre_flight` | `1` |
| `input` | `1` |
| `output` | `1` |

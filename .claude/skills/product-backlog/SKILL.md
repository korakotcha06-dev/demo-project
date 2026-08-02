---
name: product-backlog
description: Turn a stakeholder brief or raw requirement into user stories, business rules, and a prioritized product backlog for this coffee-shop QR self-order project, written straight into docs/01-requirements. Trigger on /product-backlog, and proactively whenever the user describes a new feature/requirement for the QR ordering system and wants it broken down into buildable backlog items.
---

# Product Backlog (Requirement → Backlog)

Converts a requirement or brief into a structured, prioritized backlog that slots directly into this repo's `docs/01-requirements` pipeline (`01-spec` → `02-plan` → `03-task`).

## When to use
- Touch (the entrepreneur) describes a new feature or need for the QR ordering system in plain language.
- An existing `01-spec` doc needs to be broken down into phases (`02-plan`) or actionable tasks (`03-task`).
- Reviewing whether the current backlog still matches the founding brief in `CLAUDE.md`.

## Workflow

### 1. Clarify the ask
Restate the requirement in one sentence. If it's ambiguous on something only Touch can decide (payment flow, pricing, staff process), ask — otherwise pick the default that matches the founding brief (customer scans QR at table, orders without staff) and note the assumption instead of stopping.

### 2. Write user stories
One story per distinct capability, in Thai:
```
เป็น [บทบาท] ฉันต้องการ [สิ่งที่ทำ] เพื่อ [เหตุผล]
```
Split stories that bundle multiple actors (customer vs. kitchen staff vs. cashier) — each actor gets its own story.

### 3. Attach acceptance criteria
Every story needs a checklist or Given/When/Then that says exactly when it's "done." No story ships to `03-task` without this.

### 4. Surface business rules
Write down constraints that aren't obvious from the story alone — order limits per table, payment-before-or-after-serving, what happens when an item runs out mid-order, refund/cancellation rules. These go in `01-spec` alongside the stories they constrain, not buried in a task description.

### 5. Prioritize
Rank every new item P0/P1/P2 (Must/Should/Could). Default bias: a thin P0 slice that gets a customer from "scans QR" to "order reaches the kitchen" before any P1/P2 (loyalty points, multi-language, analytics, promotions).

### 6. File it into the pipeline
- Feature list + stories + business rules + scope → `docs/01-requirements/01-spec/`
- Phase/milestone grouping (which P0 items ship together) → `docs/01-requirements/02-plan/`
- Concrete to-do breakdown → `docs/01-requirements/03-task/`
- Keep every folder's `index.md` wikilinks intact — link new docs in, don't leave them orphaned.
- Never delete a superseded version — move it to `docs/00-archived` instead.

### 7. Report
Summarize: what's newly backlogged, what's P0 vs. later, and anything that needs Touch's decision before COULSON's team can start design/build. Don't dump every acceptance criterion into the chat reply — the docs are the deliverable, the chat reply is the summary.

## Output template
```
### [ID] ชื่อเรื่อง
เป็น [บทบาท] ฉันต้องการ [สิ่งที่ทำ] เพื่อ [เหตุผล]

Acceptance Criteria:
- [ ] ...

Priority: P0/P1/P2 (Must/Should/Could)
Phase: [maps to 02-plan milestone]
Notes/Assumptions: ...
```

## Operating rules
- Match the vault's existing language (Thai) and structure — this isn't a fresh doc format, it extends what's already in `docs/01-requirements`.
- Don't invent scope beyond what the brief or Touch's message implies — a thin, buildable P0 beats a speculative full feature set.
- This skill defines *what* to build; it does not architect *how* (no DB schema, no component design) — that's `02-design`, owned by COULSON's team once the backlog is stable.

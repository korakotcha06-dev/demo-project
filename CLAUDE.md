# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

This repository currently contains **no application code** — it is an Obsidian documentation vault scaffolding the SDLC for a product that has not been built yet. There is no `package.json`, build tool, linter, or test runner. Do not invent or assume build/lint/test commands; when real application code is added to this repo, this file should be updated with the actual commands.

## Product brief

The entrepreneur (ผู้ประกอบการ) running this repo is opening a coffee shop and wants a **QR-code self-order system**: customers scan a QR code at their table and place their own order without staff taking it manually. This is the founding brief behind `docs/01-requirements` — treat it as the source of truth when drafting specs, plans, or tasks in that folder, unless a doc there has since overridden it.

## Documentation architecture

The repo is an Obsidian vault (`.obsidian/`) using a fixed SDLC pipeline under `docs/`, where each stage's output feeds the next. Every folder has its own `index.md` that explains its purpose and links to the folders immediately before/after it via Obsidian wikilinks (`[[../path/index|label]]`) — **keep these links intact and update them when you add or move docs.**

Pipeline order:

1. **`01-requirements`** — what to build
   - `01-spec` — feature requirements, user stories, business rules, scope (source of truth for requirements)
   - `02-plan` — roadmap, phases/milestones, priority
   - `03-task` — concrete to-do breakdown from the plan
2. **`02-design`** — how it looks and how it's built, derived from requirements
   - `01-prototypes` — wireframes/mockups, user flow, design system basics
   - `02-technical` — architecture, database schema, API design, tech/library choices
3. **`03-testing`** — verification, derived from design
   - `01-test-plan` — test cases/scenarios, test data, in/out of scope
   - `02-test-result` — pass/fail results, bugs found, fix status
4. **`04-retrospectives`** — lessons learned per phase/sprint, drawing on `03-testing/02-test-result` and `05-log`
5. **`05-log`** — chronological changelog and decision log, referenced by retrospectives
6. **`00-archived`** — deprecated docs. **Never delete a doc outright** — move superseded versions or cancelled plans here to preserve history.

When adding new documentation, place it in the stage-appropriate folder (spec-level facts go in `01-spec`, not `02-plan`, etc.) and follow the upstream/downstream references already declared in that folder's `index.md`.

## Conventions

- Documentation is written in Thai (ไทย); match that language when adding to existing docs.
- Obsidian-specific settings (`.obsidian/app.json`, `appearance.json`, `core-plugins.json`) are vault config, not application config — leave them alone unless the user asks to change vault behavior.

# Generative Layout Orchestration

Use this for every branded prototype. The goal is coherent structural variety, not random novelty.

## Route By Layout Authority

Choose exactly one mode before designing:

- `reference-led`: the user provides explicit layout instructions, screenshots, a design system, or an approved prototype. Follow that structure faithfully unless it breaks WeCom shell or usability constraints.
- `evidence-derived`: the user provides meaningful business or brand material but no exact layout. Derive structure from the strongest evidence and operational journey.
- `open-generative`: the user provides only a brand, industry, or sparse idea. Generate a layout DNA from neutral business reasoning and public visual evidence. Do not invent internal brand systems.

Reference-led mode overrides anti-similarity novelty. Fidelity is more important than being different from prior cases.

## Structure DNA

Before markup, define:

1. `businessAxis`: the dominant daily operating object, such as queue, customer, appointment, campaign, service case, product interest, or team exception.
2. `navigationLogic`: frequency-first, lifecycle-first, object-first, role-first, journey-first, or hub-and-action.
3. `homeNarrative`: triage board, agenda, customer radar, campaign cockpit, service calendar, relationship pulse, manager exceptions, or another reasoned composition.
4. `informationDensity`: compact, balanced, or spacious, with a role/task rationale.
5. `moduleGrammar`: rows, ledger, timeline, board, matrix, split view, canvas, carousel, dossier, checklist, or progressive disclosure. Assign different grammars according to each module's job.
6. `visualAnchor`: typography, imagery, product object, material detail, data display, spatial rhythm, or controlled color field.
7. `signatureInteraction`: a useful state-changing workflow tied to the business axis.
8. `variationSeed`: a human-readable phrase derived from the current brief, such as `appointment-led / precise / object-first`. It is not a random number and must not contain a prior case name.

## Open-Generative Selection

When no layout authority exists:

1. List at least three plausible structure directions.
2. Score each direction against operational fit, brand/public evidence fit, information depth, interaction usefulness, and similarity risk.
3. Select the strongest direction, not the visually loudest one.
4. Record why the two alternatives were rejected.
5. Avoid the starter shell's navigation order and full module stack unless the selected direction independently justifies them.
6. Compare with available prior cases. If too similar, change a business-relevant structural dimension, not merely color, typography, labels, or class prefixes.

Do not default every fashion brand to editorial launch/countdown, every sports brand to black/fluorescent hero, every luxury brand to serif/three-column grid, or every wellness brand to soft cards. Industry is a clue, not a template.

## Coherence Rules

- Navigation, home ordering, detail architecture, and signature interaction must tell the same operating story.
- Visual expression may vary strongly, but operational pages must retain scan speed and complete information.
- A signature visual moment must connect to a real task, customer, appointment, or decision.
- Do not create branded internal tiers, rooms, campaigns, roles, or workflows from public marketing.
- Do not label an inferred decision `user-confirmed`.

## Generic DOM Contract

Implement the selected DNA with semantic markers:

- `data-layout-mode`
- `data-business-axis`
- `data-nav-model`
- `data-page-architecture`
- `data-module-grammar`
- `data-signature-interaction`

Markers must be on visible functional elements. CSS class names and brand prefixes do not count as structural evidence.

## Anti-Convergence Review

Across available cases, compare:

- navigation count and order;
- home block order and dominant block type;
- module grammar sequence;
- first-viewport operational composition;
- C360, task, and appointment architecture;
- signature interaction route/state change.

Require meaningful differences in at least three dimensions for open-generative cases. Do not penalize reference-led cases for matching their authoritative source.

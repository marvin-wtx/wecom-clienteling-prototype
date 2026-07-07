# Start Mode Router

Use this router before producing any major output. The first decision is not the module list; it is how much project evidence exists and whether the assistant should research, generalize, or build from the baseline.

## Required First Choice

Ask the user to choose one path when the request is open ended:

1. **Source-backed mode**: the user has decks, BRDs, screenshots, field lists, existing prototypes, meeting notes, or product requirements.
2. **Research-led mode**: the user has a brand, industry, market, or business objective, but not enough product material.
3. **Baseline mode**: the user has little material and wants a reusable WeCom Clienteling starter framework quickly.
4. **Hybrid mode**: the user has a rough brief and also wants public research plus the reusable baseline.

If the user says "先做一个", "先给我一版", or gives a brand with no product material, default to hybrid mode. If the user gives no brand, no industry, and no material, default to baseline mode and clearly mark assumptions.

## Minimum Intake

Ask only what is needed to start:

- Start mode: source-backed, research-led, baseline, or hybrid.
- Output target: written plan/brief, HTML prototype, Figma/PPT handoff, or QA review.
- Industry and frontline role term: `SA`, `FA`, `BA`, advisor, consultant, or client-specific term.
- Required demo depth: full clickable prototype, structural page map, or coverage/QA only.

Do not ask every questionnaire item up front unless the user explicitly wants a complete discovery form.

## Source-Backed Mode

Use when there is authoritative material.

Actions:
- Inspect all provided files before proposing structure.
- Extract capabilities, roles, objects, states, page candidates, and open questions.
- Preserve confirmed terminology, role labels, field vocabulary, business states, and integration names.
- Separate generic WeCom Clienteling capabilities from project-specific extensions.
- Only add baseline defaults where the source is silent.

Deliverables:
- Evidence-backed capability map.
- Flow matrix with source notes.
- Page inventory with A/B/C depth.
- Field vocabulary map.
- Prototype brief or implementation plan.
- Coverage QA against the provided source.

## Research-Led Mode

Use when the user asks the assistant to research a brand, category, or public business context.

Actions:
- Confirm research dimensions before deep work, or state a compact default plan when the user wants speed.
- Research current public facts with sources when brand, product, store, campaign, or policy details matter.
- Translate research into clienteling assumptions instead of copying marketing language into every screen.
- Keep public research distinct from product requirements; label it as inferred context.

Suggested research dimensions:
- Brand positioning, tone, product/category focus, and campaign language.
- Retail/service model and likely advisor workflows.
- Industry role naming and customer relationship norms.
- Member/customer vocabulary and likely lifecycle states.
- Content, appointment, service, event, or consultation opportunities.
- WeCom/private-domain touchpoints and native send constraints.
- Visual references, density, color use, and operational UI tone.

Deliverables:
- Research summary with citations when web research was used.
- Inferred capability priorities.
- Prototype data assumptions.
- Page inventory and demo journeys based on public evidence plus reusable baseline rules.
- Open questions separating facts from assumptions.

## Baseline Mode

Use when the user has no solid source material.

Actions:
- Read `references/baseline-framework.md`.
- Read `references/reference-page-blueprints.md`.
- Build from the standard WeCom mini-program clienteling structure.
- Use neutral vocabulary for customer/member fields unless the user chooses labels.
- Do not use any project-specific field names, member-system names, loyalty concepts, or branded terms.
- Do not include Opportunity Follow-Up unless the user confirms a real opportunity lifecycle.

Baseline mode is allowed to produce a complete starter prototype, but it must not be shallow. Every A-level page needs distinct data, state, and action logic.

Deliverables:
- Assumptions and excluded modules.
- Baseline capability map.
- Realistic sample data model.
- Page inventory with A/B/C depth.
- Generic demo journeys.
- Prototype implementation notes using the bundled shell.
- QA checklist for baseline completeness.

## Hybrid Mode

Use when there is a rough prompt plus public research or category assumptions.

Actions:
- Start with the reusable baseline.
- Replace generic assumptions with researched or user-provided facts.
- Keep uncertain items labeled as assumptions.
- Avoid overfitting the prototype to public marketing content when the product behavior is still unknown.

Deliverables:
- A mixed source table: provided facts, public research, inferred assumptions, and generic baseline defaults.
- A prioritized prototype scope.
- Page inventory and data model showing which items are confirmed vs assumed.

## Mode Switch Rules

- If source material arrives after baseline work starts, switch to source-backed mode and reconcile the baseline against it.
- If research reveals a major channel mismatch, ask whether the WeCom mini-program assumption still holds.
- If the user asks for HTML prototype output at any point, read `references/prototype-shell-contract.md` and use `assets/prototype-shell/index.html` as the base.
- If the user asks for review, use the selected mode as context but lead with QA findings.

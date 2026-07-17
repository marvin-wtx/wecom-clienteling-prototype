# One-Pass Prototype Gates

Use this workflow for every HTML prototype generation task. The objective is not literal single-attempt code generation; it is one user request producing a complete, validated result without asking the user to discover predictable quality defects.

## Gate 1: Connected Data First

Create the connected sample data model before page markup:

- Customers, tasks, appointments, assets, metrics, roles, and permissions use stable IDs.
- Task target counts derive from `targetIds.length` or one shared count property.
- Customer names, owners, states, due dates, and next actions remain consistent across list and detail pages.
- Appointment customer and linked task resolve through IDs.
- Do not hand-write the same count or state separately in multiple page functions.

Run a consistency pass before styling. Reject conflicting counts, dates, statuses, names, or owners.

Build the evidence ledger from `evidence-and-implementation-integrity.md`. Keep assumptions out of UI and define neutral fallbacks.

Read `generative-layout-orchestration.md`. Select layout authority mode and complete the structure DNA before markup. In open-generative mode, compare at least three directions and record why one wins.

For open-generative or evidence-derived branded HTML/clickable work, read `operating-archetype-selection.md` before selecting structure DNA. Compare three distinct operating archetypes, record the operational tension, and do not use the starter priority queue as a sparse-brief fallback.

For open-generative or evidence-derived branded work, read `creative-divergence-system.md`. Define the creative thesis, inspiration transpositions, high-impact divergence levers, portfolio contrast, and coherence proof before page contracts.

Read `prototype-delivery-discipline.md`. Treat evidence, structure, product logic, data model, page contracts, prototype, and QA as required delivery stages, not optional notes.

## Gate 2: Page Contracts

Classify each page as A, B, or C depth before implementation.

For A-level pages:

- Cover the capability vocabulary from `page-information-contract.md` using truthful `data-info-capability` markers.
- Populate every region with decision-supporting fields, not only a heading or one sentence.
- Include the action result, blocked reason, and recovery path where relevant.
- Keep page-specific structures distinct.

Capabilities do not prescribe layout. Deliberately choose section order, grouping, tabs, timelines, tables, checklists, progressive disclosure, and sticky actions for the brand, role, and journey. Do not copy the bundled template's module stack unless evidence supports it.

## Gate 3: Workbench First

The home first viewport must expose:

- At least two real KPI items marked `data-home-kpi`, each containing a visible `data-metric-label`.
- At least two operational regions marked `data-home-operational`, such as priority customers, tasks, appointments, or exceptions.
- At most one campaign/editorial/brand storytelling region before the first operational region.

A campaign countdown is not a KPI. A campaign card is not a second operational region. Brand moments may introduce work but cannot displace work.

## Gate 4: Brand Skin

Apply brand evidence after the operational skeleton is complete:

- Use brand typography, geometry, imagery discipline, and accent rules on the page layer.
- Keep high-density operational surfaces neutral and fast to scan.
- Limit strong brand moments to one or two per page.
- Never display internal QA labels such as `BRAND EXPRESSIVE`, `WORKBENCH DENSE`, `ACCENT 2/2`, token names, design rationale, or implementation notes inside the product UI.
- Do not invent logos, product assets, campaign claims, or proprietary UI details.
- Complete `structuralDifferentiation` in the visual token before styling. Navigation and page composition must differ for business or brand reasons, not novelty alone.

## Gate 5: Native And Shell Boundaries

- Preserve phone-frame, status-bar, capsule, safe-area, responsive, sticky-action, and native WeCom mechanics.
- Start from the V3 shell kit, then remove `renderKitPreview` and build the project's data, routes, pages, navigation, and state transitions. The kit supplies a frame and primitives, not an acceptable default home, tab order, or page composition.
- Do not use `assets/prototype-shell-demo/` as a starting point. It is a comparison fixture whose full V2 business stack is intentionally quarantined from generation.
- Configure `mountReviewControls` for the desktop stage with project roles, free-browse/Journey mode, preset journeys, reset, and relevant entry routes. Bind `wecom-review-change` to the project's route/state model and use `journeyHud` during guided review. These demo controls are protected shell capability, not page-layer IA.
- Choose 3-5 top-level navigation items from the project's primary journeys. Their set, order, labels, icons, center-action policy, active treatment, and visual style are adaptable.
- Do not copy the default five-item order automatically. Explain the chosen navigation in the visual token.
- Keep mini-program navigation titles short: prefer Chinese titles of 2-6 characters. Keep ASCII titles to 8 characters or fewer; move longer English branding into the page body.
- Keep the WeCom capsule, back action, title, and safe area readable without truncation.

## Gate 6: Automated QA

Run:

```bash
python3 scripts/check_visual_tokens.py docs/visual-token.json
python3 scripts/check_creative_divergence.py docs/visual-token.json
python3 scripts/check_delivery_review.py docs/prototype-delivery-review.json
python3 scripts/check_prototype_shell.py prototype/index.html
python3 scripts/check_workbench_implementation.py prototype/index.html
python3 scripts/check_page_information.py prototype/index.html
python3 scripts/check_token_implementation.py docs/visual-token.json prototype/index.html
python3 scripts/check_prototype_block_layout.py docs/visual-token.json prototype/index.html
python3 scripts/check_prototype_delivery_bundle.py .
```

Treat every failure as blocking. The bundle gate requires `prototype/index.html`, visual token, delivery review, case evaluation, and real screenshot files; a standalone HTML file cannot pass release. Do not add empty `data-*` markers, hidden labels, duplicate text, or irrelevant keywords to satisfy a checker.

## Gate 7: Rendered QA

Open the prototype in the user-facing browser at a 390px by 844px mini-program viewport and inspect:

- Home.
- Customer list and C360.
- Task list and task detail.
- Appointment list and appointment detail.
- Native WeCom handoff when in scope.

Verify:

- Metric labels are actually visible.
- No foreground/background color collision, especially secondary buttons and disabled states.
- Navigation titles are not ellipsized.
- No overlap or clipping.
- First viewport obeys the workbench-first rule.
- Sticky actions do not cover the last content.
- Each full-detail page visibly contains the required decision dimensions.
- Sample data remains consistent while navigating.

Automated checks do not replace rendered QA. If the source passes but the rendered page fails, fix the page and rerun both.

Complete the delivery review from `assets/templates/prototype-delivery-review-template.json`. Scores below 4, true anti-generic flags, placeholder self-critique answers, or missing rendered checks are blockers.

Create `docs/prototype-case-evaluation.json` from `assets/templates/prototype-case-evaluation-template.json`. Capture actual screenshots for home, C360, task detail, and appointment detail (or an explicit scope exception), record at least three observed state-changing interactions, and run:

```bash
python3 scripts/check_prototype_case_evaluation.py docs/prototype-case-evaluation.json
```

When prior open-generative or evidence-derived cases are available, compare against each case:

```bash
python3 scripts/check_portfolio_diversity.py docs/prototype-case-evaluation.json \
  --reference ../prior-case/docs/prototype-case-evaluation.json
```

When a project portfolio index exists, use `assets/templates/prototype-portfolio-index-template.json` and check the entire indexed portfolio in one command instead of choosing references manually.

When prior brand cases are available, also run:

```bash
python3 scripts/check_structural_similarity.py prototype/index.html \
  --token docs/visual-token.json \
  --reference ../prior-case/prototype/index.html
```

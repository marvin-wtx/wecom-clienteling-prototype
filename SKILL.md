---
name: wecom-clienteling-prototype
description: Convert WeCom/WeChat Work ecosystem mini-program clienteling tool materials, or sparse early ideas, into reusable baseline frameworks, capability maps, page inventories, page-level interaction standards, task-execution models, field-vocabulary mapping, prototype briefs, WeCom native replicas such as 新建群发, brand visual evidence extraction, visual tokens, responsive prototype shells, and coverage QA. Use when the user asks to analyze BRDs, feature lists, screenshots, workflows, search/filter/tab/page-state details, task execution, 1v1/1vN/Moments/native broadcast flows, management dashboards, by-staff performance drilldowns, role/permission notes, CRM/CDP/MA/member-system integrations, FA/SA/BA terminology, customer/member field naming, brand visual references, UI restoration, opportunity logic, or existing prototypes for WeCom mini-program Clienteling, retail clienteling, private-domain sales assistant, C360, appointment, content sharing, or dashboard prototype work.
---

# WeCom Clienteling Prototype

Use this skill to turn clienteling inputs into a prototype-ready product plan. Treat any supplied source material as project-specific evidence to generalize from, not as mandatory scope for future work.

## First Split

First route the request by input state:

- **Source-backed mode**: the user has existing materials such as BRDs, decks, screenshots, field lists, notes, or prototypes.
- **Research-led mode**: the user has a brand, industry, market, or objective and needs the assistant to research the context.
- **Baseline mode**: the user has little or no solid material and wants a reusable WeCom Clienteling starter framework.
- **Hybrid mode**: the user has a rough prompt and needs public research plus the reusable baseline.

Then classify the deliverable into one or more work modes:

- **Business extraction**: derive capability modules, actors, objects, states, permissions, and unresolved questions from messy source material.
- **Baseline framework**: build a reusable starter IA, page inventory, and interaction chain from generic WeCom Clienteling capabilities when the user has little or no solid source material.
- **Prototype planning**: convert business capabilities into journeys, page inventory, navigation, page-depth levels, and demo flows.
- **Interaction standardization**: convert search, filter, sort, tab, bottom-sheet, and page-state details into reusable cross-page rules.
- **Task execution modeling**: define how 1v1, 1vN, Moments, native broadcast, appointment, content, and feedback actions execute.
- **Prototype execution**: write an execution brief for HTML, Figma, slides, or another prototype surface, with WeCom mini-program and demo-shell constraints.
- **Prototype shell implementation**: produce or revise an HTML/clickable prototype by reusing the bundled mini-program shell source, not by inventing a new container.
- **Prototype presentation**: specify desktop review stage, mobile full-screen mode, role switching, control visibility, free browsing, and preset journey demo behavior.
- **WeCom native replication**: decide when to replicate native WeCom pages, such as 新建群发, instead of designing a custom clienteling page.
- **Visual direction**: define industry-appropriate naming, prototype style references, brand fit, and reusable visual direction before implementation.
- **Brand visual extraction**: turn brand references, screenshots, public research, or style examples into evidence-backed visual tokens and page-layer design rules.
- **Coverage QA**: check an existing prototype against the capability map, flows, states, permissions, and integration assumptions.

## Required Workflow

1. Read `references/start-mode-router.md` before choosing a workflow path for an open-ended request.
2. Inspect the user's source material before inventing structure when source-backed mode is selected.
3. If source material is weak or missing, read `references/baseline-framework.md` and `references/reference-page-blueprints.md` before proposing a generic baseline.
4. Read `references/capability-map.md` for the reusable WeCom Clienteling capability model.
5. Read `references/prototype-pipeline.md` when turning business inputs into prototype outputs.
6. Read `references/module-to-page-patterns.md` when creating page inventories, IA, demo flows, or prototype briefs.
7. Read `references/reference-page-blueprints.md` when defining baseline page content, sample data, page-level states, or HTML prototype page structure.
8. Read `references/page-information-contract.md` when implementing or reviewing home metrics, C360, task detail, appointment detail, or any A-level full-detail page.
9. Read `references/interaction-patterns.md` when specifying search, filter, sort, tabs, page states, list controls, or reusable page-level interactions.
10. Read `references/task-execution-patterns.md` when specifying task list/detail behavior, execution methods, target handling, native send handoff, or completion feedback.
11. Read `references/wecom-mini-program-constraints.md` when designing pages, flows, interactions, integrations, or prototype implementation.
12. Read `references/wecom-native-page-replication.md` when a flow enters WeCom native compose, broadcast, recipient, or send-result behavior, or when source material mentions 新建群发, 群发, 原生企微页面, native WeCom, broadcast, or mass send.
13. Read `references/prototype-shell-contract.md` before producing, revising, or reviewing an HTML/clickable prototype.
14. Use `assets/prototype-shell/index.html` as the starting source for HTML prototypes unless the user explicitly requires another stack.
15. Read `references/prototype-presentation-spec.md` when producing an HTML/clickable prototype, demo shell, or prototype execution brief.
16. Read `references/terminology.md` when role naming, industry vocabulary, customer/member field names, or Chinese/English labels affect credibility.
17. Read `references/visual-design-reference.md` when producing or briefing a visual prototype.
18. Read `references/brand-visual-extraction.md` when brand references, public brand research, screenshots, high-fidelity UI generation, UI restoration, or brand-skinned HTML prototypes are in scope.
19. Use `assets/templates/visual-token-template.json` when producing a brand visual token. If the token is saved as JSON, run `scripts/check_visual_tokens.py` before implementation or delivery.
20. Run `scripts/check_workbench_implementation.py` on branded HTML prototypes to verify the visual token's workbench-balance promises are actually implemented.
21. Run `scripts/check_page_information.py` on HTML prototypes with home metrics, C360, task detail, or appointment detail pages. Treat failures as page-depth defects, not optional polish.
22. Read `references/intake-questionnaire.md` when source material is missing actors, integration scope, page depth, demo goals, visual direction, terminology, WeCom mini-program constraints, native page replication, presentation mode, interaction standards, task execution details, or acceptance criteria.
23. Read `references/qa-rubric.md` when reviewing coverage or validating an existing prototype.
24. Use `assets/templates/` files as output skeletons when the user wants a structured deliverable.

## Domain Rule

Assume the target product is a WeCom/WeChat Work ecosystem mini-program clienteling tool unless the user explicitly asks to adapt the method to another channel. Do not design it as a generic SaaS dashboard, consumer shopping app, or standalone mobile app by default. Desktop views are review/demo containers for the mobile mini-program experience, not the primary product surface.

Treat WeCom native page replicas as a separate surface from clienteling mini-program pages. If a business action leaves the clienteling tool and enters a native WeCom compose/send/broadcast page, replicate the native page pattern instead of redesigning it as branded clienteling UI.

Keep core WeCom Clienteling capabilities separate from project-specific integrations. Do not assume every clienteling project has a proprietary member-system, loyalty, commerce, content, CRM/CDP/MA, service, appointment-resource, or external ecosystem integration. Ask whether such integrations exist, then model them as extension modules.

Keep Opportunity Follow-Up separate from the default core model. Only consider it when the user mentions signals such as opportunity,重点客人, high-value customer, priority client, VIP follow-up, high-potential customer, lead, pipeline, purchase intent, next-best-action, or sustained nurturing. Then ask whether the need is just segmentation/task targeting or a real opportunity lifecycle before adding an Opportunity module.

## Output Principles

- Produce business-first artifacts before screens: capability map, flow matrix, page inventory, and open questions.
- If the user has little source material, produce a baseline framework first, then mark assumptions and customization questions.
- In baseline mode, use `references/reference-page-blueprints.md` to create distinct page structures, connected sample data, and meaningful state/action logic. Do not produce repeated card pages with generic filler.
- Give every rendered metric a visible label, unit where relevant, period/scope when ambiguous, and drilldown. Bare numbers are a blocking defect even when labels exist in data or source code.
- For A-level C360, task detail, and appointment detail pages, satisfy the distinct information-region minimums in `references/page-information-contract.md`. Do not present a summary card plus one action as a complete detail page.
- In HTML prototypes, mark KPI labels with `data-metric-label` and distinct A-level detail regions with `data-info-region="<region-name>"` so semantic coverage can be validated.
- Make assumptions explicit when the user has not provided enough material.
- Preserve local terminology from the user's materials, including module names, role names, field labels, and industry-specific sales-associate terms.
- Determine FA/SA/BA during intake or from industry context. Do not expose FA/SA/BA as a runtime selector in the prototype shell.
- Do not default to project-specific customer/member field names. If source material does not confirm field labels, use neutral business labels such as customer identifier, member identifier, contact method, customer grouping, member level, profile label, and lifecycle state.
- For prototypes, separate **full-detail pages**, **structural pages**, and **navigation/skeleton pages**.
- For HTML/clickable prototypes, start from `assets/prototype-shell/index.html` or port its classes and behavior directly. Do not recreate the phone frame, WeCom mini-program container, top bar, capsule, or bottom tabbar from scratch.
- For HTML/clickable prototypes, keep the desktop review shell as a compact console around a 390px by 844px mini-program viewport, scaled to fit the desktop window without cropping.
- For HTML/clickable prototypes, preserve the desktop phone frame including the iPhone-style notch. Hide decorative phone hardware only in mobile full-screen mode.
- Preserve the protected top shell geometry: 38px status bar, nav title and WeCom capsule centered in the nav row below it, compact notch, and status text showing `9:41` and `5G` without decorative signal-dot placeholders.
- For HTML/clickable prototypes, implement desktop review stage and mobile full-screen mode as code-level responsive behavior. Do not expose a visible mobile/desktop selector in the product UI.
- Preserve the protected shell layer, but adapt the page design layer to user-provided business materials, brand references, visual references, and fidelity goals so different projects do not look identical.
- For high-fidelity branded prototypes or UI restoration, produce a compact evidence table and brand visual token before implementation. Map visual evidence into page-layer CSS variables, component rules, imagery rules, module-specific layout choices, and a workbench balance plan.
- Strong brand visual expression is allowed and often desirable, but keep customer lists, task execution, appointment rows, dashboard drilldowns, search/filter controls, and native WeCom handoffs faster to scan than decorative brand moments.
- Do not invent exact brand assets, proprietary UI details, product imagery, membership terms, or campaign copy. Use provided/public evidence, neutral defaults, or explicit assumptions.
- Include role switching, permission-driven show/hide rules, free-browse mode, and preset journey mode when the user asks for an interactive review prototype.
- For manager, regional, or HQ roles, include a management dashboard structure and a by-frontline-role performance drilldown when dashboard/tracking is in scope. Reuse generic metric groups such as sales or contribution, customer operation, appointment/service conversion, task execution, and WeCom connection; adapt names and formulas to the user's source material.
- Keep desktop-only review controls, role controls, and preset journey controls outside the mini-program screen; hide them in mobile presentation.
- Preserve required WeCom native replicas, including 新建群发, recipient summary, message/content payload, asset selection entry, send action, frequency note, and return-to-business result state when the flow requires them.
- Use SVG icons or an approved icon library. Do not use emoji for tabbar icons, quick entrances, task markers, page states, or placeholder illustrations.
- Standardize reusable page interactions, including search fields, filter groups, sort behavior, tab usage, bottom sheets, disabled-action reasons, and empty/loading/error/no-permission states.
- Standardize task execution by separating task source, task type, target grain, execution channel, native handoff, completion feedback, and measurable result.
- Define visual direction before implementation: brand fit, industry convention, reference sources, density, tone, component style, and what should remain generic.
- Run `scripts/check_prototype_shell.py` and `scripts/check_page_information.py` on generated HTML prototypes before considering them complete. For branded prototypes, also run `scripts/check_workbench_implementation.py` so brand expression does not erase search/filter, task execution, appointment, dashboard, or native handoff clarity. Then visually verify desktop and mobile render paths, including metric-label visibility.
- Validate that each important flow has an actor, trigger, customer state, system state, action, result, and recovery/exception path.

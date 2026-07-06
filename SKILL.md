---
name: wecom-clienteling-prototype
description: Convert WeCom/WeChat Work ecosystem mini-program clienteling tool materials, or sparse early ideas, into reusable baseline frameworks, capability maps, page inventories, page-level interaction standards, task-execution models, field-vocabulary mapping, prototype briefs, WeCom native replicas such as 新建群发, visual direction, responsive prototype shells, and coverage QA. Use when the user asks to analyze BRDs, feature lists, screenshots, workflows, search/filter/tab/page-state details, task execution, 1v1/1vN/Moments/native broadcast flows, role/permission notes, CRM/CDP/MA/member-system integrations, FA/SA/BA terminology, customer/member field naming, visual references, opportunity logic, or existing prototypes for WeCom mini-program Clienteling, retail clienteling, private-domain sales assistant, C360, appointment, content sharing, or dashboard prototype work.
---

# WeCom Clienteling Prototype

Use this skill to turn clienteling inputs into a prototype-ready product plan. Treat any supplied source material as project-specific evidence to generalize from, not as mandatory scope for future work.

## First Split

Classify every request into one or more work modes:

- **Business extraction**: derive capability modules, actors, objects, states, permissions, and unresolved questions from messy source material.
- **Baseline framework**: build a reusable starter IA, page inventory, and interaction chain from generic WeCom Clienteling capabilities when the user has little or no solid source material.
- **Prototype planning**: convert business capabilities into journeys, page inventory, navigation, page-depth levels, and demo flows.
- **Interaction standardization**: convert search, filter, sort, tab, bottom-sheet, and page-state details into reusable cross-page rules.
- **Task execution modeling**: define how 1v1, 1vN, Moments, native broadcast, appointment, content, and feedback actions execute.
- **Prototype execution**: write an execution brief for HTML, Figma, slides, or another prototype surface, with WeCom mini-program and demo-shell constraints.
- **Prototype presentation**: specify desktop review stage, mobile full-screen mode, role switching, control visibility, free browsing, and preset journey demo behavior.
- **WeCom native replication**: decide when to replicate native WeCom pages, such as 新建群发, instead of designing a custom clienteling page.
- **Visual direction**: define industry-appropriate naming, prototype style references, brand fit, and reusable visual direction before implementation.
- **Coverage QA**: check an existing prototype against the capability map, flows, states, permissions, and integration assumptions.

## Required Workflow

1. Inspect the user's source material before inventing structure.
2. If source material is weak or missing, read `references/baseline-framework.md` and propose a generic baseline with assumptions.
3. Read `references/capability-map.md` for the reusable WeCom Clienteling capability model.
4. Read `references/prototype-pipeline.md` when turning business inputs into prototype outputs.
5. Read `references/module-to-page-patterns.md` when creating page inventories, IA, demo flows, or prototype briefs.
6. Read `references/interaction-patterns.md` when specifying search, filter, sort, tabs, page states, list controls, or reusable page-level interactions.
7. Read `references/task-execution-patterns.md` when specifying task list/detail behavior, execution methods, target handling, native send handoff, or completion feedback.
8. Read `references/wecom-mini-program-constraints.md` when designing pages, flows, interactions, integrations, or prototype implementation.
9. Read `references/wecom-native-page-replication.md` when a flow enters WeCom native compose, broadcast, recipient, or send-result behavior, or when source material mentions 新建群发, 群发, 原生企微页面, native WeCom, broadcast, or mass send.
10. Read `references/prototype-presentation-spec.md` when producing an HTML/clickable prototype, demo shell, or prototype execution brief.
11. Read `references/terminology.md` when role naming, industry vocabulary, customer/member field names, or Chinese/English labels affect credibility.
12. Read `references/visual-design-reference.md` when producing or briefing a visual prototype.
13. Read `references/intake-questionnaire.md` when source material is missing actors, integration scope, page depth, demo goals, visual direction, terminology, WeCom mini-program constraints, native page replication, presentation mode, interaction standards, task execution details, or acceptance criteria.
14. Read `references/qa-rubric.md` when reviewing coverage or validating an existing prototype.
15. Use `assets/templates/` files as output skeletons when the user wants a structured deliverable.

## Domain Rule

Assume the target product is a WeCom/WeChat Work ecosystem mini-program clienteling tool unless the user explicitly asks to adapt the method to another channel. Do not design it as a generic SaaS dashboard, consumer shopping app, or standalone mobile app by default. Desktop views are review/demo containers for the mobile mini-program experience, not the primary product surface.

Treat WeCom native page replicas as a separate surface from clienteling mini-program pages. If a business action leaves the clienteling tool and enters a native WeCom compose/send/broadcast page, replicate the native page pattern instead of redesigning it as branded clienteling UI.

Keep core WeCom Clienteling capabilities separate from project-specific integrations. Do not assume every clienteling project has a proprietary member-system, loyalty, commerce, content, CRM/CDP/MA, service, appointment-resource, or external ecosystem integration. Ask whether such integrations exist, then model them as extension modules.

Keep Opportunity Follow-Up separate from the default core model. Only consider it when the user mentions signals such as opportunity,重点客人, high-value customer, priority client, VIP follow-up, high-potential customer, lead, pipeline, purchase intent, next-best-action, or sustained nurturing. Then ask whether the need is just segmentation/task targeting or a real opportunity lifecycle before adding an Opportunity module.

## Output Principles

- Produce business-first artifacts before screens: capability map, flow matrix, page inventory, and open questions.
- If the user has little source material, produce a baseline framework first, then mark assumptions and customization questions.
- Make assumptions explicit when the user has not provided enough material.
- Preserve local terminology from the user's materials, including module names, role names, field labels, and industry-specific sales-associate terms.
- Do not default to project-specific customer/member field names. If source material does not confirm field labels, use neutral business labels such as customer identifier, member identifier, contact method, customer grouping, member level, profile label, and lifecycle state.
- For prototypes, separate **full-detail pages**, **structural pages**, and **navigation/skeleton pages**.
- For HTML/clickable prototypes, specify both desktop review stage and mobile full-screen behavior, including which controls appear only in desktop stage.
- Include role switching, permission-driven show/hide rules, free-browse mode, and preset journey mode when the user asks for an interactive review prototype.
- Preserve required WeCom native replicas, including 新建群发, recipient summary, message/content payload, asset selection entry, send action, frequency note, and return-to-business result state when the flow requires them.
- Standardize reusable page interactions, including search fields, filter groups, sort behavior, tab usage, bottom sheets, disabled-action reasons, and empty/loading/error/no-permission states.
- Standardize task execution by separating task source, task type, target grain, execution channel, native handoff, completion feedback, and measurable result.
- Define visual direction before implementation: brand fit, industry convention, reference sources, density, tone, component style, and what should remain generic.
- Validate that each important flow has an actor, trigger, customer state, system state, action, result, and recovery/exception path.

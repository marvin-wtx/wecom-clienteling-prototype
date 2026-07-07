# Prototype Pipeline

Use this workflow to convert source material into a prototype plan.

## 0. Start Mode Routing

Before source intake, read `references/start-mode-router.md` and choose:

- Source-backed mode when authoritative materials exist.
- Research-led mode when the user asks for public brand/category research.
- Baseline mode when there is little material and speed matters.
- Hybrid mode when a rough prompt should be combined with public research and reusable baseline assumptions.

The chosen mode determines evidence handling:
- Source-backed facts can become requirements.
- Public research should be cited and labeled as context or inference.
- Baseline defaults must be marked as assumptions.
- Mixed outputs need a source table showing provided facts, researched facts, inferences, and generic defaults.

## 1. Source Intake

Inputs may include BRD, feature list, deck, screenshots, field list, user journey, meeting notes, existing prototype, or raw stakeholder prompts.

Extract:
- Business goal and demo goal.
- Target users and roles.
- Industry terminology such as FA, SA, BA, advisor, or client-specific role names.
- Customer/member field vocabulary, including identifier, contact, grouping, level, profile label, and lifecycle labels.
- Channels and systems involved.
- Business objects and states.
- Core journeys and edge cases.
- Must-have vs optional modules.
- Prototype format and expected fidelity.
- WeCom mini-program/container constraints.
- Native WeCom page replicas such as 新建群发 when communication execution leaves the clienteling page.
- Prototype presentation requirements: desktop stage, mobile full-screen, role switching, free browse, preset journeys.
- Reusable interaction details: search, filter, sort, tabs, page states, disabled reasons, and result states.
- Task execution details: source, type, target grain, execution channel, native handoff, and completion evidence.
- Visual fidelity, brand references, and design constraints.

If little source material exists, switch to baseline framework mode and read `references/baseline-framework.md` plus `references/reference-page-blueprints.md`.

If the user requests research, collect only the research dimensions needed for the output and use current public sources before treating brand/category facts as context.

## 2. Capability Decomposition

Map source material to:
- Core WeCom Clienteling capabilities.
- Advanced conditional capabilities only when triggered and confirmed.
- Extension capabilities.
- Shared objects such as customer, contact, task, appointment, content, owner, store, member profile, and opportunity only if confirmed.
- Shared states such as registered/unregistered, bound/unbound, active/inactive, pending/completed, sent/failed.

Output: capability map and unresolved questions.

Before writing UI labels, read `references/terminology.md` and map field vocabulary. If the user has no field preference, use neutral generic labels instead of project-specific identifiers.

## 3. Flow Modeling

For each important flow, capture:
- Actor.
- Trigger.
- Entry point.
- Customer/contact state.
- System/source state.
- Key action.
- Result.
- Exception/recovery path.
- Metrics or evidence.

Output: flow matrix.

## 4. IA And Page Inventory

Convert flows into a page map:
- Top-level tabs or entry points.
- Cross-module tools.
- Page groups by business capability.
- Detail pages and modals.
- Shared components and global states.
- Role-specific variations.

Assign page depth:
- **A / full detail**: required for primary demo flows and business decisions.
- **B / structural**: enough content to prove IA, state, and flow, but not full interaction.
- **C / skeleton**: navigation placeholder, future scope, or low-priority supporting page.

Output: page inventory with depth, source, data, and acceptance notes.

Read `references/interaction-patterns.md` for reusable search/filter/sort/tab/page-state rules.
Read `references/reference-page-blueprints.md` when source material does not define page-level detail.

## 4A. Task Execution Model

When tasks are in scope, define:
- Task source.
- Task type.
- Target grain.
- Execution channel.
- Native WeCom handoff if needed.
- Completion feedback.
- Metrics and result state.

Read `references/task-execution-patterns.md`.

## 5. WeCom And Presentation Constraints

Before briefing or building a prototype, define:
- WeCom contact, identity, and mini-program card assumptions.
- Native WeCom page replication needs, including 新建群发 or send/broadcast handoff.
- Native/container navigation constraints.
- Role and permission show/hide rules.
- Desktop review stage vs mobile full-screen behavior.
- Stage controls, free browse, preset journeys, and URL parameters.

Read `references/wecom-mini-program-constraints.md`, `references/wecom-native-page-replication.md` when relevant, `references/prototype-shell-contract.md` for HTML/clickable prototypes, and `references/prototype-presentation-spec.md`.

Output: channel and presentation spec.

## 6. Visual Direction

Before writing a visual prototype brief, define:
- Industry and role naming.
- Style direction.
- Reference sources and missing assets.
- Density and tone.
- Brand constraints and generic placeholder rules.
- Component conventions for operational screens.

Read `references/terminology.md` and `references/visual-design-reference.md`.

Output: visual direction note.

## 7. Prototype Brief

Write an execution brief that contains:
- Objective.
- In/out scope.
- Required demo flows.
- Page inventory and depth.
- Data model and sample data.
- Baseline sample-data depth and cross-page data links when source data is sparse.
- Field vocabulary mapping.
- WeCom mini-program constraints.
- Native WeCom page replicas and return states.
- Interaction standards for search, filter, sort, tabs, page states, and disabled actions.
- Task execution model for list, detail, target handling, channel, and completion feedback.
- Prototype presentation modes and controls.
- Visual references.
- Style direction and role naming.
- Interaction requirements.
- Language and terminology rules.
- Acceptance checklist.

Use `assets/templates/prototype-brief-template.md`.

## 8. Prototype Production

When implementing:
- For HTML/clickable prototypes, copy `assets/prototype-shell/index.html` first or port its shell into the chosen framework.
- Build the actual usable experience first, not a marketing page.
- Preserve business density and operational scanning.
- Use realistic sample data, states, role-specific content, and cross-page links. A task target, customer card, C360 view, appointment, and content asset should not contradict each other.
- Keep navigation and flow traceable to the page inventory.
- Make extension modules visible only if they are in scope.
- Implement WeCom mini-program/container constraints before adding decorative UI.
- Preserve the shell's WeCom title bar, capsule, page body, bottom tabbar, desktop review frame, mobile full-screen behavior, role controls, and journey controls.
- Implement reusable search, filter, sort, tab, page-state, and disabled-action behavior consistently across A-level pages.
- Implement task execution by type and channel, not as a generic static task page.
- Avoid repeated same-layout pages with only text swaps. Home, customer list, C360, task list/detail, appointment, content, and dashboard need distinct structure, data fields, and actions.
- Implement native WeCom replicas, such as 新建群发, when the flow requires native send/broadcast behavior.
- Implement desktop review stage and mobile full-screen behavior when the output is an HTML/clickable review prototype.
- Do not expose mobile/desktop switching as a visible selector. Use responsive detection and optional URL parameters for QA.
- Keep review controls outside the production app UI and hide them in mobile full-screen mode.
- Support free browse and preset journey mode when an interactive review prototype is requested.
- Use SVG icons or an approved icon library instead of emoji.
- Apply the chosen visual direction consistently; do not default to FA/SA/BA naming without industry confirmation.
- Run `python3 scripts/check_prototype_shell.py path/to/index.html` before final review.

## 9. Coverage QA

Validate:
- Every A-level page maps to at least one required flow.
- Every required flow has start, action, result, and exception handling.
- Every role/permission difference is visible or explicitly deferred.
- Every integration has source system, visible state, action, and write-back/result.
- WeCom contact, mini-program card, and permission constraints are represented.
- Native WeCom page replicas are included or explicitly deferred.
- Search, filter, sort, tabs, page states, and disabled-action reasons are standardized where they appear.
- Task execution distinguishes source, type, target, channel, native handoff, completion feedback, and metrics.
- Desktop/mobile presentation behavior and stage control visibility are verified.
- Static shell QA passes, and mobile full-screen is visually verified as nonblank.
- Role switching, free browsing, and preset journeys work as scoped.
- Prototype language matches the client's terminology.
- Visual style matches the industry, fidelity target, and available references.

Use `references/qa-rubric.md`.

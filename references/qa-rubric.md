# Prototype QA Rubric

Use this to review prototype coverage and readiness.

## Coverage Checks

- The deliverable assumes a WeCom ecosystem mini-program clienteling tool unless another channel is explicitly specified.
- Each in-scope capability has at least one page, flow, or explicit deferral.
- Each primary demo flow has an entry, action path, result, and exception state.
- Each A-level page is traceable to a business requirement or demo goal.
- Opportunity follow-up is included only when priority-customer/opportunity lifecycle scope is confirmed.
- Each extension integration states source system, signal/state, frontline advisor action, and result/write-back.
- Each role difference is represented or listed as an assumption.
- Industry role naming such as FA, SA, BA, advisor, or consultant is confirmed or flagged as an assumption.
- FA/SA/BA is not exposed as a runtime selector inside the prototype. It is fixed by industry or confirmed during intake.
- Customer/member field vocabulary is confirmed or uses neutral generic labels rather than project-specific identifiers.
- Reusable interaction standards are documented for search, filter, sort, tabs, page states, and disabled actions where they appear.
- Task execution standards are documented for source, type, target grain, execution channel, native handoff, completion feedback, and metrics.
- The selected start mode is clear: source-backed, research-led, baseline, or hybrid.
- When public research informs the prototype, researched facts are separated from assumptions and generic defaults.

## Business Logic Checks

- Registered/unregistered, bound/unbound, owner/supporting advisor, and store/region visibility are clear where relevant.
- WeCom contact states drive contact, send, invite, and mini-program card actions.
- Native WeCom send/broadcast pages are replicated when the flow leaves the clienteling mini-program.
- Task, appointment, content, transfer, and confirmed opportunity states have realistic transitions.
- 1v1, 1vN, Moments, native broadcast, appointment, content, and offline task patterns are not collapsed into one generic task detail when their execution differs.
- Customer actions and system actions are not mixed without explanation.
- Frequency control, consent, privacy, or customer agreement requirements are surfaced when material implies them.
- Failure paths are present for binding, sending, resource conflict, transfer, and external integration data.

## Prototype Quality Checks

- HTML/clickable prototypes start from `assets/prototype-shell/index.html` or directly port its shell structure and behavior.
- `scripts/check_prototype_shell.py` passes for generated HTML.
- For branded HTML/clickable prototypes, `scripts/check_workbench_implementation.py` passes so token-level workbench balance is visible in the implemented pages.
- Navigation matches the page inventory.
- Page depth matches A/B/C commitments.
- Sample data demonstrates real decisions, not filler.
- Baseline sample data is connected across pages: customer list, C360, task target list, appointment records, content assets, and dashboard drilldowns do not contradict each other.
- Home, customer list, C360, task list/detail, appointment, content, and dashboard use distinct structures and field sets when they are in scope.
- Repeated cards are not used as the main structure for every module.
- Manager/HQ dashboard pages include period control, role/scope copy, grouped KPI modules, progress or target attainment, supporting values, and a by-frontline-role performance entry.
- By-frontline-role performance pages include a selector or tabs for visible team members plus sales/contribution, customer operation, appointment/service, task execution, and WeCom connection sections.
- Dashboard terminology uses the confirmed frontline role term. It should not hard-code FA, SA, BA, advisor, or 店员 when the user's industry calls for another term.
- Operational screens are dense enough for work but still scannable.
- Home metrics have visible labels, units where relevant, period/scope, and drilldowns. No KPI is rendered as a bare number or explained only by position/color.
- HTML metric labels use `data-metric-label`, and A-level detail coverage uses truthful `data-info-capability` markers for deterministic QA.
- Home has at least two real `data-home-kpi` containers and two `data-home-operational` regions; a countdown or campaign card is not counted as either.
- No more than one campaign/editorial/brand storytelling region appears before the first home operational region.
- A-level detail pages cover the capability vocabulary from `page-information-contract.md`; layout, grouping, ordering, and interaction remain adaptable.
- The visual token includes structural differentiation for navigation, home, C360, tasks, appointments, dashboard, and a signature interaction.
- Navigation set/order and at least two page architectures are justified by brand, role, industry, or journey evidence rather than copied from the starter shell.
- Implemented navigation labels/order match the visual token, and declared architecture/signature IDs exist on visible HTML.
- When prior cases are available, structural similarity checks reject prefix/color/copy-only variants.
- The token declares `reference-led`, `evidence-derived`, or `open-generative` layout authority and the rendered prototype matches it.
- Open-generative work records at least three candidate directions, a scored selection rationale, and rejected alternatives.
- Structure validation is brand-agnostic. Passing does not depend on a known brand name or brand-prefixed CSS class.
- `user-confirmed` evidence is traceable to an actual user source; inferred or public facts are not relabeled as confirmation.
- Navigation, business axis, home narrative, module grammars, page architectures, and signature interaction form one coherent operating story.
- Shared customer, task, appointment, and asset objects are connected by ID. Counts, states, owners, dates, and names do not conflict across pages.
- Product UI does not expose QA/debug copy such as brand intensity, workbench density, accent budget, token names, or implementation notes.
- Mini-program top titles remain readable and untruncated; longer English branding moves into the page body.
- Secondary, disabled, and outline buttons have visible labels with sufficient foreground/background contrast.
- Metric labels are visibly rendered at the target viewport; CSS clipping, low contrast, overlap, or hidden overflow do not erase field semantics.
- A-level C360 pages expose at least four distinct regions across identity/relationship, value/recency, operating context, customer knowledge, history, and actions.
- A-level task detail pages expose at least five distinct regions across definition, progress, audience, guidance/assets, result capture, and channel-specific execution.
- A-level appointment detail pages expose at least five distinct regions across schedule, people/place, service/resource, customer context, preparation/communication, outcome/follow-up, and actions/exceptions.
- Detail-page density comes from decision-supporting dimensions, not repeated cards, decorative labels, or generic filler.
- Chinese/English terminology matches the client source material.
- Search placeholders, filters, C360 fields, sample data, dashboard dimensions, and task-targeting labels use the confirmed field vocabulary.
- Visual direction matches the industry, prototype fidelity, and available reference sources.
- High-fidelity branded prototypes include a compact evidence table and brand visual token before implementation.
- Brand visual token decisions are applied through page-layer CSS variables and component rules, not by rebuilding the protected shell.
- If a JSON visual token is produced, `scripts/check_visual_tokens.py` passes.
- Brand references are traceable to user-provided materials, public sources, design-reference search, style templates, or explicit assumptions.
- Branded business terminology is recorded in an evidence ledger. Internal-sounding segments, programs, rooms, task types, and workflows are user-confirmed or replaced with neutral defaults.
- Assumption claims do not appear in delivered UI.
- Public marketing sources are not used as proof of internal CRM/customer tiers or advisor workflows.
- Prior-case brand names, campaigns, products, roles, segments, and content assets are absent.
- Brand skin does not alter native WeCom replica structure, mini-program top geometry, bottom tabs, role/journey controls, or sticky CTA anchoring.
- Brand depth is present beyond palette changes: typography hierarchy, geometry, accent rule, and visual anchors are defined and visible where appropriate.
- Workbench balance is explicit: brand intensity, hero policy, operational priority, accent budget, module differentiation, page-layer-only rule, and readability rules are documented.
- Workbench balance is implemented: home first viewport shows at least two workbench signals, customer list shows search/filter, task list shows type/status controls and next actions, appointments show time/customer/service/status/action, dashboard shows metric/target/drilldown, and native WeCom handoff stays operational.
- Expressive brand moments do not compete with search, filters, task due dates, target counts, appointment time/resource rows, dashboard drilldowns, or native WeCom handoff.
- Strong brand color or high-contrast modules are limited by an accent budget and do not flood every card, chip, tab, or CTA.
- Home, customer list, C360, task list/detail, appointment, content, dashboard, and transfer pages are visually adapted to their jobs, not only recolored from one repeated pattern.
- Quiet brands still have recognizable anchors through typography, spacing, imagery discipline, material/detail rhythm, or component shape.
- Empty, loading, error, no-permission, and success states are covered for high-risk actions.
- Search and filter states include no result, cleared query, selected filters, role-limited filters, and source failures when relevant.
- Tabs, segmented controls, status filters, and filter chips are used consistently according to hierarchy.
- Mini-program navigation, safe areas, bottom-tab visibility, and sticky action bars match the page depth and flow.
- The WeCom mini-program shell is present on every custom app page: title bar, capsule/safe area, body container, and correct top-level tabbar.
- Native WeCom replicas, such as 新建群发, hide clienteling bottom navigation and unrelated app tools.
- Native replicas carry recipient count, message copy, attachment, frequency/compliance note, send/cancel path, and return-to-business result state.
- Desktop review stage and mobile full-screen behavior are both verified when the prototype is HTML/clickable.
- Desktop review stage shows a complete 390px by 844px mini-program frame with iPhone-style notch, scaled to fit; top bar and bottom tabbar are not cropped.
- Desktop top shell has separated status and nav rows: `9:41` and `5G` sit in the status row, while the page title and WeCom capsule are centered in the nav row below it with no crowding.
- Desktop review controls are compact and outside the phone, not a large rough control panel inside or around the app.
- Desktop/mobile behavior is code-level responsive or URL-driven for QA, not a visible selector.
- `scripts/check_page_information.py` passes for prototypes containing home metrics or A-level detail pages.
- Mobile full-screen mode is nonblank, hides decorative phone hardware such as notch/statusbar, and does not hide the phone/screen/body container.
- Stage controls are hidden in mobile full-screen mode and separated from production app UI.
- Role switching changes permissions, data scope, and available tools.
- Role switching does not change the industry frontline term. It changes business roles only, such as frontline vs manager.
- Free browse and preset journey modes both work when scoped.
- Journey mode controls role when the journey requires a role-specific path.
- Emoji are absent from tabbars, quick entries, task cards, page states, and placeholder illustrations.
- Brand color is used as an accent unless the user provides a full design system.
- A baseline visual style stays neutral and operational unless brand or industry references are confirmed.

## Output Checks

- Deliverables include assumptions and open questions.
- The prototype brief can be handed to a designer or frontend builder without reinterpreting the business.
- QA findings are prioritized by business risk, not only visual polish.
- Project-specific modules are not mislabeled as generic WeCom Clienteling capabilities.
- Project-specific field names are not used as generic defaults.
- Generic visual templates are adapted to the client's industry rather than copied blindly.
- Prototype shell requirements are explicit enough for a frontend builder to reproduce the review experience.

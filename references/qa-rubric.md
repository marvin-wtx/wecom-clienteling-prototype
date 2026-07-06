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
- Customer/member field vocabulary is confirmed or uses neutral generic labels rather than project-specific identifiers.
- Reusable interaction standards are documented for search, filter, sort, tabs, page states, and disabled actions where they appear.
- Task execution standards are documented for source, type, target grain, execution channel, native handoff, completion feedback, and metrics.

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
- Navigation matches the page inventory.
- Page depth matches A/B/C commitments.
- Sample data demonstrates real decisions, not filler.
- Operational screens are dense enough for work but still scannable.
- Chinese/English terminology matches the client source material.
- Search placeholders, filters, C360 fields, sample data, dashboard dimensions, and task-targeting labels use the confirmed field vocabulary.
- Visual direction matches the industry, prototype fidelity, and available reference sources.
- Empty, loading, error, no-permission, and success states are covered for high-risk actions.
- Search and filter states include no result, cleared query, selected filters, role-limited filters, and source failures when relevant.
- Tabs, segmented controls, status filters, and filter chips are used consistently according to hierarchy.
- Mini-program navigation, safe areas, bottom-tab visibility, and sticky action bars match the page depth and flow.
- The WeCom mini-program shell is present on every custom app page: title bar, capsule/safe area, body container, and correct top-level tabbar.
- Native WeCom replicas, such as 新建群发, hide clienteling bottom navigation and unrelated app tools.
- Native replicas carry recipient count, message copy, attachment, frequency/compliance note, send/cancel path, and return-to-business result state.
- Desktop review stage and mobile full-screen behavior are both verified when the prototype is HTML/clickable.
- Desktop/mobile behavior is code-level responsive or URL-driven for QA, not a visible selector.
- Mobile full-screen mode is nonblank and does not hide the phone/screen/body container.
- Stage controls are hidden in mobile full-screen mode and separated from production app UI.
- Role switching changes permissions, data scope, and available tools.
- Free browse and preset journey modes both work when scoped.
- Journey mode controls role when the journey requires a role-specific path.
- Emoji are absent from tabbars, quick entries, task cards, page states, and placeholder illustrations.
- Brand color is used as an accent unless the user provides a full design system.

## Output Checks

- Deliverables include assumptions and open questions.
- The prototype brief can be handed to a designer or frontend builder without reinterpreting the business.
- QA findings are prioritized by business risk, not only visual polish.
- Project-specific modules are not mislabeled as generic WeCom Clienteling capabilities.
- Project-specific field names are not used as generic defaults.
- Generic visual templates are adapted to the client's industry rather than copied blindly.
- Prototype shell requirements are explicit enough for a frontend builder to reproduce the review experience.

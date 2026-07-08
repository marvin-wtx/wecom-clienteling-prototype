# Page Information Contract

Use this contract when producing or reviewing full-detail prototype pages. It prevents visually polished prototypes from collapsing into unlabeled numbers, generic summary cards, or thin secondary pages.

## Core Rule

Every full-detail page must answer four questions without requiring the reviewer to infer them:

1. **What object is this?**
2. **Why does it matter now?**
3. **What context supports the decision?**
4. **What can the user do, and what result will be recorded?**

Do not increase density by adding decorative cards or repeating the same field in multiple forms. Add distinct decision-supporting dimensions.

## Field Semantics

Every value must have a visible field label, unit where relevant, and scope or period when ambiguity is possible.

- Never show a KPI as a bare number. Pair it with a visible label such as `今日任务`, `待确认预约`, or `优先客户`.
- For rates and progress, show numerator/denominator or target context when available, such as `6/18 已触达` or `72% / 目标 80%`.
- For money, counts, dates, and times, make units and periods explicit.
- Do not rely on color, position, placeholder copy, or source-code order to explain a value.
- Ensure metric labels remain visible at the rendered viewport. Check contrast, font size, overflow, and stacking.
- In HTML, put `data-metric-label` on the visible label element. Do not place it on a hidden accessibility-only duplicate.

## Page Depth

Classify pages before implementation:

- **A-level full detail**: supports review and action. Use the full contracts below.
- **B-level structural**: shows credible structure and the primary interaction, with explicit deferred areas.
- **C-level navigation/skeleton**: proves routing only and must not be presented as complete.

Brand fidelity does not lower page-depth requirements. A-level pages must not become B-level pages to preserve whitespace or an editorial mood.

For HTML prototypes, mark each distinct A-level region with `data-info-region="<region-name>"`. Use one marker per meaningful region; do not add markers to wrappers or duplicate the same content to satisfy QA.

## Home Workbench Contract

The first viewport should contain:

- Identity/scope: role, store/team, and current date or period.
- Two or three KPI items with visible labels, values, period/scope, and tap target.
- At least two operational signals: priority customers, tasks, appointments, exceptions, or campaign-to-task entry.
- A clear relationship between each KPI and its drilldown.

Reject:

- Bare numbers without labels.
- A campaign hero that pushes operational signals below the first viewport.
- Metrics whose labels disappear because of CSS, clipping, low contrast, or overlap.

## Customer C360 Contract

Use distinct regions rather than one summary card:

1. **Identity and relationship**: customer identity, owner/store, contact and registration state, member/value level, lifecycle/profile labels.
2. **Value and recency**: purchase/contribution summary, transaction count or recency, last interaction, data timestamp where useful.
3. **Current operating context**: active task, appointment/service status, opportunity/reason signal when in scope, next best action, due time.
4. **Customer knowledge**: preferences, sizes or product interests, wishlist/interests, notes, consent/contact restrictions when relevant.
5. **History**: transactions, interactions, tasks, appointments/services, and notes through tabs, timeline, or grouped sections.
6. **Action layer**: WeCom contact, task, appointment, content, note, invite/register, or transfer actions according to permissions and state.

At least four of the six regions must be visible or directly reachable on an A-level C360 page. A single profile card plus a three-row timeline is not sufficient.

## Task Detail Contract

Use these regions:

1. **Definition**: goal, source, type, priority, owner, due time, target grain, success metric.
2. **Execution progress**: numerator/denominator, pending/completed/skipped/failed states, exception count.
3. **Audience**: target segment or customer list with per-target contact state, result state, and next action when target grain is individual.
4. **Guidance and assets**: editable talking points, asset preview, source, readiness, validity, and usage constraints.
5. **Result capture**: result options appropriate to the channel, notes, reason, next follow-up date, and write-back state.
6. **Execution action**: channel-specific primary action and disabled reason or recovery path.

Do not use generic copy such as `根据客户状态生成` or `1 个素材已就绪` as the only evidence. Show enough preview and metadata for the user to decide whether execution is appropriate.

## Appointment Detail Contract

Use these regions:

1. **Schedule**: date, start/end time, timezone if relevant, status, confirmation state.
2. **People and place**: customer, owner, support role, store/location.
3. **Service and resource**: service type, resource or room, product/size preparation, capacity or conflict state.
4. **Customer context**: preferences, purpose, linked task/campaign, recent interaction, contact restrictions.
5. **Preparation and communication**: checklist, notes, confirmation channel, last confirmation time.
6. **Outcome and follow-up**: arrival/completion/no-show/cancel state, result note, contribution or conversion where relevant, next action.
7. **Actions and exceptions**: confirm, reschedule, cancel, contact, check in, complete, record result, plus conflict or permission recovery.

At least five regions must be visible or directly reachable on an A-level appointment detail. A key-value card with customer, time, owner, status, and note is only a B-level structure.

## Visual Density And Hierarchy

- Prefer section bands, tabs, compact key-value grids, timelines, checklists, and action rows over stacking large cards.
- Use cards only for real objects or grouped tools; do not put every section in a floating card.
- Keep the primary decision and action visible while allowing the body to scroll.
- Use progressive disclosure for long history, but keep summaries and counts visible.
- Distinguish overview, evidence, execution, and history through hierarchy, not only border boxes.

## Acceptance

Before delivery:

- Read every number aloud with its visible label, unit, period, and scope.
- Verify that each A-level detail page has the required number of distinct information regions.
- Confirm that fields support a decision or action rather than merely filling space.
- Verify each primary action has a result state and each blocked action has a reason or recovery path.
- Check the rendered page in the user-facing viewport; source-code presence alone does not prove visibility.

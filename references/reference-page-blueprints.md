# Reference Page Blueprints

Use these blueprints when building a baseline or when source material is too thin to specify page-level behavior. They are generic WeCom Clienteling patterns derived from a working reference implementation, but they must remain project-neutral.

Do not copy client-specific names, proprietary field labels, real customer data, or unique member-system concepts into generic work. If the user has no vocabulary preference, use neutral labels such as customer ID, member level, customer profile, lifecycle state, interaction history, owner, store, task source, and content asset.

## Baseline Data Standard

A prototype is not credible if every page is the same card layout with decorative labels. Even in baseline mode, create a small connected data model:

- **Roles**: at least frontline advisor plus manager/supervisor when role switching is in scope.
- **Customers**: at least 6 customers with different ownership, contact, registration, member level, profile label, lifecycle state, preference, last purchase, last interaction, and next action.
- **WeCom-only contacts**: at least 2 contacts that are added in WeCom but not yet matched or registered.
- **Tasks**: at least 5 tasks covering 1v1, 1vN, native broadcast or Moments when relevant, appointment/service follow-up, and offline/result recording.
- **Appointments**: 6-8 records across pending, confirmed, arrived, completed, canceled, and conflict states when appointment is in scope.
- **Content assets**: at least 3 assets with type, source, readiness, validity, usage scope, and task linkage.
- **Metrics**: at least 4 metric groups with denominator, period, owner scope, and drilldown path.
- **Management metrics**: when manager/HQ roles are in scope, include grouped KPI data plus by-frontline-role rows. Each row should have at least one progress metric, one activity metric, and one exception or pending metric.
- **Cross-links**: tasks target real sample customers, appointments reference real sample customers, C360 shows the same states as the list, and task materials reference content assets.

Each record needs a reason and next action. Avoid generic filler such as "客户A", "示例任务", or identical repeated cards.

## Desktop Review Shell

For HTML prototypes, the desktop surface is a review console around a mobile mini-program, not a desktop product.

Required layout:
- Phone viewport: 390px wide by 844px high before scaling.
- Phone stays fully visible on desktop through code-level scale; do not crop the bottom tabbar or top frame.
- Desktop phone frame includes an iPhone-style notch; keep it visible in desktop review mode.
- Top shell uses protected mini-program spacing: 38px status bar, compact centered notch, nav title centered in the row below the status bar, and the 88px by 32px WeCom capsule aligned to that nav row.
- Status bar copy is only `9:41` and `5G`; do not add signal-dot placeholders or crowd the nav title into the status row.
- Desktop header and controls are outside the phone, centered, compact, and no wider than about 920px.
- Controls are small operational review controls: role selector, journey selector, entry buttons, reset when needed.
- Review controls are hidden in mobile full-screen mode.
- Mobile mode fills the viewport with the mini-program screen and has no visible desktop frame.
- Mobile mode hides decorative phone hardware such as the border, notch, and statusbar.
- Do not expose a visible mobile/desktop selector. Use responsive behavior and optional QA URL parameters.
- Use a WeCom-style top bar, title truncation, right capsule, body scroll area, and bottom tabbar.
- Native WeCom replicas hide the custom tabbar and use native-style visual language.

Neutral starter tabs:
- Home.
- Customers.
- Center quick-action entry.
- Tasks.
- Appointments.

This is not a required order. Choose 3-5 top-level items from journey frequency, role, industry, and demo goals. Dashboard, content, opportunity, service queue, or another module may replace a starter tab. Native broadcast remains a handoff, not a branded top-level destination.

## Home Workbench

Purpose: daily operating entry for frontline work.

Page content:
- Advisor identity, role label, store/team, date or business period.
- Two or three compact metric cards, usually task progress, appointment/service progress, and business contribution. Every value needs a visible label, period/scope, and drilldown; rates should show denominator or target context when available.
- Today appointment/service queue with status, time, customer, resource or owner, and missing action.
- Today task list with type, priority, source, target count, progress, due time, and next action.
- Quick entries for customers, tasks, appointment, content, dashboard, and native send when in scope.

Interactions:
- Tap a metric to drill into dashboard or related list.
- Tap a customer row to C360.
- Tap a task to task detail.
- Tap appointment to appointment detail or create flow.
- Role switch changes visible metrics, scope, and quick entries.

States:
- No tasks today.
- Tasks overdue.
- Appointment conflict.
- Customer cannot be contacted because WeCom contact state is missing.

## Customer List And C360

Purpose: find customers, understand context, and act from customer state.

Customer list content:
- Search with field selector or clear placeholder: name, contact method, customer ID, member ID, WeCom nickname, or tag.
- Scope tabs: my customers, store/team customers, other advisor customers, WeCom-only contacts, or project-defined scopes.
- Sort controls: recent purchase, recent interaction, customer priority, member level, lifecycle state, or owner.
- Filter groups: ownership, member level, profile label, lifecycle, WeCom contact state, registration state, task state, appointment state.
- Count summary and selected filter chips.
- Customer cards with name, owner/scope, member level, profile label, lifecycle state, contact/registration state, recent purchase, recent interaction, current task, and next best action.

C360 content:
- Header with customer identity, owner, contact/registration state, member level, profile labels, and disabled-action reason if needed.
- Trade or value summary when available.
- Current todo and appointment/service status.
- Detail tabs: profile, transactions, interactions, preferences, wishlist/interests, notes, tasks, appointment/service history.
- Sticky actions: send WeCom message, invite/register, create task, create appointment, share content, add note, or transfer depending on role and state.
- For A-level fidelity, organize the page into at least four distinct regions from identity/relationship, value/recency, current operating context, customer knowledge, history, and action layer. Do not treat one summary card plus a short timeline as complete.

Interactions:
- Local search and exact/global lookup are separate when identifiers are in scope.
- Opening a WeCom-only contact should show match/register actions, not a full known-customer profile.
- Disabled actions explain the missing condition.
- Manager scope can show read-only or transfer actions where frontline scope cannot.

## Task Execution

Purpose: turn assigned or recommended work into traceable customer actions.

Task list content:
- Task completion overview with denominator and period.
- Status filters: pending, in progress, completed, skipped, expired.
- Type filters: 1v1, 1vN, Moments, native broadcast, appointment, content share, data completion, offline follow-up.
- Cards with source, priority, target count, channel, content readiness, due time, progress, and next action.

Task detail content:
- Task goal, source, type, audience, due time, owner, and success metric.
- Recommended copy or talking points.
- Required materials and readiness state.
- Target customer list with per-customer contact state, result state, and next action.
- Execution action: open WeCom chat, enter native broadcast, share content, publish Moments, create appointment, record offline result, complete/skip.
- Result capture: sent, replied, no response, appointment created, declined, skipped reason, next follow-up date.
- For A-level fidelity, expose at least five distinct regions from definition, execution progress, audience, guidance/assets, result capture, and execution action.

Execution rules:
- 1v1 sends from one customer context and records per-customer outcome.
- 1vN has target list progress and per-customer status.
- Moments has publish content and post-publish recording, not recipient-level send status.
- Native broadcast enters a separate native page replica.
- Appointment/service tasks should link to appointment creation or detail.
- Offline tasks require result and note capture.

## Appointment Or Service

Purpose: schedule, confirm, and record customer service moments.

Pages:
- Calendar/list by day, advisor, store, or resource.
- Appointment detail with customer, time, store, service/resource, owner, support role, status, and preparation.
- Create/edit wizard: select customer, service/resource, time, owner/support, notes, and confirmation channel.
- Confirmation/success state.
- Completion capture: arrived, completed, no-show, canceled, result note, next follow-up.
- For A-level appointment detail, expose at least five distinct regions from schedule, people/place, service/resource, customer context, preparation/communication, outcome/follow-up, and actions/exceptions.

Interactions:
- Conflict detection for time/resource.
- Pending online allocation or approval when applicable.
- Reschedule/cancel with reason.
- Appointment card links back to C360 and task detail.

## Content Library

Purpose: find approved assets for customer communication.

Pages:
- Library home with source tabs such as HQ, store/team, recent, or favorites.
- Folder/category grid.
- Search and type filters: image, text, link, product card, mini-program card, video, article, event invite.
- Asset list with title, source, validity, readiness, usage scope, and linked campaign/task.
- Preview with copy, attachment, share constraints, and task/customer context.

Interactions:
- Preview before send.
- Attach to task execution.
- Copy talking point or select asset for native send.
- Disabled state for expired, unapproved, or role-limited content.

## Dashboard And Tracking

Purpose: make clienteling performance reviewable.

Frontline view:
- Personal task completion.
- Customer touch reach and response.
- Appointment/service conversion.
- Content usage.
- Customer growth or activation.

Manager view:
- Store/team/region overview with role scope and business period.
- Grouped KPI modules, not only summary numbers. Default groups: sales or contribution, customer operation, appointment/service conversion, task execution, and WeCom connection.
- Progress or target attainment for each major group, plus supporting values and denominators.
- Advisor/frontline performance preview with ranking or workload signals.
- Customer ownership and transfer status.
- Task/campaign performance by source and type.
- WeCom add/bind/register funnel when in scope.
- Drilldown page for by-frontline-role performance.

Interactions:
- Period, store/team/region, advisor/frontline person, and task-source filters.
- Drilldown from metric to customer/task/appointment list.
- No-permission state for manager-only metrics.

Management dashboard page structure:
- Header: role scope, data scope, period label, and latest data timestamp.
- Period selector: today, week, month, year or the source-defined reporting periods.
- KPI group cards: each card combines a progress ring or progress bar, 2-3 supporting rows, and optional small paired metrics.
- Frontline performance entry: list or CTA leading to by-frontline-role performance detail.

By-frontline-role performance detail:
- Frontline person tabs or selector scoped to the manager's visible team.
- Identity row with person, store/team, reporting period, and role term.
- Sales/contribution area: target attainment, sales or contribution value, transaction count, average basket/order value, UPT/SPT or equivalent only if relevant.
- Customer operation area: acquisition, activation, retention/returning, profile completion, contact/bind rate, or the user's confirmed customer metrics.
- Appointment/service area: attended/completed count, conversion, contribution, and pending service items.
- Task and WeCom operation area: completed/pending task counts, skipped/overdue if relevant, contact adds/binds, outreach, response, deletion/loss, and write-back status.
- Avoid project-specific field labels unless provided. Use neutral labels such as customer operation, member level, profile label, lifecycle state, customer connection, and frontline role.

## Transfer And Ownership

Purpose: govern customer/contact ownership changes.

Pages:
- Transfer entry with reason, source advisor, target advisor, scope, and count.
- Candidate customer list with filters and risk markers.
- Receiving advisor selection.
- Confirmation with impact summary.
- Result with success/failure details and retry path.

Interactions:
- Bulk selection.
- Read-only preview before confirmation.
- Failure reasons such as permission, already transferred, customer locked, or data conflict.

This module is usually manager-only and can remain structural unless the user asks for full governance flows.

## Settings, Role, And Permissions

Purpose: explain prototype role logic without turning settings into the main product.

Content:
- Current role, store/team, data scope, and visible tools.
- Permission explanations for hidden/disabled actions.
- Optional prototype-only role switch in desktop review controls, not inside the production mini-program.

States:
- No permission.
- Role has read-only access.
- Role can act only on owned customers.

## Native WeCom Replicas

Use a native page replica when the business action leaves the mini-program and enters WeCom native behavior.

For native broadcast or 新建群发-like flows, include:
- Recipient entry and recipient count.
- Message/content editing.
- Attachment or mini-program card selection.
- Frequency/compliance note when relevant.
- Preview/send/cancel.
- Return-to-business result state, such as sent, failed, frequency-limited, or partially completed.

Do not make native pages look like branded clienteling pages. They should be visibly separated from custom mini-program screens.

## Baseline Acceptance

Before delivering a baseline prototype or brief, verify:

- Every A-level module has a distinct page layout, not only a repeated card list.
- Every important page has business object, state, action, and result.
- Every visible number has a field label, unit where relevant, and period/scope when ambiguous.
- A-level C360, task detail, and appointment detail pages satisfy `page-information-contract.md`; thin summary-card pages are explicitly marked B-level instead of presented as complete.
- Sample data is connected across pages.
- Search/filter/sort/tab controls are meaningful and mapped to real fields.
- Task execution differs by channel and target grain.
- Appointment, content, dashboard, and transfer are either scoped with concrete behavior or explicitly marked structural.
- The desktop review shell shows the full phone frame and compact controls.
- Mobile mode is automatic full-screen and nonblank.
- No emoji appear in tabbar, quick actions, task markers, or placeholder illustrations.

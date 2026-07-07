# Module To Page Patterns

Use these patterns when converting modules into IA, page inventory, and prototype screens.

For reusable search, filter, sort, tab, and page-state behavior, read `interaction-patterns.md`. For task execution detail, read `task-execution-patterns.md`. When the source does not define page-level detail, read `reference-page-blueprints.md`.

## Common App Frame

Typical mobile workbench structure:
- Home/workbench: daily summary, priority tasks, key metrics, alerts.
- Clients: client list, search/filter, C360.
- Tasks: assigned work and follow-up.
- Appointment/invitation: calendar, list, create flow, result.
- Center quick-action entry or tools page: content, dashboard, transfer, settings, extension modules.
- Advanced opportunity: add only when priority-customer or opportunity lifecycle is confirmed.

Adjust labels to the user's context. Some projects may use bottom navigation; others may use enterprise app tabs, mini-program pages, desktop dashboards, or embedded WebViews.

## Page Patterns By Module

### Add And Binding

Minimum pages:
- Add/bind entry or status.
- Customer/prospect match result.
- Registration invitation.
- Success/failure state.

Key interactions:
- Copy/send invite.
- Confirm binding.
- Resolve duplicate/ambiguous match.
- View what is unlocked after binding.

### Client And C360

Minimum pages:
- Client list.
- Search and filter.
- C360 overview.
- Transaction/interaction/wishlist/detail drilldowns as needed.

Key interactions:
- Search, sort, filter, save filter.
- Open customer detail.
- Add note/tag.
- Start task, content send, appointment, or contact action.

Standardization:
- Treat search/filter/sort/tabs as shared interaction layers, not one-off pages.
- Include role and ownership effects in search results and disabled actions.
- Show no-result, no-permission, and source-failure states when they affect contact actions.

### Task

Minimum pages:
- Task list or home task card.
- Task detail.
- Execution target list if 1vN.
- Completion/result feedback.

Key interactions:
- Start execution.
- Select customer/target.
- Complete, skip, fail, or record no response.
- View task reason and recommended action.

Standardization:
- Distinguish task source, task type, target grain, execution channel, and completion evidence.
- Support 1v1, 1vN, Moments, native broadcast, appointment, content, and offline record patterns only when in scope.
- Keep Opportunity lifecycle out of Task unless explicitly confirmed.

### Appointment Or Invitation

Minimum pages:
- Calendar/list.
- Detail.
- Create/edit.
- Time/resource selection.
- Confirmation.
- Arrival/result.

Key interactions:
- Pick date/time/resource.
- Detect conflicts.
- Confirm/send invitation.
- Record attended/no-show/cancelled/completed.

### Content

Minimum pages:
- Library home.
- Category/list/search.
- Preview/detail.
- Send confirmation.
- Send result.

Key interactions:
- Search/filter.
- Preview.
- Select customer/recipient.
- Send/share.
- View send record.

### Dashboard

Minimum pages:
- Personal performance summary.
- Metric detail.
- Manager/store overview if in scope.
- Management dashboard for manager/regional/HQ roles when role switching or management tools are in scope.
- By-frontline-role performance drilldown from the management dashboard.

Key interactions:
- Date/store/advisor filter.
- Drill down to task/customer/appointment/content details.
- Compare target vs actual.

Management dashboard structure:
- Header with role scope, store/team/region scope, and business period.
- Period control such as today, week-to-date, month-to-date, and year-to-date.
- Grouped metric cards with progress/target state and supporting rows. Default groups: sales or contribution, customer operation, appointment/service conversion, task execution, and WeCom connection.
- Staff/frontline preview list showing at least three people with sales or contribution, task completion, WeCom connection, and a "view performance" action.

By-frontline-role performance detail:
- Tabs or segmented control for each frontline person in the current manager scope.
- Sales/contribution section with progress ring, value, target attainment, orders, average basket or equivalent.
- Customer operation section with acquisition/activation, retention/returning, profile completion, or contact binding according to source material.
- Appointment/service section with attended/completed count, conversion, contribution, and pending service items.
- Task and WeCom operation section with completed/pending task counts, contact adds/binding, outreach, response, deletion/loss, or similar metrics.
- Use the confirmed frontline term. For example, fashion can say FA performance, beauty can say BA performance, and generic projects can say advisor/frontline performance.

### Transfer

Minimum pages:
- Transfer entry/list.
- Select customers.
- Select receiving advisor.
- Confirmation.
- Result/failure.

Key interactions:
- Filter transfer candidates.
- Bulk/select individual customers.
- Confirm ownership change.
- Review failures and retry.

### Extension Module

Minimum pages depend on the integration. Always define:
- Entry point from core app.
- External state or signal.
- Frontline advisor action enabled by that state.
- Result/write-back.
- Fallback if integration data is missing.

Examples:
- Member onboarding status.
- Loyalty member-level or benefit recommendation.
- Commerce signal follow-up.
- CDP/MA audience reason.
- Service case follow-up.

### Advanced Opportunity Module

Use only when the user confirms a real opportunity lifecycle, not just a task target, tag, or saved filter.

Minimum pages:
- Opportunity list.
- Opportunity detail.
- Follow-up timeline or next action.

Key interactions:
- Update follow-up status.
- Schedule next action.
- Convert to appointment/content/send/contact action.
- Distinguish opportunity status from task completion.

## Deliverable Mapping

For each page, document:
- Page name.
- Module.
- Role.
- Depth A/B/C.
- Source flow.
- Data needed.
- Primary action.
- Secondary action.
- Empty/error/permission state.
- Acceptance note.

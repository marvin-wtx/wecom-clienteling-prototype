# Baseline Framework Mode

Use this when the user has only a rough idea, no solid BRD, or asks to start from a common WeCom Clienteling framework for a WeCom ecosystem mini-program clienteling tool.

## Principle

Build a generic but realistic starting point from core capabilities. Do not wait for perfect input. Make assumptions explicit and keep every module's page and interaction chain generic enough to reuse across industries.

Do not include advanced Opportunity Follow-Up by default. Add it only after the user mentions priority-customer or opportunity signals and confirms it needs a lifecycle beyond task targeting, tags, or filters.

## Minimum Assumptions To State

- Industry and frontline role term are unknown until confirmed.
- Customer/member field vocabulary is unknown until confirmed; use neutral labels rather than project-specific identifiers.
- Product surface defaults to WeCom ecosystem mini-program / embedded mobile workbench.
- Prototype presentation defaults to desktop review stage plus mobile full-screen mode when an HTML/clickable prototype is requested.
- Visual style defaults to neutral enterprise workbench unless brand/industry references are provided.
- Core modules are included as a starter framework, with A/B/C depth adjustable later.
- Project-specific integrations are placeholders until named.

## Baseline Core Modules

### 1. Home Workbench

Purpose: give the frontline advisor a daily operating entry.

Base pages:
- Home overview.
- Notification or alert list.
- Today's task summary.

Base interactions:
- Open priority task.
- Jump to client/C360.
- Open appointment or content action.
- View key metrics.
- Use mini-program top navigation and bottom navigation as the top-level app frame.

### 2. Add, Bind, And Identify

Purpose: connect WeCom contacts to known customers or prospects.

Base pages:
- Add/bind status.
- Match result.
- Registration invitation.
- Success/failure state.

Base interactions:
- Confirm match.
- Send registration invitation.
- Resolve unmatched or duplicate customer.
- Return to C360 after binding.

### 3. Client List And C360

Purpose: find customers and act from customer context.

Base pages:
- Client list.
- Search/filter.
- C360 overview.
- Transaction/interaction/wishlist/notes drilldowns as optional B-level pages.

Base interactions:
- Search, filter, sort.
- Open C360.
- Add note/tag.
- Start task/contact/content/appointment action.

Baseline interaction standard:
- Include local list search plus exact/global customer lookup when appropriate.
- Include filters for ownership/scope, customer grouping, member level, customer state, business signals, and WeCom contact state.
- Include sort by recent interaction, recent purchase, or business priority.
- Include empty, no-result, no-permission, disabled-action, and source-failure states for A-level pages.

### 4. Task Execution

Purpose: execute assigned or recommended clienteling actions.

Base pages:
- Task list.
- Task detail.
- Target customer list for 1vN tasks.
- Completion/result feedback.

Base interactions:
- Start task.
- Select customer target.
- Send message/content or record contact result.
- Complete, skip, fail, or no response.

Baseline execution standard:
- Define task source, type, target grain, execution channel, and completion evidence.
- Include status tabs or filters for pending, in progress, completed, skipped, and expired.
- Support 1v1 and 1vN execution as baseline patterns.
- Add Moments, native WeCom broadcast, appointment, or content-specific execution only when the flow calls for it.
- Keep completion/skip feedback inside task detail or a bottom sheet unless a dedicated page is required.

### 5. Appointment Or Invitation

Purpose: invite customers to store, event, consultation, fitting, or service.

Base pages:
- Calendar/list.
- Appointment detail.
- Create/edit appointment.
- Time/resource selection.
- Confirmation.
- Arrival/result capture.

Base interactions:
- Choose customer, time, and resource.
- Detect conflict.
- Send confirmation.
- Record attended, cancelled, no-show, or completed.

### 6. Content And Sharing

Purpose: let advisors find and share approved content.

Base pages:
- Content library home.
- Category/list/search.
- Preview.
- Send confirmation.
- Send result.

Base interactions:
- Search/filter content.
- Preview material.
- Select customer or use customer context.
- Send/share and record result.

### 7. Dashboard And Tracking

Purpose: show personal and manager-level clienteling performance.

Base pages:
- Personal dashboard.
- Metric detail.
- Store/manager overview as B/C-level if managers are in scope.

Base interactions:
- Filter date/store/advisor.
- Drill down to tasks, appointments, content, and customer actions.
- Compare target vs actual.

### 8. Transfer And Ownership

Purpose: manage customer/contact ownership changes.

Base pages:
- Transfer entry/list.
- Select customers.
- Select receiving advisor.
- Confirmation.
- Result/failure.

Base interactions:
- Filter transfer candidates.
- Select individual or bulk customers.
- Confirm transfer.
- Review failures and retry.

### 9. Settings, Role, And Permissions

Purpose: make visibility and role-dependent behavior understandable.

Base pages:
- Profile/settings.
- Role/permission explanation or admin placeholder.
- Empty/no-permission state.

Base interactions:
- View role and store.
- Switch demo role if useful.
- Show restricted content for out-of-scope permissions.

## Baseline Prototype Presentation

When the output includes an HTML/clickable prototype, include:
- Desktop review stage with phone frame, title/version, role selector, device-frame toggle, free-browse/journey mode switch, journey selector, and reset.
- Mobile full-screen mode that hides all stage controls and fills the viewport.
- URL parameters or equivalent controls for view and role when useful for review links.
- Role switching for frontline and manager/supervisor scenarios when permissions are in scope.
- Free browse mode for unguided exploration.
- Preset journey mode for guided demos.
- Journey HUD with current step, short instruction, previous/next/finish/exit.
- Control show/hide rules so review controls never appear as in-app production features.

## Baseline Page Depth

Use this starter depth:

| Module | Default depth | Reason |
|---|---:|---|
| Home workbench | A | Main entry and demo anchor. |
| Add/binding | A | Core WeCom clienteling foundation. |
| Client/C360 | A | Core customer context and action hub. |
| Task execution | A | Core daily operating workflow. |
| Appointment/invitation | B | Common but can vary by business. |
| Content sharing | B | Common supporting workflow. |
| Dashboard/tracking | B | Needed for measurement, often simplified. |
| Transfer/ownership | C | Common governance flow, often not phase-one demo. |
| Settings/permissions | C | Explain variations without overbuilding. |
| Opportunity follow-up | Excluded by default | Add only after priority-customer/opportunity confirmation. |

## Baseline Output

When using baseline mode, output:
- Assumptions.
- Core capability map.
- Generic demo flows.
- Baseline page inventory with A/B/C depth.
- WeCom mini-program and native/container constraints.
- Prototype presentation mode spec when applicable.
- Reusable interaction standards for search, filter, sort, tabs, and page states.
- Task execution model for source, type, target, channel, and completion feedback.
- Visual direction assumption.
- Customization questions.
- Explicit excluded/conditional modules, especially Opportunity and project-specific integrations.

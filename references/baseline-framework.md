# Baseline Framework Mode

Use this when the user has only a rough idea, no solid BRD, or asks to start from a common WeCom Clienteling framework for a WeCom ecosystem mini-program clienteling tool.

Before producing baseline output, also read `references/start-mode-router.md` and `references/reference-page-blueprints.md`.

## Principle

Build a generic but realistic starting point from core capabilities. Do not wait for perfect input. Make assumptions explicit and keep every module's page and interaction chain generic enough to reuse across industries.

Do not include advanced Opportunity Follow-Up by default. Add it only after the user mentions priority-customer or opportunity signals and confirms it needs a lifecycle beyond task targeting, tags, or filters.

Baseline mode is not a low-detail placeholder mode. It is a reusable starter product model. Each A-level page must include concrete objects, states, actions, and linked sample data so the prototype can be judged as a working clienteling tool.

## Minimum Assumptions To State

- Industry and frontline role term are unknown until confirmed.
- Customer/member field vocabulary is unknown until confirmed; use neutral labels rather than project-specific identifiers.
- Product surface defaults to WeCom ecosystem mini-program / embedded mobile workbench.
- Prototype presentation defaults to desktop review stage plus mobile full-screen mode when an HTML/clickable prototype is requested.
- Visual style defaults to neutral enterprise workbench unless brand/industry references are provided.
- Core modules are included as a starter framework, with A/B/C depth adjustable later.
- Project-specific integrations are placeholders until named.

## Minimum Baseline Data Depth

Use a small but connected data model:

- At least 6 customers across different member levels, lifecycle states, WeCom contact states, registration states, owners, and next actions.
- At least 2 WeCom-only contacts that need match, bind, or registration handling.
- At least 5 tasks across 1v1, 1vN, native send or Moments when relevant, appointment/service, content share, and offline/result recording.
- 6-8 appointment/service records when appointment is in scope.
- At least 3 content assets with type, source, readiness, validity, and linked task usage.
- At least 4 dashboard metric groups with period, denominator, owner scope, and drilldown target.

Cross-link the data. A task target should appear in the customer list and C360; an appointment should reference a real customer; a content asset should appear in a task detail or native send path.

## Baseline Core Modules

### 1. Home Workbench

Purpose: give the frontline advisor a daily operating entry.

Base pages:
- Home overview.
- Notification or alert list.
- Today's task summary.
- Today's appointment or service queue when relevant.
- Quick action area for customers, tasks, appointment/service, content, dashboard, and native send when in scope.

Base interactions:
- Open priority task.
- Jump to client/C360.
- Open appointment or content action.
- View key metrics.
- Drill down from metric to the related list.
- Show role-specific scope for frontline vs manager.
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
- WeCom-only contact list or state inside the client list.
- Match/bind/register entry when a contact is not yet a known customer.

Base interactions:
- Search, filter, sort.
- Open C360.
- Add note/tag.
- Start task/contact/content/appointment action.
- Explain disabled actions based on WeCom contact, registration, ownership, or permission state.

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
- Native send entry when the execution channel leaves the mini-program.
- Content attachment or talking-point preview when the task requires prepared material.

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
- Do not collapse every task into a generic "send message" card. Different channels must show different required fields, handoff behavior, and result feedback.

### 5. Appointment Or Invitation

Purpose: invite customers to store, event, consultation, fitting, or service.

Base pages:
- Calendar/list.
- Appointment detail.
- Create/edit appointment.
- Time/resource selection.
- Confirmation.
- Arrival/result capture.
- Conflict or unavailable resource state.

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
- Content readiness or approval state.

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
- Drilldown list for at least one metric in A-level dashboard prototypes.

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
- Reuse `assets/prototype-shell/index.html` or port its shell into the chosen framework.
- Desktop review stage with compact title/version, role selector, free-browse/journey mode switch, journey selector, reset, and entry buttons outside the phone.
- A 390px by 844px mini-program viewport on desktop, scaled to fit the window without cropping the phone, top bar, or bottom tabbar.
- Mobile full-screen mode that hides all stage controls and fills the viewport.
- URL parameters for view and role when useful for QA/review links.
- No visible mobile/desktop selector in the app or review stage.
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

## Baseline Page Blueprint Requirement

Before writing a page inventory or building an HTML prototype, apply `references/reference-page-blueprints.md`.

Minimum page-level expectations:
- Home, client list, C360, task list, and task detail should be A-level unless the user narrows scope.
- Appointment, content library, and dashboard should be at least B-level when they are included in navigation.
- Transfer/ownership and settings can remain C-level unless manager governance is a demo goal.
- Each A-level page needs unique layout sections, not just the same repeated card component with different labels.
- Every A-level page must include at least one meaningful empty, disabled, conflict, or result state.
- Page controls must map to real fields in the sample data.

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

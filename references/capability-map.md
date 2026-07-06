# WeCom Clienteling Capability Map

Use this as a reusable map for retail WeCom/WeChat Work clienteling projects. Adapt terms to the user's business; do not force every module into every project.

## Core Capabilities

### 1. Add, Bind, And Identify

Purpose: connect a WeCom contact to a known customer or prospect.

Typical scope:
- WeCom friend add entry points, QR codes, invitation links, welcome messages.
- Customer/prospect matching and binding.
- Registered vs unregistered customer states.
- Capture advisor, owner advisor, supporting advisor, store, boutique, and region relationships.
- Failed or ambiguous identity resolution.

Prototype implications:
- Entry screen, binding status, registration invite, success/failure states, and contact-source labels.
- Show who can act, who owns the customer, and what is visible before/after binding.

### 2. Client List And C360

Purpose: let the confirmed frontline role, such as FA, SA, BA, advisor, or consultant, find, understand, and act on customers.

Typical scope:
- Client list, global search, advanced filters, sort, saved filters.
- C360 profile, tags, notes, preferences, transactions, interaction history, wishlist, service context.
- Profile states for known customers, prospects, inactive customers, blocked contacts, or transferred customers.

Prototype implications:
- List/search/filter pages.
- C360 overview plus drilldowns for transaction, interaction, wishlist, notes/tags, and relationship history.
- Clear action hierarchy: contact, invite, assign task, send content, create appointment, update note/tag.

### 3. Task Execution

Purpose: turn headquarters, store, or system-generated priorities into frontline advisor actions.

Typical scope:
- Today's tasks, task list, task detail, customer execution list, 1v1 and 1vN execution.
- Task states: pending, in progress, completed, skipped, expired, failed, no response.
- Frequency control, notification, completion feedback, evidence capture.

Prototype implications:
- Home task summary, task list, detail, execution, result feedback, and exception states.
- Show the link between task reason, recommended action, customer eligibility, and measurable outcome.

### 4. Appointment Or Invitation

Purpose: create and manage store visit, fitting, event, consultation, or appointment invitations.

Typical scope:
- Calendar, date list, resource view, appointment detail, create/edit appointment, confirmation, arrival/result maintenance.
- Resource selection such as advisor, room, product, event, service slot.
- Conflict, waitlist, cancellation, no-show, completed states.

Prototype implications:
- Calendar/list, create flow, time/resource selection, support selection, confirmation, detail, result capture.
- If the project uses "invitation" rather than "appointment", reflect that language consistently.

### 5. Content And Sharing

Purpose: let frontline advisors share approved content or product/service material through WeCom.

Typical scope:
- HQ content, store content, category folders, search/filter, preview, share confirmation, send result.
- Content lifecycle, approval status, language, audience eligibility, send record.

Prototype implications:
- Content library, content detail/preview, target selection, send confirmation, result, usage tracking.

### 6. Dashboard And Tracking

Purpose: make clienteling work measurable for frontline advisors and managers.

Typical scope:
- Personal sales/clienteling dashboard, task performance, customer follow-up, appointment, content, conversion, store/region overview.
- Different visibility for frontline advisor, supervisor, store manager, regional manager, HQ.

Prototype implications:
- Separate operational views from management views.
- Tie metrics back to flows: add/bind, task, appointment, content, conversion, and advanced opportunity only if in scope.

### 7. Transfer And Ownership

Purpose: handle customer/contact ownership changes.

Typical scope:
- Transfer candidates, original owner, receiving advisor, approval, confirmation, result, failure handling.
- Ownership changes caused by store move, role change, turnover, customer preference, or operational reassignment.

Prototype implications:
- Transfer list, select customers, select receiving advisor, confirmation, result, error/retry.
- Show data visibility changes and audit trail.

## Advanced Conditional Capabilities

Do not include these by default. Add them only when the user's material indicates the need, or when the user confirms them after consultation.

### Opportunity Follow-Up

Purpose: manage priority customers or commercial opportunities that need sustained nurturing outside one-off tasks.

Trigger terms:
- Opportunity, lead, pipeline, next-best-action.
- 重点客人, 重点客户, 高价值客户, 高潜客户, VIP 客户.
- Purchase intent, replenishment signal, high-priority follow-up, long-cycle conversion, priority client list.

Consult before adding:
- Is this just a segment/filter used for task targeting, or a lifecycle with status, owner, cadence, and next action?
- Does it need a separate opportunity list/detail, or can it live inside task/C360?
- What states exist: new, contacted, interested, converted, paused, lost, no response?
- What makes it different from normal tasks, customer tags, or saved filters?

Prototype implications if confirmed:
- Opportunity list and detail pages.
- Follow-up timeline or next-best-action area.
- Status update and next action scheduling.
- Clear distinction from task execution and client filtering.

## Extension Capabilities

Model these separately from the core WeCom Clienteling scope:

- Proprietary member system, loyalty, member level, points, coupons, benefits.
- Private commerce, mini-program shop, order, reservation, or payment.
- Product recommendation, wishlist, styling board, consultation, content platform.
- CRM/CDP/MA segmentation, campaigns, audience lists, journey automation.
- Service system, repair, aftersales, care program, concierge service.
- Event, class, community, or membership-program onboarding.

For each extension, ask:
- What system owns the data?
- Which customer states come from this integration?
- What frontline advisor action is enabled?
- What is visible inside WeCom vs linked out?
- What status/result needs to be written back?
- What should the prototype demonstrate, and what can remain implied?

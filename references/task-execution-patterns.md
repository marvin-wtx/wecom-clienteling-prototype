# Task Execution Patterns

Use this reference when a prototype includes task follow-up, assigned actions, recommendations, campaign execution, content sending, appointment actions, Moments, or native WeCom send/broadcast handoff.

## Boundary

Task execution is a core WeCom Clienteling capability. Opportunity follow-up is not included by default. Add an Opportunity module only when the user confirms a real lifecycle with owner, reason, status, cadence, next action, and conversion result.

## Task Source

Common sources:
- HQ or brand campaign.
- Store or boutique manager assignment.
- System recommendation.
- CRM/CDP/MA audience trigger.
- Appointment or event operation.
- Content or product launch action.
- Customer service, after-sales, or loyalty/member signal.

Represent the source on task list cards when it affects trust, priority, permissions, or execution rules.

## Task Type

Common task types:
- 1v1 customer follow-up.
- 1vN batch follow-up with per-customer progress.
- Moments or 朋友圈 posting.
- Native WeCom broadcast or 新建群发 handoff.
- Appointment invite, confirm, reschedule, arrival, or result capture.
- Content share or product/material recommendation.
- Customer data completion, binding, registration, tag/note update.

Each type should define:
- Target grain: one customer, many customers, no direct customer list, or appointment/resource.
- Execution channel: clienteling page, WeCom chat, native WeCom page, mini-program card, content share, phone/offline record, or external system.
- Completion evidence: sent, contacted, replied, booked, attended, skipped, failed, expired, or manually recorded.

## Task List

Default task list elements:
- Status tabs or filters: pending, in progress, completed, skipped, expired.
- Source/type/due/status filters.
- Sort by due time and priority.
- Card title.
- Task type or channel badge.
- Source badge, such as HQ, store, system, CRM/CDP/MA.
- Target customer or target count.
- Due time.
- Priority.
- Recommended action.
- Disabled reason when the task cannot be executed.
- Progress for 1vN tasks.

Common list actions:
- Open task detail.
- Start or continue execution.
- Filter by status/source/type.
- Jump to related C360, content, appointment, or native WeCom replica when appropriate.

## Task Detail

Use a shared task detail frame across task types:
- Status and basic task information.
- Task objective or business reason.
- Target summary.
- Recommended script or talking points.
- Preconfigured content/material preview.
- Frequency, permission, or compliance prompt.
- Execution action area.
- Execution record.
- Complete, skip, fail, or no-response feedback.

Do not create a separate complete/skip page unless the source material requires it. A bottom sheet, inline form, or modal is usually enough.

## 1v1 Execution

Use when one task targets one customer.

Show:
- Customer summary.
- C360 entry.
- WeCom contact state and available contact actions.
- Recommended copy or material.
- Primary execution action, such as open chat, send content, invite, or record offline contact.
- Result capture.

States:
- Ready.
- Customer not WeCom friend.
- Customer unregistered/unbound.
- Permission-limited.
- Sent/contacted.
- No response.
- Completed/skipped/failed.

## 1vN Execution

Use when one task targets a list of customers.

Show:
- Target list within task detail or a child page.
- Total, processed, unprocessed, failed, and skipped counts.
- Per-customer status.
- Per-customer disabled reason.
- C360 entry for each customer.
- Per-customer execute action.
- Bulk action only when the channel and compliance rules allow it.

Rules:
- Keep individual customer result tracking visible.
- Do not treat batch execution as one completed state unless all target handling is defined.
- If execution enters native WeCom broadcast, preserve the handoff and return state.

## Moments / 朋友圈

Use when the task is to publish a post rather than contact specific customers.

Show:
- Posting requirement.
- Recommended copy.
- Material or asset preview.
- Visibility or audience rule if provided.
- Publish action or native handoff.
- Completion record.

Do not force a customer target list unless the source material provides one.

## Native WeCom Broadcast

Use when the flow enters native WeCom compose, broadcast, mass send, or 新建群发 behavior.

Read `wecom-native-page-replication.md` and preserve:
- Native page header and visual distinction.
- Recipient summary.
- Message/content payload.
- Asset selection entry when in scope.
- Send/cancel path.
- Frequency/compliance note.
- Return-to-business result state.

## Completion Feedback

Default feedback fields:
- Result: completed, sent, contacted, booked, replied, no response, skipped, failed, expired.
- Note.
- Next follow-up date when useful.
- Skip or failure reason.
- Attachment/result proof only when source material needs it.

Submission states:
- Ready to submit.
- Submitting.
- Submitted.
- Submit failed with retry.
- Returned to task list/detail with updated status.

## Metrics

Task metrics should specify denominator and source:
- Assigned tasks.
- Executable tasks.
- Executed tasks.
- Completed tasks.
- Customer-level completions for 1vN tasks.
- Send success/failure.
- Appointment conversion.
- Reply or engagement if source data exists.

Do not mix task completion, appointment attendance, opportunity conversion, and unregistered WeCom-friend counts unless the metric definition explicitly says so.

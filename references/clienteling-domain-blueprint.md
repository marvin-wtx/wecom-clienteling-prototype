# Clienteling domain blueprint · V4.0

Use this reference to separate transferable retail product structure from brand-specific business claims.

## Common product model

Clienteling helps a frontline user see work, understand the customer context, choose an action, execute through WeCom, and observe the result. Reusable core objects are:

- `Actor`: current frontline or manager role;
- `WorkItem`: task or appointment requiring action;
- `ClientProfile`: basic information, example membership, transactions, interactions, tags, and current actions;
- `ContentAsset`: sendable or previewable content;
- `OutreachDraft`: recipients, message, and one material;
- `Appointment`: customer, time, type, location, status, and notes;
- `ExecutionReceipt`: facts created by the completed action.

## Standard framework

The recommended scope intake offers:

- Home: workbench and today list;
- Clients: list/search/filter, basic profile, membership, transactions, interactions;
- Tasks: list, detail, outreach preparation, native send and result;
- Appointments: calendar/list, detail, create and confirm;
- Performance: personal and task performance summaries;
- Tools: asset library;
- Primary Journey: task → customer/material preparation → native send → result.

Users may add or remove second-level pages in the single intake round.

A user-requested module outside this framework is an extension, not an error. Preserve it, ask for its second-level pages and depth in the same intake, and use neutral structure unless the user supplies its fields or rules.

## Common structures versus brand facts

Common structures and mock values are allowed. Example membership tiers, masked contacts, transaction rows, interaction rows, task states, appointment times, and demo KPIs make the prototype complete without claiming that the brand uses those definitions.

Require source material for real tier names and rules, segmentation, customer eligibility or consent, task origin, KPI definitions or targets, appointment resources or approval, organization permissions, and CRM write-back.

## FSN boundary

Do not transfer FSN-specific FA/Manager permissions, OneID, VIPCode, Attached/Captured, LION, FSN/WFJ segments, INCHANEL, headquarters/store asset rules, fitting-room resources, customer transfer rules, customer records, tasks, or KPI definitions.

Transfer only structural principles: each object has identity, actions have entry conditions, state changes are explicit, back navigation preserves origin, and roles expose only authorized capabilities.

## Result truth

After native send, show only the runtime receipt: sent status, recipient count, message snapshot, material snapshot, and return action. Replies, read state, appointments, follow-up timing, and CRM changes require later events or supplied rules.

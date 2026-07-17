# Operating Archetype Selection

Use this for open-generative or evidence-derived branded HTML/clickable prototypes. It turns sparse inputs into a reasoned operating model without inventing the brand's internal process.

## Purpose

Choose an **operating archetype** before choosing page blocks. An archetype is a clienteling work pattern, not an industry layout, visual theme, or fixed page template. It changes what the frontline user notices first, the navigation priority, the shape of detail pages, and the state-changing interaction.

Do not use this for `reference-led` work when the supplied layout is authoritative. Preserve that layout and document any necessary shell or usability exception.

## Selection Rule

For open-generative or evidence-derived work:

1. Consider at least three distinct archetypes.
2. Select one primary archetype from business evidence, public brand evidence, industry context, and demo objective.
3. Record the operational tension: the recurring decision or tradeoff the frontline user must resolve.
4. Reject at least two considered archetypes with a concrete reason.
5. Change the home narrative, navigation logic, at least two detail-page architectures, and the signature interaction to fit the selection.

`priority-queue` is valid, but it is not a neutral automatic default. Do not select it only because the brief is sparse, the starter shell uses it, or it is easy to implement. State a positive recurring-workload reason.

## Archetype Families

| ID | Best fit | Home and navigation implication | Detail and interaction implication |
| --- | --- | --- | --- |
| `priority-queue` | Daily follow-up, deadline, exception, or workload triage is the clearest operating need. | Triage or ranked queue; frequency-first navigation. | C360 resolves priority reason and next action; follow-up state is created or updated. |
| `appointment-atelier` | Service readiness, booking conversion, resource preparation, or store visit is the strongest credible journey. | Service agenda or preparation board; appointment may lead navigation. | Appointment becomes a preparation/outcome workspace; confirm, prepare, arrive, and follow-up change state. |
| `product-interest-studio` | Product discovery, preference capture, or assisted recommendation is supported by the brief. | Interest pulse or curated product-context entry; object-first navigation is plausible. | C360 surfaces interests and context; saved interest becomes a sharable or appointment-ready action. |
| `lifecycle-radar` | Replenishment, activation, loyalty moment, or relationship timing is the operating rationale. | Segment/radar composition; lifecycle-first navigation. | Customer timeline emphasizes trigger, window, and response; action schedules the next moment. |
| `service-recovery-desk` | Resolution, care follow-up, exception handling, or trust repair is central. | Case queue and risk signals; worklist navigation. | C360 uses issue, commitment, history, and recovery context; resolution writes back an outcome. |
| `event-attendance-cockpit` | RSVP, attendance, guest preparation, or event conversion is the credible main journey. | Event readiness and guest status; event/agenda entry gains priority. | Guest detail connects invite, attendance, preference, and post-event follow-up. |
| `content-conversation-engine` | Approved material must become relevant one-to-one conversations or measured outreach. | Content-to-action worklist or readiness view; hub-and-action navigation fits. | Asset preview, customer context, send/handoff, and response capture form one workflow. |
| `manager-exception-review` | The primary user is manager/HQ and needs team, ownership, conversion, or risk intervention. | Exception-first management cockpit; role-first navigation. | Drilldown moves from KPI exception to frontline/customer action and records intervention. |

The archetype does not authorize internal names, tiers, campaigns, rooms, or proprietary workflow claims. Keep those neutral unless separately evidenced.

## Token Contract

For applicable work, add `archetypeSelection` to the visual token:

```json
{
  "primaryArchetypeId": "appointment-atelier",
  "candidateArchetypeIds": [
    "appointment-atelier",
    "product-interest-studio",
    "priority-queue"
  ],
  "operationalTension": "The advisor must convert an expressed visit intent into a prepared, confirmed service moment without losing customer context.",
  "selectionRationale": "Service preparation and appointment conversion are the most credible recurring decision in the brief, so the information architecture begins with readiness rather than a generic customer queue.",
  "antiConvergenceCommitment": "Navigation, first viewport, appointment detail, and result capture will follow service readiness rather than the starter queue stack.",
  "rejectedArchetypes": [
    {
      "id": "product-interest-studio",
      "reason": "Interest capture is useful supporting context but the brief does not make product discovery the daily operating center."
    },
    {
      "id": "priority-queue",
      "reason": "A generic urgency queue would hide the preparation and resource decisions that make this service journey distinctive."
    }
  ]
}
```

When the primary archetype is `priority-queue`, also add `priorityQueueJustification` with a positive evidence- or workload-based reason. "The brief is sparse" is not enough.

## Portfolio Rule

When previous open-generative cases are available, do not repeatedly pick the same archetype unless the new brief genuinely calls for it. If it is reused, change at least four of these dimensions: navigation model, home narrative, C360 architecture, task model, data story, appointment architecture, signature interaction.

Record the comparison in the prototype case evaluation and run the portfolio diversity checker. Different colors, brand words, imagery, typography, or border radius do not count as a material difference.

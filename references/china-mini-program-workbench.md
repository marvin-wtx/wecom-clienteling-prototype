# China Mini-Program Workbench

Use this before composing any clienteling workbench. It is a design judgment aid, not a page template.

## Start from one work moment

Make the first phone viewport answer, without reading a paragraph:

1. What needs attention now?
2. Why is it urgent or valuable?
3. What can the advisor do next?

Show one dominant work focus, then a short ranked queue and a visible recent-result area. Do not lead with a campaign, a generic greeting, or an equal-weight KPI wall.

## Use a small operational vocabulary

- **Priority item:** a tappable row with customer/task, reason, time/status, and one clear action.
- **Status:** compact chips or short labels; distinguish due, waiting, ready, completed, and blocked without paragraphs.
- **Queue:** grouped list rows with real touch targets; do not put every item in a large white card.
- **Result:** a timestamped, named write-back that appears after the corresponding action.
- **Decision/action:** use a bottom action bar, bottom sheet, picker, or confirmation region when the action needs a choice.

Use cards only when grouping a single decision or dense object. Different work types must not all use the same title + fine border + two-column fields pattern.

## Readability and hierarchy

- Design at 390px first. Keep the primary task readable at normal phone scale; do not solve density by shrinking all text.
- Give the next action the strongest contrast and the largest touch target. Keep supporting metadata quiet.
- Use one accent for priority, progress, confirmation, and primary action; do not use brand treatment as a substitute for hierarchy.
- Let brand direction influence material, rhythm, typography, and restrained imagery—not the credibility of an invented workflow.
- Prefer concise Chinese operational copy. Field inventories, repeated labels, and long explanatory sentences are implementation notes, not UI.

## Common failures

Reject a page when it looks like any of these:

- a white-card / hairline-border stack where every block has equal visual weight;
- a KPI strip with no clear follow-on action;
- a task detail that reads like a specification table rather than an execution surface;
- a pre-completed seed used to make the workbench look alive;
- a fictional premium concept, editorial story, or brand lore replacing daily work;
- an action that changes a counter but leaves no named result where the user returns.

## Minimum interaction proof

Begin at a genuinely open item. Complete one action, return to the workbench, and show that exact item/result in the result area with a changed status or timestamp. Use the same path for screenshots and reviewer Journey.

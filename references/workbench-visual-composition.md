# Workbench Visual Composition

Use this after choosing the operating loop and before writing UI markup. It governs hierarchy, not IA or brand style.

## First viewport

Compose exactly these three semantic regions in order:

1. `data-workbench-priority`: one open work item with customer/object, reason, due/status, and primary action.
2. `data-workbench-queue`: a short ranked list of the next relevant items. Use rows, not a gallery of equal cards.
3. `data-workbench-result`: latest named write-back, initially an honest empty state when nothing has been completed.

Do not place a KPI wall, repeated navigation shortcuts, campaign image, or generic greeting before the priority item. A compact context line is enough.

## Component contrast

- Make priority a distinct focus treatment; it is the only strong accent or material moment on the first screen.
- Make queue items compact, tappable rows with different status treatments, not copies of the priority card.
- Make result look like a receipt: object, outcome, timestamp, and optional next follow-up.
- Use low-contrast separators or background grouping for supporting information. Spend borders sparingly.
- Do not duplicate a bottom-tab route as a shortcut. A shortcut must be a creation, native handoff, or role-specific exception.

## Brand translation

Translate brand into one accent, surface material, typography rhythm, and selected imagery. Never use a brand moodboard, luxury vocabulary, or editorial layout to manufacture an operating model.

## Screenshot test

At normal phone scale, a reviewer must point to the priority action in three seconds. If they instead see several equal cards, an unexplained metric strip, or need to read dense copy to find the next action, redesign the composition.

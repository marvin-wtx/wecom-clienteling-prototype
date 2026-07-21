# Workbench Visual Recipes

Choose one recipe after defining the work loop and `workbenchVisualPlan`. A recipe changes material, contrast, and typography only. It never supplies page names, roles, data, or a business concept.

Copy `assets/prototype-shell/workbench-visual-primitives.css` unchanged next to the project `index.html`, link it locally, and wrap the workbench with one of the following attributes:

```html
<main class="wb-workbench" data-workbench-style="precise">
```

## Precise

Use `data-workbench-style="precise"` for dense everyday work. It uses clean edges, quiet surfaces, and a clear primary button. Let the content—not decorative materials—create urgency.

## Boutique

Use `data-workbench-style="boutique"` when credible brand material calls for a restrained, warmer expression. It adds gentle surface depth and a single display-type moment to the priority item. Do not turn it into an editorial story or use it to imply a premium operating model.

## Vivid

Use `data-workbench-style="vivid"` when the real work moment is time-sensitive and immediate. It puts the accent on the one priority item and keeps the queue/result quiet. Do not use it for every module or action.

## Required primitives

Use these class names in the three required semantic regions; local project CSS may only set brand tokens or add project-specific detail around them.

| Region | Required class | Intent |
| --- | --- | --- |
| `data-workbench-priority` | `wb-priority` | One open item, reason, status, one next action |
| `data-workbench-queue` | `wb-queue` | Compact ranked rows using `wb-queue__row` |
| `data-workbench-result` | `wb-result` | Empty state first; named receipt after action |

Use `wb-status` for compact states and `wb-action-sheet` when an action needs a choice. Do not use the primitives to construct a KPI wall, repeated card gallery, or duplicate bottom-tab shortcuts.

## Screenshot judgment

Inspect an actual Chrome render at normal phone scale before release. A passing first viewport has a complete shell, one immediately discoverable next action, a visually subordinate queue, and an honest result state. The reviewer must reject a page that is cropped, blank, card-stacked, or presents duplicate primary navigation—even when JSON artifacts say it passed.

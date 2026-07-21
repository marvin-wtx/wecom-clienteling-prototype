# Prototype Shell Contract · V4.0

Use `assets/prototype-shell/index.html`, `shell-runtime.js`, and `workbench-visual-primitives.css` only after scope, blueprint, and page-state gates pass.

## Geometry

- Keep `#app` full height and `.body` as the scroll container.
- Keep the bottom tab bar pinned to the mobile viewport when confirmed navigation includes one.
- Keep desktop phone geometry at 390 × 844 before scaling; mobile fills `100dvh`.
- Keep normal `?view=desktop` product-only.
- Show role, Journey, Fit, and review controls only with `?review=1`, outside the phone.

## Contract markers

Mark implemented mobile pages with `data-page-id`, `data-module`, `data-selection`, and `data-page-depth`. Mark each common contracted field with `data-common-field`. Declare demo content once with `data-demo-data="true"`.

## Native group send

Mount `renderWecomExecute()` directly into `#app` with `data-native-mount="direct"`. Do not wrap it in `appShell`, `.wx-nav`, a task header, tab bar, or branded shell. Bind the current recipients, message, and image or mini-program material. Cancel preserves the draft; send creates a runtime receipt shown by a result carrying `data-result-source="runtime-receipt"`.

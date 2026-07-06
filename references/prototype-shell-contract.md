# Prototype Shell Contract

Use this contract whenever the output is an HTML or clickable prototype for a WeCom / WeChat Work mini-program clienteling tool.

## Mandatory Source Asset

- Start from `assets/prototype-shell/index.html` unless the user explicitly requests another stack.
- Keep the shell structure intact: `stage`, `stage-header`, `stage-controls`, `phone-wrap`, `phone`, `statusbar`, `screen`, `wx-nav`, `wx-capsule`, `body`, `tabbar`, `journey-hud`, and native page containers.
- Build pages by filling the shell's content slots, route map, data fixtures, role labels, and journey definitions. Do not rebuild a different phone frame, mini-program top bar, or bottom tab system.
- If using React/Vue/Svelte or another framework, port the shell classes and behavior directly instead of inventing new layout rules.

## Viewport Behavior

- Desktop and mobile presentation must be code-level responsive.
- On desktop, show a review frame with prototype controls outside the mini-program screen.
- On mobile, the prototype must become a true full-screen mini-program view using viewport and user-agent detection.
- URL parameters such as `?view=mobile` and `?view=desktop` may exist for QA, but do not expose a visible "mobile/desktop" selector in the product UI.
- Mobile mode must never hide the phone, screen, page body, or mini-program container. A blank mobile screen is a release blocker.

## WeCom Mini-Program Frame

- Every in-app page must sit inside the mini-program container.
- Preserve a WeCom-style title bar and capsule area. Long titles must truncate before colliding with the capsule.
- Bottom tabs appear only on top-level mini-program pages. Secondary flows may hide the tabbar and provide a back path.
- Native WeCom replicas, such as `新建群发`, must be visually separated from custom mini-program pages and must preserve the native flow sequence.
- Desktop review controls, role controls, journey controls, and QA controls must live outside the phone screen.

## Interaction Baseline

- Every list page should include search, filter, empty/loading/error states when relevant, and a tab or segmented control only when there are true categories.
- Task execution must model channel, audience, content readiness, execution action, progress, result feedback, and next follow-up.
- Disabled actions must explain the missing condition, for example missing customer selection, content not ready, permission unavailable, or native WeCom limit.
- Preset journeys should drive route, role, highlighted step, and expected outcome while still allowing free browsing.

## Role And Vocabulary

- Confirm the industry role label before writing final copy:
  - `SA` for general sales/service associate contexts.
  - `FA` for fashion advisor contexts.
  - `BA` for beauty and personal-care advisor contexts.
- Ask whether the project has custom customer/member field names. If not, use neutral labels such as customer ID, member level, customer profile, preference, lifecycle stage, and interaction history.
- Do not introduce project-specific field names into generic prototypes unless the user provided them for that project.

## Visual Rules

- Use SVG icons or an approved icon library. Do not use emoji in tabbars, quick entrances, status markers, empty states, or task cards.
- Start from a neutral WeCom workbench palette and apply brand color as an accent. Avoid one-note palettes where every surface is a variation of the same hue.
- Keep cards at 8px radius or below unless the user's design system requires otherwise.
- Use compact operational layouts. This is a working tool, not a marketing landing page.

## QA Requirements

Run the static shell checker before delivery:

```bash
python3 scripts/check_prototype_shell.py path/to/index.html
```

For private client work, add a local blocklist without committing it:

```bash
WECOM_CLIENTELING_FORBIDDEN_TERMS="term1,term2" python3 scripts/check_prototype_shell.py path/to/index.html
```

Also visually verify:

- Desktop frame loads and controls are outside the mini-program screen.
- Mobile viewport shows a full-screen, nonblank mini-program.
- Top bar, capsule, body content, bottom tabbar, and sticky actions do not overlap.
- Emoji are absent from UI source and rendered screenshots.
- Native WeCom pages and custom mini-program pages remain distinguishable.

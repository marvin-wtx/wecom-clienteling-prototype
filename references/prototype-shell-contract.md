# Prototype Shell Contract

Use this contract whenever the output is an HTML or clickable prototype for a WeCom / WeChat Work mini-program clienteling tool.

## Mandatory Source Asset

- Start from `assets/prototype-shell/index.html` unless the user explicitly requests another stack.
- Keep the shell structure intact: `stage`, `stage-header`, `stage-controls`, `phone-wrap`, `phone`, `statusbar`, `screen`, `wx-nav`, `wx-capsule`, `body`, `tabbar`, `journey-hud`, and native page containers.
- Build pages by filling the shell's content slots, route map, data fixtures, role labels, and journey definitions. Do not rebuild a different phone frame or mini-program top bar. Keep the bottom-navigation mechanics and safe area, but adapt its information architecture and visual treatment.
- If using React/Vue/Svelte or another framework, port the shell classes and behavior directly instead of inventing new layout rules.

## Viewport Behavior

- Desktop and mobile presentation must be code-level responsive.
- On desktop, show a review frame with prototype controls outside the mini-program screen.
- On desktop, the mini-program viewport should be 390px by 844px before scaling. Scale the phone wrapper to fit the available desktop height and width instead of changing the page content height.
- The full phone must remain visible on desktop, including top frame, iPhone-style notch, mini-program navigation, body, and bottom tabbar.
- Desktop stage header and controls should be compact, centered, and no wider than about 920px. They are reviewer tools, not app chrome.
- On mobile, the prototype must become a true full-screen mini-program view using viewport and user-agent detection.
- URL parameters such as `?view=mobile` and `?view=desktop` may exist for QA, but do not expose a visible "mobile/desktop" selector in the product UI.
- Mobile mode must never hide the phone, screen, page body, or mini-program container. A blank mobile screen is a release blocker.
- Mobile full-screen mode should hide decorative desktop hardware details such as the phone border, notch, and statusbar so the mini-program fills the viewport cleanly.

## WeCom Mini-Program Frame

- Every in-app page must sit inside the mini-program container.
- Desktop review mode must show the iPhone-style hardware notch as part of the protected phone frame. Do not remove it when adapting page design.
- Preserve a WeCom-style title bar and capsule area. The protected top geometry is a 38px status row plus a nav row below it; the nav title and WeCom capsule must be vertically centered in that nav row instead of sharing the status-row space.
- Status text should show `9:41` on the left and `5G` on the right without fake signal-dot placeholders. The compact notch should remain centered above the status row in desktop review mode.
- Long titles must truncate before colliding with the capsule.
- Bottom tabs appear only on top-level mini-program pages. Secondary flows may hide the tabbar and provide a back path.
- The bundled Home, Customers, center quick action, Tasks, and Appointments order is only a neutral starter example.
- Choose 3-5 top-level items from the project's highest-frequency journeys. Home is optional when another workbench entry is clearer. Customers, Tasks, Appointments, Content, Dashboard, Opportunities, or a role-specific queue may become top-level according to scope.
- The center quick-action entry is optional. Use it only when cross-module creation or execution is a dominant workflow.
- Tab order, labels, icon style, active treatment, indicator style, and background/material may vary by brand and role. Preserve touch targets, safe area, state clarity, and route behavior.
- Content library, dashboard, transfer, native broadcast, and manager tools can be reached through quick actions, task detail, or role-specific entries unless they are primary demo tabs.
- The center quick-action entry must not duplicate primary bottom tabs or page-local controls. Do not put Tasks, Appointments, or Customer Filter inside the quick-tool panel when they already exist as main tabs or list-page controls.
- The quick-tool panel should expose true shortcuts such as content/material library, dashboard, and role-specific management actions. Store manager or higher roles should be able to reach Customer Transfer when that capability is in scope.
- Dashboard routes should adapt to the selected business role. Frontline users may see personal execution metrics; store manager, regional, or HQ roles should see management views such as team execution, advisor coverage, customer asset status, and transfer needs.
- Management dashboard routes for store manager, regional, or HQ roles must include a reporting period control, role/scope copy, grouped KPI modules, progress or target attainment, and a link into by-frontline-role performance. Do not represent management tracking as only four generic summary cards.
- The by-frontline-role performance route should be reachable from the management dashboard and use the confirmed frontline term. It should show sales/contribution, customer operation, appointment/service conversion, task execution, and WeCom connection metrics, with labels adapted to the user's source material.
- Native WeCom replicas, such as `新建群发`, must be visually separated from custom mini-program pages and must preserve the native flow sequence.
- Desktop review controls, role controls, journey controls, and QA controls must live outside the phone screen.

## Interaction Baseline

- Every list page should include search, filter, empty/loading/error states when relevant, and a tab or segmented control only when there are true categories.
- Task execution must model channel, audience, content readiness, execution action, progress, result feedback, and next follow-up.
- Disabled actions must explain the missing condition, for example missing customer selection, content not ready, permission unavailable, or native WeCom limit.
- Secondary-page bottom CTA bars must be pinned to the bottom of the mini-program shell. Keep the content area scrollable and padded so the CTA never floats mid-page, overlaps cards, or depends on content height.
- Preset journeys should drive route, role, highlighted step, and expected outcome while still allowing free browsing.
- Baseline prototypes must use connected sample data. Customer, task, appointment, content, and dashboard screens should reference the same underlying objects where possible.
- Do not ship generic repeated pages where every module uses the same card layout with different titles.
- The bundled shell may include small interactive sample pages to demonstrate routing and controls, but those examples are not a substitute for project-specific page content.

## Role And Vocabulary

- Confirm the industry role label before writing final copy:
  - `SA` for general sales/service associate contexts.
  - `FA` for fashion advisor contexts.
  - `BA` for beauty and personal-care advisor contexts.
- Treat the frontline role term as a generation-time configuration, not as a visible prototype control. Do not expose a FA/SA/BA selector in the shell.
- Stage role switching is only for permission and data-scope roles, for example frontline, store manager, regional manager, or HQ.
- Ask whether the project has custom customer/member field names. If not, use neutral labels such as customer ID, member level, customer profile, preference, lifecycle stage, and interaction history.
- Do not introduce project-specific field names into generic prototypes unless the user provided them for that project.

## Visual Rules

- Treat the bundled shell as a protected frame, not a frozen visual style. The protected layer is: desktop review stage, desktop phone frame and notch, mobile/desktop responsive behavior, WeCom mini-program container, nav title/capsule geometry, bottom-navigation mechanics and safe area, role/journey controls, sticky CTA behavior, native WeCom replica structure, and QA guardrails.
- Treat page composition as an adaptable layer. A project may change page density, content hierarchy, card/list/table patterns, brand accents, typography scale within shell limits, icons, imagery, data fields, and module-specific layouts when source material or visual references justify it.
- Adaptable page design must still pass the shell contract: no broken mobile full-screen mode, no in-app viewport selector, no FA/SA/BA runtime selector, no emoji UI, no duplicated quick tools, no floating secondary CTA, and no custom redesign of native WeCom pages.
- For branded prototypes, map visual references into a brand visual token before coding. Apply brand skin through CSS variables such as `--brand-primary`, `--brand-primary-strong`, `--brand-accent`, `--brand-on-primary`, `--bg`, `--surface`, `--surface-soft`, `--line`, `--text`, and `--muted`.
- Brand skin can alter page-level colors, card rhythm, density, image placement, chips, CTAs, module layouts, and bottom-navigation visual treatment. Product IA can alter the bottom-navigation item set and order. Neither may break shell geometry, capsule behavior, safe area, route state, role/journey controls, mobile full-screen behavior, sticky CTA anchoring, or native WeCom replica structure.
- Native WeCom replicas should remain native-like and neutral. Use business content from the project, but do not apply branded marketing surfaces or custom clienteling navigation to native compose/send pages.
- Use SVG icons or an approved icon library. Do not use emoji in tabbars, quick entrances, status markers, empty states, or task cards.
- Apply one global shell SVG guardrail: every generated inline SVG icon must have explicit width, height, stroke, line-cap, line-join, and `fill: none`. Do not rely on per-button icon CSS only; a missed search/filter icon can render at the browser's default SVG size and visually cover the page.
- Start from a neutral WeCom workbench palette and apply brand color as an accent. Avoid one-note palettes where every surface is a variation of the same hue.
- Keep cards at 8px radius or below unless the user's design system requires otherwise.
- Use compact operational layouts. This is a working tool, not a marketing landing page.
- Keep review controls visually modest: compact select fields and buttons, small labels, and no large decorative control panels.

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
- Desktop phone frame shows the notch; mobile full-screen hides decorative phone hardware.
- Status bar, nav title, capsule, body content, bottom tabbar, notch, and sticky actions do not overlap.
- Secondary-page CTAs sit at the bottom edge of the shell in filter, C360, task detail, create/edit, and result pages.
- Emoji are absent from UI source and rendered screenshots.
- Native WeCom pages and custom mini-program pages remain distinguishable.

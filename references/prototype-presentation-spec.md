# Prototype Presentation Spec

Use this when creating an HTML or clickable review prototype. The default pattern is a mobile mini-program experience inside a desktop review stage, plus a full-screen mobile mode.

For HTML prototypes, first read `prototype-shell-contract.md` and start from `../assets/prototype-shell/index.html` or port that shell directly into the chosen framework.

## Required Presentation Modes

### Desktop Review Stage

Purpose: let stakeholders review, switch roles, use preset journeys, and inspect the mobile mini-program in a controlled frame.

Include:
- Stage header with prototype title, version, and optional update note.
- Stage controls above the phone frame.
- Phone frame sized around a mobile mini-program viewport, commonly 390 x 844 or comparable.
- Role selector.
- Mode switch between **Free Browse** and **Journey Demo**.
- Preset journey selector and reset button when journey mode is active.
- URL parameters for reproducible review links when feasible, such as `view=desktop`, `view=mobile`, `role=...`, `date=...`, and optional journey state.
- No visible mobile/desktop selector inside the prototype. Viewport mode must be automatic or URL-driven for QA.

### Mobile Full-Screen Mode

Purpose: approximate actual mobile/WebView usage.

Rules:
- Hide desktop stage header and stage controls.
- Hide decorative phone frame/status shell unless explicitly needed.
- Use `100vw` and `100dvh` behavior where supported.
- Keep the mini-program navigation and app UI visible.
- Preserve the same business pages and role/page behavior as desktop stage.
- Do not hide the phone, screen, body, or mini-program container in mobile mode.

## Stage Controls

Use stage controls only in desktop review mode:
- Role: switch between configured roles, such as frontline advisor, manager development, manager/global, or client-specific roles.
- Mode: free browse vs journey demo.
- Journey selector: choose a preset journey.
- Reset journey: restart the current preset journey.
- Language toggle may live inside the app shell or stage if required by the prototype.

In mobile full-screen mode, hide stage controls. Do not let review controls look like production app features.

## Role Switching

Implement role switching when prototype scope includes permission differences:
- Role switching changes available tools, data scope, page labels, and management views.
- In journey mode, the active journey may control role; manual role switching should be disabled or blocked with a clear toast/message.
- Role-specific visibility must match business rules: hide unavailable manager-only tools for frontline users if the business rule says hidden.

## Free Browse Mode

Free browse mode is the default exploratory state:
- User can navigate any built page through app navigation and links.
- Role selector is active.
- Journey HUD is hidden.
- Page state should be stable after role or language changes.

## Journey Demo Mode

Preset journey mode is for guided stakeholder review:
- User chooses a named journey from a selector.
- Journey sets the required role.
- Each step navigates to a page, highlights a target area, and shows short guidance.
- HUD shows journey name, step count, step label, description, previous/next, finish, and exit.
- Exiting journey returns to a stable default page such as home.

Typical journeys:
- Daily workbench to task detail.
- Search client and inspect C360.
- Invite known customer to register mini-program.
- Convert unmatched WeCom friend.
- Create appointment/invitation and send mini-program card.
- Browse content library and preview material.
- Manager-only customer transfer.
- Manager dashboard/drilldown when management scope exists.

## Control Visibility And App UI Rules

Keep review controls separate from app controls:
- Stage controls: desktop only.
- Mini-program top navigation: app UI.
- Bottom navigation: app UI on top-level pages only.
- Floating/central tool entry: app UI if the business design requires it.
- Sticky bottom action bars: app UI for creation, confirmation, and result flows.

For app UI visibility:
- Hide bottom navigation on deep details, filters, transaction drilldowns, task details, C360 detail pages, registration flows, appointment creation/detail/completion, and other pages where bottom tabs conflict with the active flow.
- Show role-dependent tools only for eligible roles.
- Hide project-specific modules unless they are in scope.

## Responsive QA

Verify:
- `scripts/check_prototype_shell.py` passes for generated HTML.
- Desktop stage scales the phone frame without changing the designed mobile layout.
- Mobile mode removes stage controls and fills the viewport.
- Mobile mode is nonblank and still shows mini-program top navigation, body content, and expected bottom navigation or sticky action.
- No visible viewport selector appears in the app or stage controls.
- Stage controls do not wrap awkwardly in English or Chinese.
- Long mini-program titles fit around native safe areas.
- Text and actions fit in both desktop-stage phone and mobile full-screen modes.
- Free browse and every preset journey still work after switching role, language, and viewport.

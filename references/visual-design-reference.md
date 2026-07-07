# Visual Design Reference

Use this before producing a visual prototype or prototype brief. The goal is to choose an industry-appropriate direction, not to over-style operational screens.

## Visual Intake

Ask only what is needed for the current fidelity:

- What brand or industry should the prototype visually feel aligned with?
- Is there a brand guideline, design system, mini-program, app, CRM, POS, or WeCom workbench screenshot to reference?
- Should the prototype look like a neutral product demo, an enterprise workbench, or a brand-polished client presentation?
- What is the expected deliverable surface: WeCom mini-program-style mobile experience, desktop review stage around mobile, Figma screen, PPT, or HTML prototype?
- What level of visual fidelity is needed: wireframe, clean business prototype, high-fidelity branded prototype, or clickable demo?
- Are product images, campaign images, logos, icons, fonts, colors, or sample content available?
- Are there visual constraints from WeCom, an existing app shell, or client IT?

For product UI work, use real references first when available. If Lazyweb or another design-reference tool is available, search relevant patterns before designing: client list, C360, task detail, appointment calendar, content library, dashboard, transfer flow, or industry-specific workbench.

For HTML/clickable prototypes, the bundled shell already defines a neutral operational base. Keep that base unless the user provides a stronger design system.

## Shell Versus Page Design

Do not confuse shell consistency with visual sameness.

Protected shell layer:
- Desktop review stage and external role/journey controls.
- Mobile full-screen behavior and automatic responsive mode.
- WeCom mini-program container, top title bar, capsule, bottom tabs, and safe-area behavior.
- Secondary-page bottom CTA anchoring.
- Native WeCom page replicas such as 新建群发.
- QA guardrails such as no emoji UI, no runtime FA/SA/BA selector, and no duplicated quick tools.

Adaptable page layer:
- Brand accent colors, typography weight, information density, card/list/table choices, section rhythm, and icon style.
- Module-specific layouts for home, customer list, C360, tasks, appointment, content library, dashboard, transfer, and extension modules.
- Visual hierarchy and copy tone based on the target industry and provided references.
- Data fields and labels, as long as project-specific names are not invented without source evidence.
- High-fidelity brand moments, product images, campaign assets, or executive-demo polish when the user provides enough material.

If the user provides screenshots, brand references, or a design system, adapt the page layer to those references while preserving the protected shell. If there is no visual reference, use the neutral operational shell and vary page content through business structure, not decoration.

## Style Direction Templates

Choose one direction as a starting point, then adapt to the client's brand and prototype goal.

### 1. Neutral Enterprise Workbench

Best for: early business alignment, IT handoff, cross-industry clienteling.

Characteristics:
- High information density.
- Light background, restrained color accents.
- Clear hierarchy, tables/lists/cards used for operational scanning.
- Minimal decoration.
- Status chips, metrics, filter bars, and stable navigation.

Avoid:
- Marketing-style hero sections.
- Overly decorative cards.
- Heavy gradients or lifestyle imagery that makes business logic harder to review.
- Emoji icons or consumer-app decoration in operational navigation.

### 2. Luxury Fashion Clienteling

Best for: fashion, luxury retail, boutique advisor experiences.

Characteristics:
- Quiet premium tone.
- Sparse but precise typography.
- Product/customer imagery used selectively.
- Warm neutral or monochrome base with one controlled accent.
- Strong spacing and curated detail, but still operational.

Use role naming:
- Prefer FA unless the client says otherwise.

Avoid:
- Loud SaaS colors.
- Generic stock imagery.
- Overly playful icons or round app-like visuals.
- Turning the entire prototype into one gold, brown, black, or beige palette because the brand is luxury.

### 3. Beauty BA Workbench

Best for: cosmetics, skincare, fragrance, personal care.

Characteristics:
- BA-centered customer consultation and replenishment logic.
- Product/category visuals can be more visible than in generic enterprise tools.
- Softer color palette may be acceptable, but keep operational contrast.
- Emphasize member profile, purchase cycle, product preference, samples, coupons, service or counter appointment.

Use role naming:
- Prefer BA unless the client says otherwise.

Avoid:
- Calling BA users FA/SA.
- Making the UI feel like a consumer shopping app when it is an advisor workbench.
- Emoji for product categories, tabs, metrics, or quick actions.

### 4. Branded Executive Demo

Best for: stakeholder presentation where brand fit matters.

Characteristics:
- More polished navigation and page framing.
- Stronger use of brand color, campaign content, and realistic sample data.
- Fewer placeholder states; more curated demo path.

Avoid:
- Letting polish hide missing business coverage.
- Using brand elements without enough content permission or source material.

### 5. Wireframe / Requirement Handoff

Best for: validating scope, page inventory, system rules, and IT discussion.

Characteristics:
- Low visual polish.
- Explicit labels, states, and data fields.
- Clear page numbering and flow traceability.
- Component consistency over brand expression.

Avoid:
- Ambiguous visual shorthand that reviewers may misread as final UX.

## Visual Brief Output

When briefing a prototype, include:
- Chosen style direction.
- Industry role naming.
- WeCom mini-program/container visual constraints.
- Desktop review stage vs mobile full-screen presentation rules.
- Reference sources available and missing.
- Color/typography/image constraints.
- Page density target.
- Component conventions: cards, lists, tabs, filter bars, status chips, modals, bottom navigation.
- Icon rule: SVG or approved icon library only; no emoji in app UI.
- Color rule: neutral WeCom/workbench base plus controlled brand accents; avoid one-hue themes.
- What is intentionally not designed in this round.

## QA Checks

- Does the role naming match the industry?
- Does the visual density support operational work?
- Does the styling fit the review purpose?
- Are extension modules visually distinguished without looking disconnected?
- Are references traceable to provided material or real pattern research?
- Are generic templates clearly adapted to the client instead of copied verbatim?
- Are tabbar, quick entrance, task, and state icons implemented as SVG/library icons rather than emoji?
- Does the palette preserve operational contrast and avoid overusing a single brand hue?

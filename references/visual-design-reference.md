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

For HTML/clickable prototypes, the bundled V3 shell kit defines a modern neutral operational base and reusable mechanics, not a default app layout. Keep its protected frame and primitives unless the user provides a stronger design system; design the actual navigation, page composition, data story, and module grammar for the project.

## V3 Modern Baseline

The shell kit is intentionally more refined than the former generic demo without becoming a hidden brand skin:

- The desktop stage uses a quiet technical canvas, compact review controls, a lighter device frame, and restrained elevation so the prototype reads as a reviewed product rather than a wireframe inside a heavy mock phone.
- The mini-program frame uses translucent navigation/tab materials, hairline boundaries, precise type hierarchy, and controlled panel depth. These improve perceived quality while preserving WeCom geometry and scanning speed.
- The page utility layer supplies compact surfaces, metric strips, row patterns, media frames, search/filter controls, action bars, and dynamic tab counts. It does not prescribe a hero, KPI grid, center action, card stack, tab order, or business module.
- Treat the provided preview as a visual component specimen only. Remove it before delivery and construct the visual rhythm from the selected operating model and actual brand evidence.

Modern does not mean universally glossy, blue, rounded, or image-heavy. Brand evidence may change the page-layer palette, type, material, imagery, density, and geometry; the neutral shell only protects the operating frame.

## Visual Generation Workflow

Use this sequence for brand-aware prototypes:

1. Choose fidelity: wireframe, clean business prototype, high-fidelity branded prototype, screenshot restoration, or executive demo.
2. Gather evidence: user screenshots, brand guidelines, official site/app/mini-program, campaign/product pages, internal CRM/POS references, or design-reference search.
3. Deconstruct evidence: identify color, typography, component shape, imagery, density, copy tone, and navigation behavior.
4. Produce a brand visual token using `assets/templates/visual-token-template.json` when fidelity is branded or higher.
5. Define workbench balance: brand intensity, hero policy, accent budget, operational priority, module differentiation, and readability rules.
6. Define structural differentiation: navigation model, home composition, page architecture by module, information ordering, and signature interaction.
7. Define page capability contracts for home, customers, tasks, appointments, dashboard, and native WeCom handoff.
8. Apply the token to the adaptable page layer and bottom-navigation presentation. Keep shell mechanics and native replicas protected.
8. Run visual QA and, when a JSON token is saved, `scripts/check_visual_tokens.py`. For branded HTML prototypes, also run `scripts/check_workbench_implementation.py`.

If evidence is weak, do not overfit. Use a neutral operational base with a clearly labeled brand-adjacent accent.

## Shell Versus Page Design

Do not confuse shell consistency with visual sameness.

Protected shell layer:
- Desktop review stage and external role/journey controls.
- Mobile full-screen behavior and automatic responsive mode.
- WeCom mini-program container, top title bar, capsule, bottom-navigation mechanics, and safe-area behavior.
- Secondary-page bottom CTA anchoring.
- Native WeCom page replicas such as 新建群发.
- QA guardrails such as no emoji UI, no runtime FA/SA/BA selector, and no duplicated quick tools.

Adaptable page layer:
- Brand accent colors, typography weight, information density, card/list/table choices, section rhythm, and icon style.
- Module-specific layouts for home, customer list, C360, tasks, appointment, content library, dashboard, transfer, and extension modules.
- Visual hierarchy and copy tone based on the target industry and provided references.
- Data fields and labels, as long as project-specific names are not invented without source evidence.
- High-fidelity brand moments, product images, campaign assets, or executive-demo polish when the user provides enough material.
- Bottom-navigation item set, order, labels, icon treatment, active state, center-action policy, and material treatment within mini-program constraints.

## Structural Differentiation

Before coding, choose a structure rather than inheriting the template:

- Navigation model: 3-5 top-level destinations, order rationale, optional center action, role variation, and overflow strategy.
- Home composition: queue-first, customer-first, metric-first, appointment-first, campaign-to-task, manager overview, or another evidence-backed composition.
- C360 architecture: tabbed dossier, timeline-led profile, action-first concierge view, product-interest canvas, compact CRM sheet, or another suitable structure.
- Task architecture: checklist execution, target-progress worklist, content-preview workflow, conversation-led action, appointment conversion flow, or channel-specific structure.
- Appointment architecture: schedule-led, preparation-led, customer-context-led, resource-led, or outcome-led.
- Dashboard architecture: grouped scorecard, exception-first review, ranked team view, funnel-led analysis, or another role-appropriate pattern.
- Signature interaction: one useful brand-appropriate interaction, such as product shortlist, fitting preparation checklist, training-plan recommendation, clienteling script composer, or service ritual.

Do not use the same architecture labels as decorative themes. They must change information order, component type, or interaction path. Across multiple brand cases, vary at least navigation model, home composition, two detail-page architectures, and signature interaction.

If the user provides screenshots, brand references, or a design system, adapt the page layer to those references while preserving the protected shell. If there is no visual reference, use the neutral operational shell and vary page content through business structure, not decoration.

## Evidence Deconstruction

Before writing UI code, summarize:

- Source: screenshot, URL, file, reference search, user note, or assumption.
- Observable detail: color, typography, shape, border, shadow, density, image treatment, icon style, or copy tone.
- Prototype decision: CSS token, component rule, page layout rule, data/content rule, or explicit non-use.

Do not treat brand adjectives as enough. "Luxury", "premium", or "beauty" must become concrete choices such as restrained accent usage, exact or approximate palette, typography weight, card rhythm, image placement, and copy tone.

## Brand Token Application

When implementing HTML, map brand decisions into tokenized CSS first:

- `--brand-primary`, `--brand-primary-strong`, `--brand-accent`, `--brand-on-primary`.
- `--bg`, `--surface`, `--surface-soft`, `--line`, `--line-strong`, `--text`, `--muted`, `--subtle`.
- Keep destructive, warning, and disabled states legible and separate from brand accent colors.

Then apply tokens page by page:

- Home: brand moment, metrics, priority sections, campaign/product module, or executive-demo imagery if useful.
- Customers/C360: search/filter clarity, row density, tags, customer summary, preference/product-interest modules.
- Tasks: execution clarity, progress, channel labels, target grain, native handoff, and result states.
- Appointment: schedule/resource states, service detail, conflict/confirmation state, and clear CTAs.
- Content: product/campaign imagery when approved.
- Dashboard: operational KPI grouping, progress, target attainment, trend, and drilldown hierarchy.
- Transfer/extensions: permission, ownership, source system, and write-back clarity.

Never use brand skin as a reason to remove required search, filter, tabs, task result states, role behavior, or native WeCom handoff.

## Brand Expression Versus Workbench Utility

Strong brand visual design is desirable when the user asks for high fidelity. The balance rule is: brand expression should clarify priority and confidence, while the workbench keeps repeated tasks fast.

Use this hierarchy:

- **Can be expressive**: home hero, priority campaign, launch/drop module, premium customer state, content module, executive-demo path, dashboard highlight.
- **Should be balanced**: C360 summary, KPI cards, task cards, appointment cards, customer profile modules.
- **Must stay operational**: search, filters, tab controls, list rows, task due dates, target counts, action buttons, appointment time/resource rows, error/no-permission states, native WeCom replicas.

When a brand has loud evidence, contain it through an accent budget: one or two strong visual moments per page, then neutral operational surfaces. When a brand has quiet evidence, avoid making the UI bland; use precise typography, spacing, material detail, image discipline, and component rhythm as the brand anchors.

For every branded page, ask:

- What is the user's fastest next action on this page?
- Which one visual anchor makes the brand recognizable?
- Which brand treatment is deliberately avoided because it would slow scanning?
- Is the page structurally different because of its job, or only recolored?

Implementation proof checks:

- Home first viewport: show at least two workbench signals, such as priority clients, tasks, appointments, dashboard KPI, or campaign-to-task entry. A campaign/editorial hero alone is not a workbench.
- Customer list: keep search and filter/segment controls visible before customer rows.
- Task list: keep task type/status filters visible and show source/type, target grain, due/progress, and primary next action.
- Appointment: align time, customer, service/resource, owner/status, and action.
- Dashboard: preserve metric grouping, target/trend/period, and drilldown entry.
- Native WeCom handoff: keep native structure and recipient/message/frequency/send/return cues visible.

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
- Copying consumer fashion campaign home screens so literally that the clienteling workbench summary disappears.

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
- Applying executive-demo hero density to every workbench list page.

### 5. Jewelry / Watch High-Touch Service

Best for: jewelry, watches, high-value appointment retail, VIC/VIP service.

Characteristics:
- Precise typography and quiet spacing.
- Strong appointment, preference, product-interest, and concierge-service cues.
- Very limited accent color, high contrast, and strong detail discipline.
- Product imagery may be important, but only when approved or public.

Use role naming:
- Ask for the client-preferred term. Use SA or advisor if no industry-specific term is confirmed.

Avoid:
- Generic luxury gold wash.
- Large decorative hero blocks that crowd operational tasks.
- Treating high-value customers as an opportunity lifecycle unless the user confirms opportunity scope.

### 6. Athletic / Lifestyle Retail Launch Workbench

Best for: sportswear, lifestyle retail, drop/launch programs, community events.

Characteristics:
- Brand moments can be bold when tied to launches, drops, events, training, or priority client outreach.
- Typography, contrast, geometry, and campaign modules may be expressive.
- Customer, task, appointment, and dashboard pages still need fast scanning and clear execution.

Use role naming:
- Use the brand or source-backed frontline term when available. Otherwise use SA or advisor.

Avoid:
- Turning every page into a campaign page.
- Flooding the accent color across all cards and chips.
- Letting launch modules hide ordinary clienteling work.

### 7. Wellness / Community Retail Workbench

Best for: yoga, fitness community, wellness, class-based retail, service and event communities.

Characteristics:
- Calm typography, organic geometry, warm neutrals, and community/service cues can carry the brand.
- Strong accents are reserved for deadlines, event capacity, launch windows, or premium community states.
- Appointment, class, and community participation modules may be more important than product-heavy modules.

Use role naming:
- Use the brand or source-backed frontline term when available. Otherwise use SA or advisor.

Avoid:
- Forcing loud uppercase, black blocks, or cut-corner athletic styling without evidence.
- Making calm visual tone so soft that task priority and status disappear.

### 8. Wireframe / Requirement Handoff

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
- Brand visual token summary when fidelity is branded or higher.
- Workbench balance summary: brand intensity, hero policy, accent budget, and which surfaces must stay operational.
- Evidence table linking sources to UI decisions.
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
- Does each branded decision trace to evidence, an explicit assumption, or a selected style template?
- Does the brand skin stay in the adaptable page layer while shell/native WeCom surfaces remain protected?
- Does brand expression support the user's fastest next action instead of competing with it?
- Are expressive brand moments limited by an accent budget?
- Do high-frequency work surfaces remain dense, legible, and predictable?
- Do module layouts differ because the modules do different jobs, not only because colors changed?
- If a JSON visual token exists, does `scripts/check_visual_tokens.py` pass?
- For branded HTML, does `scripts/check_workbench_implementation.py` pass?

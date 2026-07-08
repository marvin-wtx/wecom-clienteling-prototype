# Brand Visual Extraction

Use this when a WeCom Clienteling prototype needs brand-aware UI generation, screenshot-informed visual restoration, or high-fidelity presentation polish.

## When To Use

Use this before implementation when the user provides or asks for:

- A brand name, public brand research, competitor/category examples, or style references.
- Brand guidelines, app/mini-program screenshots, CRM/POS screenshots, campaign pages, product pages, or design-system snippets.
- A high-fidelity branded prototype, executive demo, or close visual recreation of an existing UI.

Skip detailed extraction only for low-fidelity wireframes or pure business mapping. In that case, keep the neutral operational shell and state that brand styling is deferred.

## Evidence First

Do not jump from brand name to styling. First produce a compact evidence table:

| Source | Observable Detail | Prototype Decision |
| --- | --- | --- |
| Official site, app screenshot, campaign page, user screenshot, or reference search | Color, typography, component shape, image treatment, copy tone, density, icon style, navigation pattern | Token, component, layout, or content rule used in the prototype |

Rules:

- Use provided screenshots or brand material as strongest evidence.
- If researching publicly, separate observed facts from assumptions and generic defaults.
- Do not invent exact logo usage, product imagery, campaign copy, membership names, or proprietary colors when not provided or publicly visible.
- If evidence is weak, create a neutral brand-adjacent skin and mark it as an assumption.

## Brand Visual Token

Before a branded prototype is built, summarize the evidence into a brand visual token. Use `assets/templates/visual-token-template.json` as the schema.

Required sections:

- `brand`: name, industry, target fidelity, and frontline role term.
- `referenceSources`: URLs, files, screenshots, or notes used as evidence.
- `palette`: primary, primary strong, accent, background, surface, soft surface, text, muted text, line, danger, and on-primary colors.
- `typography`: font family, title/body weights, hierarchy, and density notes.
- `componentStyle`: card, chip, tab, CTA, list, filter, and bottom-sheet treatment.
- `componentStyle.geometry`: radius, cut-corner, border, and shape rules derived from evidence or industry fit.
- `componentStyle.accentRule`: where strong brand color is allowed and where it is forbidden.
- `componentStyle.anchor`: the primary and secondary visual anchors that make the brand recognizable.
- `workbenchBalance`: how brand expression stays balanced with search, task execution, appointments, dashboard scanning, and native handoff clarity.
- `imageryRules`: what imagery can be used, where it belongs, and what fallback is allowed.
- `layoutRhythm`: density, section spacing, card padding, list row height, and dashboard density.
- `shellBoundary`: what must remain protected in the WeCom shell versus what can be brand-skinned.
- `moduleAdaptation`: page-level rules for home, customers, C360, tasks, appointments, content, dashboard, transfer, and extension modules.
- `avoid`: visual mistakes to prevent.
- `assumptions`: unresolved or inferred choices.

If a token is saved as JSON, run:

```bash
python3 scripts/check_visual_tokens.py path/to/visual-token.json
```

## Brand Depth And Workbench Balance

Color swapping alone is not a brand prototype. Before implementation, answer these depth questions and write the answers into the visual token:

1. **Typography hierarchy**: define `display`, `h1`, `h2`, `num`, and `eyebrow`. Do not hard-code one style such as all-caps 900 weight. Use brand evidence and Chinese label readability to choose size, weight, tracking, line height, and transform.
2. **Geometry system**: define `controlRadius`, `cardRadius`, `useClipPath`, `clipCorner`, `borderWeight`, and a short rationale. Sharp corners, cut corners, soft radius, editorial spacing, and precise luxury geometry are all valid only when evidence or industry fit supports them.
3. **Accent rule**: list concrete `useCases` and `avoid` cases. Strong brand colors should mark priority, urgency, premium states, campaign modules, or selection states. They should not flood every card, hide filters, or weaken primary task actions.
4. **Visual anchors**: define `primaryAnchor` and `secondaryAnchor`. Anchors may be typography, imagery, a product/campaign module, a metric display, spacing, material detail, or controlled color blocks. Do not assume black blocks, large numbers, or clipped cards are universal.
5. **Workbench balance**: define `brandIntensity`, `heroPolicy`, `operationalPriority`, `accentBudget`, `moduleDifferentiation`, `pageLayerOnly`, and `readabilityRules`.

The target balance is not neutral blandness. A high-fidelity brand prototype can be expressive, but brand expression must help the reviewer understand the work. If a branded hero, campaign block, or product image competes with search, filters, task due dates, target grain, appointment time, or KPI drilldown, reduce the brand treatment or move it to a lower-priority module.

Use this intensity guide:

- **Restrained**: business alignment, IT review, early scope validation, weak brand evidence.
- **Balanced**: default for branded workbench prototypes. Brand is recognizable, but daily work remains faster to scan than visual moments.
- **Expressive**: executive demo, launch journey, strong evidence and assets. Still keep customer lists, task execution, appointments, dashboards, and native WeCom replicas operational.

## Matching Modes

Choose one mode explicitly:

- **Tone match**: use brand mood, color discipline, and copy tone without copying a specific UI.
- **Component match**: adapt observed component details such as cards, chips, buttons, tabs, or list density.
- **Screenshot restoration**: recreate a supplied screen closely while preserving the WeCom shell and clienteling business logic.

For screenshot restoration, state which parts are protected shell, which parts are copied structurally, and which parts are interpreted.

## Applying Tokens To The Shell

Keep the shell protected:

- Phone frame, status bar, mini-program nav, capsule, bottom tabs, role/journey controls, mobile/desktop behavior, native replicas, and sticky CTA behavior are not redesigned.

Apply brand skin to the page layer:

- Use CSS variables such as `--brand-primary`, `--brand-primary-strong`, `--brand-accent`, `--brand-on-primary`, `--bg`, `--surface`, `--surface-soft`, `--line`, `--text`, and `--muted`.
- Use imagery in content areas, customer/product cards, content library, campaign modules, and executive-demo moments.
- Use brand typography weight and spacing within compact operational limits.
- Apply stronger brand treatment to page moments that benefit from it: home priority module, campaign/content module, premium customer state, dashboard highlight, or executive journey.
- Keep high-frequency work surfaces efficient: customer lists, task lists, task detail actions, appointment rows, filters, and no-permission/error states should remain dense, legible, and predictable.
- Keep native WeCom replicas visually neutral and native-like. Do not brand-redesign native compose/send pages.

## Industry Starting Points

- Fashion/luxury: controlled palette, sparse hierarchy, restrained accents, selective product/customer imagery, FA term unless overridden.
- Beauty/personal care: BA term unless overridden, product/category imagery, consultation/replenishment cues, softer but high-contrast surfaces.
- Jewelry/watch: high-touch service tone, appointment and product-interest emphasis, precise typography, low-noise premium accents.
- General retail/service: SA or advisor term, practical workbench density, strong search/filter/list affordances.
- Athletic/lifestyle retail: expressive campaign or launch modules can be strong, but lists and task execution must remain operational.
- Wellness/fitness/yoga: softer geometry, calmer hierarchy, and community/service cues can carry the brand; do not force loud display typography or black blocks unless evidenced.
- Executive demo: more polish and curated content, but no missing business coverage hidden by visuals.

## Visual QA

Before delivery, check:

- Every branded decision traces to a source, an explicit assumption, or a style template.
- Brand skin changes page layer only; shell geometry and native WeCom replicas remain intact.
- Palette is not a one-hue wash; neutral surfaces and readable text contrast are preserved.
- Icons are SVG/library icons, not emoji.
- Product/campaign imagery is used only when provided, public, or clearly marked as placeholder.
- Module layouts are visually adapted to their job; the prototype is not the same card repeated with new colors.
- Brand intensity is balanced with workbench clarity: search/filter, task execution, appointment timing, dashboard drilldown, and native handoff stay faster to understand than decorative elements.

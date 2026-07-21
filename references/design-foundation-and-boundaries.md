# Design foundation and boundaries · V4.0

Use this only after the neutral mobile product passes.

## Evidence and interaction

Run one grouped design intake. Ask for available brand assets, intended tone, density, imagery level, fidelity target, and explicit dislikes. Recommend one direction. Do not make the user specify CSS or component details.

Design two to four representative screens before the full product. Prefer the workbench, a customer screen, and a primary-Journey screen when those modules exist. Show them in a visible browser and wait for user acceptance.

## Awesome DESIGN.md boundary

[Awesome DESIGN.md](https://github.com/VoltAgent/awesome-design-md) is an MIT-licensed index of externally hosted DESIGN.md analyses. It can strengthen brand expression but does not define retail clienteling UX.

Allowed extraction:

- color roles and contrast strategy;
- typography families, weights, rhythm, and density;
- atmosphere, geometry, surface, depth, and imagery treatment;
- documented responsive and touch principles.

Forbidden transfer:

- marketing-site IA, hero order, desktop navigation, or page templates;
- source-site copy, business objects, journeys, metrics, or data;
- logos, proprietary fonts, identity assets, or copyrighted imagery without supplied permission;
- another brand's visual identity unless the user explicitly selects it as an analogue.

Record the URL, exact-brand or user-selected-analogue basis, adopted aspects, and rejected aspects in `docs/design-intake.json`. Treat an unavailable remote reference as optional; fall back to official sources and the local foundation.

## Protected UX versus adaptable expression

Protect:

- page purpose, semantic grouping, required content, action order, and state meaning;
- selected/disabled/error/empty/success states;
- minimum 44px touch targets, scroll containers, sticky actions, and bottom navigation;
- back-context preservation and all state transitions;
- the frozen native WeCom page and mobile/review-shell boundary.

Adapt:

- brand tokens, typography within readable limits, spacing within density limits;
- card and control geometry, borders, surface material, depth, and motion;
- imagery placement where it does not precede or compete with the primary work action;
- emphasis treatments that preserve the same semantic priority.

Design may change how the product is perceived. It may not change how the user understands the work, completes the action, or confirms the result.

## Component use

Read `assets/design-foundation/component-ux-contracts.json` before styling. Open `assets/design-foundation/component-reference.html` in a visible browser when selecting baseline hierarchy and states. Treat it as a floor, not a theme to clone.

Every used baseline component must expose `data-ux-component`. Mark meaningful rendered states with `data-ux-state`. A visual change fails if it removes required content, collapses distinct states, weakens the primary action, introduces an inert control, or changes business transitions.

## Visual acceptance

Accept representative screens only when all are true:

- work and primary action are recognizable within three seconds;
- brand expression is traceable to evidence or a confirmed analogue;
- list, detail, selection, empty, and result states remain distinct;
- repeated components are visually and behaviorally consistent;
- the mobile screen remains readable and operable at 390 × 844;
- no page, field, action, or transition changed from the accepted functional build.

Static documents are not visual proof. Record user acceptance and representative screenshots, then perform final visible-browser acceptance on the completed build.

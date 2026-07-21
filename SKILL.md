---
name: wecom-clienteling-prototype
description: Turn a brand prompt or supplied WeCom clienteling materials into a scoped, operable retail clienteling prototype. Use for workbenches, customer lists and profiles, membership, C360, tasks, appointments, performance, asset tools, native WeCom execution, multi-role review, visual design, or prototype QA.
---

# WeCom Clienteling Prototype · V4.0

Build a credible clienteling product in stages. Confirm the product frame before creating pages; validate mobile business structure before brand design; add desktop review controls only after the mobile product passes.

## Do not clone a prior product

Use FSN only as the source of transferable domain principles. Never copy its pages, data, role names, fields, metrics, rules, IA, or visual composition into another brand. `assets/prototype-shell/` supplies runtime mechanics only.

Read `references/clienteling-domain-blueprint.md` before scoping. Read `references/operating-language.md` before writing UI copy. Read `references/native-wecom-broadcast-contract.md` before implementing native group send.

## Stage 0 · Run one scope intake before creating files

Do not create HTML, tokens, screenshots, or QA documents from the first sparse prompt.

Use `assets/templates/scope-intake-template.json` to play back:

- brand and supplied sources;
- primary role;
- selected modules and second-level pages;
- primary Journey;
- whether other selected pages need a complete loop or clickable structure;
- the demo-data policy.

Show the exact selected second-level page list, primary Journey, depth, and estimated page count in the playback. Never hide an expanded scope behind “standard modules.” If more than 12 pages are requested as complete loops, obtain explicit expansion confirmation after showing the exact list.

When the prompt only names a brand, ask one grouped question with recommended defaults. When the prompt already names modules, preserve them and ask only what materially changes role, Journey priority, or depth. If the user explicitly accepts all recommended defaults, continue without another question.

Use a compact playback such as: “我会先按客户顾问的通用零售框架制作：首页工作台与今日事项、客户列表/详情/会员/交易/互动、任务列表/详情/企微触达、邀约、个人业绩与素材库；主链路优先跑通任务到企微发送。请一次告诉我要删加的模块、主要角色，以及其他页面是否也要完整闭环。” Do not turn this into a long questionnaire.

Never drop a module explicitly named by the user because it is outside the recommended framework. Record it in `extensions` with `source: user-request`, confirm its second-level pages and depth in the same intake, and carry it through the blueprint and page-state contract. The common module contract supplies no invented fields for an extension; use only user-supplied facts plus neutral structural labels.

Classify the confirmed scope as:

- `framework-default`: recommended standard retail demo frame;
- `module-scoped-demo`: user-selected modules with common structures and mock values;
- `source-grounded`: supplied material defines brand-specific fields, roles, rules, or workflows.

Save the confirmed result as `docs/scope-intake.json`. Do not start Stage 1 without it.

## Stage 1 · Create the business blueprint

Create `docs/business-blueprint.json` from `assets/templates/business-blueprint-template.json`.

Use `assets/templates/common-retail-module-contracts.json` for selected pages. These contracts may supply common structures and plain mock fields such as basic customer information, example membership tier, transactions, interactions, task status, appointment details, performance summaries, and asset metadata.

Every field or claim must use one provenance:

- `user-source`: explicitly requested or supported by supplied materials;
- `common-structure`: reusable product structure defined by this skill;
- `mock-value`: visibly demonstrative value;
- `public-brand`: public visual or verbal brand material; never business logic;
- `runtime`: value created by user interaction;
- `unsupported`: forbidden.

Record every brand-like visible mock in `visibleMockClaims` with its scope authorization and visible disclosure. Render its `data-visible-claim` and `data-content-provenance` markers. Public product names may label public content or user-authorized mock tone; they do not authorize internal tiers, KPI rules, task sources, appointment resources, or recommendations.

Module selection authorizes that module, not brand-specific rules. Never turn mock membership tiers, task sources, customer segments, consent, KPI definitions, appointment resources, permissions, or CRM write-back into claims about the brand.

## Stage 2 · Define pages and state before HTML

Create `docs/page-state-contract.json` from `assets/templates/page-state-contract-template.json`.

- Include every selected second-level page and no unselected module.
- Give every page one purpose, required information, primary action, and incoming/outgoing state.
- Mark the depth of each page as `complete-loop` or `clickable-structure`.
- Pick at least one complete primary Journey.
- Keep selected IDs stable across pages.

The standard primary Journey is:

`今日任务 → 客户与素材 → 新建群发 → 结果确认`

It is one Journey inside the product, not the whole product. The result may show only facts produced by the send receipt. Do not invent read status, replies, appointments, follow-up rules, or CRM updates after send.

Run the scope, blueprint, and page-contract gates before creating HTML.

## Stage 3 · Build the mobile functional prototype

Seed the protected runtime with `scripts/seed_runtime_shell.py`, then implement the confirmed mobile IA with neutral or weak branding.

- Build every selected page to its confirmed depth.
- Mark each implemented page with `data-page-id`, `data-module`, `data-selection`, and `data-page-depth`; mark every contracted common field with `data-common-field` so the build can be checked against the confirmed scope.
- Attach page, field, component, and state markers only to content rendered inside `#app` for the corresponding route. Markers inside `<template>`, comments, scripts, hidden containers, zero-size marker-only elements, review metadata, or outside the currently rendered product page do not count and must fail validation.
- Make every visible control work. A visible control works only when it produces an observable, semantically correct result: search changes the displayed records, filters change active state and records, detail actions open the selected object ID, selection persists, cancel returns to the correct source, and a button may not navigate to its current route unless it also creates a meaningful state change.
- Keep common fields plain and demonstrative; mark the product once as using demo data. Separate structure provenance from value provenance: a wrapper may mark `data-common-field`, but visible mock names, mock metrics, mock tiers, sample locations, advisor names, and generated examples need `data-content-provenance="mock-value"`; public brand words need `data-content-provenance="public-brand"`.
- Preserve source context and selected object IDs on navigation. Detail pages must read the clicked row's ID instead of defaulting to the first record.
- Complete the primary Journey end to end.
- Do not add desktop review controls, visual rationale, or multi-Journey HUD inside the phone.

Minimum `clickable-structure` standard: the page must be reachable through a semantically correct route, render its contracted fields at runtime inside `#app`, use incoming selected IDs, implement every visible control, preserve filters/source context, include default plus one meaningful state when the page has state, and avoid a generic key-value layout when the page contract requires a distinct hierarchy.

Use the frozen native group-send page only for recipient count, message, image or mini-program material, material selection, cancel, and send completion. Mount `renderWecomExecute()` directly in `#app`; never wrap it in an app shell or `.wx-nav`.

Validate this stage in a visible browser before visual design.

## Stage 4 · Confirm and apply brand design

Start only after the functional mobile prototype passes. Read `references/design-foundation-and-boundaries.md`. Use `assets/design-foundation/component-ux-contracts.json`, `assets/design-foundation/page-composition-recipes.json`, and `assets/design-foundation/component-reference.html` as the executable UX foundation.

### 4A · Run one design intake

Create `docs/design-intake.json` from `assets/templates/design-intake-template.json`. Ask one grouped question covering available brand assets, desired tone and density, imagery level, fidelity target, and disliked patterns. Recommend a direction instead of asking the user to design the interface. Show and confirm this intake before creating representative branded screens; do not merge design intake with design acceptance.

Use design evidence in this order:

1. supplied brand guidelines, UI screenshots, or design files;
2. the exact brand's official public sources;
3. Lazyweb when available;
4. an exact-brand entry in [Awesome DESIGN.md](https://github.com/VoltAgent/awesome-design-md);
5. the skill's generic component foundation.

Awesome DESIGN.md is an optional visual-language reference, not a runtime dependency or UX source. Adopt only color roles, typography rhythm, atmosphere, geometry, depth, imagery treatment, and documented responsive principles. Never copy its marketing IA, desktop navigation, content, business rules, or branded identity assets. Never silently use another brand as an analogue; require the user to select that analogue in the design intake.

### 4B · Design representative screens first

Apply the confirmed direction to two to four representative screens: one home/workbench screen when selected, one customer screen when selected, and at least one primary-Journey screen. Preserve the accepted functional screen as the structural source of truth.

- Copy `shell-runtime.js`, `layout-audit.js`, and `workbench-visual-primitives.css` unchanged. Apply brand expression through variables and project CSS.
- Build from a matching composition recipe; do not recreate the page shell, scrolling, sticky actions, bottom navigation, or protected component structure.
- Create `docs/component-usage.json` from the template during representative design, but do not leave it representative-only. It must include `representativePageIds` and one `pages[]` design-mapping entry for every selected page before release.
- Mark baseline components with `data-ux-component` and meaningful states with `data-ux-state`; in `?review=1`, expose the components actually rendered outside the phone.
- Preserve semantic grouping, action order, required states, touch targets, scroll behavior, state transitions, and frozen native UI.
- Vary brand tokens, typography, density within limits, imagery, surface material, geometry, and motion only where the component contract permits.
- Use real supplied assets or generated image assets; do not handcraft SVG, CSS, text-symbol, or placeholder art as product imagery.

Before asking for acceptance, run every representative page at 390 × 844 in visible Google Chrome and save `window.__wecomLayoutReport` to `docs/representative-layout-review.json`. Reject overlap, horizontal overflow, controls under 44px, broken or placeholder assets, unbound counters, and native shell nesting. Then show the representative screens and ask for acceptance before styling the remaining pages. Save the decision as `docs/design-acceptance.json`; do not self-approve on the user's behalf.

### 4C · Extend the accepted design

After explicit user design acceptance, apply the direction to every selected page without changing approved pages, objects, fields, or transitions. Do not style remaining pages when `docs/design-acceptance.json` is missing, `accepted` is not true, `acceptedBy` is not `user`, or `remainingPagesMayBeStyled` is not true.

For every selected page, create a page-level design mapping in `docs/component-usage.json` before writing final CSS/HTML. Each mapping must name the page's `recipe`, `informationHero`, `primaryAction`, `stateCoverage`, `components`, `brandOverrides`, and a short `compositionRationale`. Use `assets/design-foundation/page-composition-recipes.json`; if no recipe fits, stop and add a general reusable recipe to the skill instead of improvising a white-card page.

The full product must not degrade into one repeated card/list/table pattern. Common pages need distinct composition intent:

- customer list: search/filter as the working control, segmented filters with active and clear states, rows with identity plus decision context;
- customer detail sections: membership, transactions, and interactions must each have their own information hero and state pattern, not only a three-row key/value table;
- task list and task detail: status, due time, related customer, and next action must drive the hierarchy;
- appointments: list, detail, and create must separate schedule context, customer identity, editable choice, and confirmation state;
- performance: personal performance and task performance are separate selected pages when both are contracted; a button may not loop back to the same page;
- asset library: search/filter, preview/selection, asset type, selected state, and broken-image fallback must be visibly designed;
- result pages: show only runtime facts and use a distinct success/empty/error state.

Compare each styled screen against its accepted functional counterpart and rerun the business gates before release. A functional structure can pass while the branded prototype still fails; the expected delivery is a brand-aware, polished product prototype, not a complete set of generic fields.

## Stage 5 · Add the delivery console

Add desktop/mobile presentation and optional role/Journey controls only after mobile business and recorded design acceptance.

- Show only roles and Journeys implemented and tested in the phone product.
- Keep all review controls outside the phone and behind `?review=1`.
- Keep normal `?view=desktop` free of version, prototype, QA, and review language.
- Never let the console change mobile routes, data, or product behavior.

## Stage 6 · Record browser acceptance

Record one concise `docs/prototype-delivery-review.json` bound to the tested URL and build hash. In visible Chrome verify and screenshot every selected page, not only representative screens or the primary Journey:

- first mobile viewport and responsive desktop phone;
- scroll and navigation;
- every selected page and visible control, with runtime evidence that `#app [data-page-id]` equals the expected page after navigation;
- the primary Journey, selected object IDs, and state persistence;
- native cancel/send behavior;
- console errors and broken images;
- page-specific visual hierarchy, component reuse, CTA placement, sticky-action clearance, bottom-tab clearance, empty/success/error states, and whether the page still reads as a designed product screen rather than a generic card stack.

Static documents are inputs or gates, never quality proof. Token, review, or case-evaluation files cannot substitute for visible Chrome screenshots and observed behavior. Save runtime evidence in `docs/prototype-delivery-review.json`: `runtimePages`, `testedControlsByPage`, `controlAssertions`, `objectIdentityAssertions`, and `provenanceSamples`.

## Release gates

Run, in order:

```bash
python3 scripts/check_scope_intake.py case-directory
python3 scripts/check_business_blueprint.py case-directory
python3 scripts/check_page_state_contract.py case-directory
python3 scripts/check_blueprint_implementation.py case-directory
python3 scripts/check_design_intake.py case-directory
python3 scripts/check_design_foundation_implementation.py case-directory
python3 scripts/check_component_usage.py case-directory
python3 scripts/check_representative_layout_review.py case-directory
python3 scripts/check_design_acceptance.py case-directory
python3 scripts/check_prototype_delivery_bundle.py case-directory
python3 scripts/check_skill_version_consistency.py path/to/wecom-clienteling-prototype
```

Reject a delivery that hid the exact page list, skipped either intake, merged design intake with acceptance, styled all pages before representative-screen acceptance, recreated protected UI-kit mechanics, silently borrowed another brand, changed protected UX structure, generated unselected modules, used marker-only templates, used unsupported or untraceable brand claims, used placeholder product imagery, left visible controls inert, allowed sticky actions to cover content, dropped selected object IDs, made a detail action always open the first record, made a filter or preview button navigate to the wrong module, or wrapped native group send in a business shell.

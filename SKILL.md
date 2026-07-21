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
- Make every visible control work.
- Keep common fields plain and demonstrative; mark the product once as using demo data.
- Preserve source context on back navigation.
- Complete the primary Journey end to end.
- Do not add desktop review controls, visual rationale, or multi-Journey HUD inside the phone.

Use the frozen native group-send page only for recipient count, message, image or mini-program material, material selection, cancel, and send completion. Mount `renderWecomExecute()` directly in `#app`; never wrap it in an app shell or `.wx-nav`.

Validate this stage in a visible browser before visual design.

## Stage 4 · Confirm and apply brand design

Start only after the functional mobile prototype passes. Read `references/design-foundation-and-boundaries.md` and use `assets/design-foundation/component-ux-contracts.json` plus `assets/design-foundation/component-reference.html` as the UX and component baseline.

### 4A · Run one design intake

Create `docs/design-intake.json` from `assets/templates/design-intake-template.json`. Ask one grouped question covering available brand assets, desired tone and density, imagery level, fidelity target, and disliked patterns. Recommend a direction instead of asking the user to design the interface.

Use design evidence in this order:

1. supplied brand guidelines, UI screenshots, or design files;
2. the exact brand's official public sources;
3. Lazyweb when available;
4. an exact-brand entry in [Awesome DESIGN.md](https://github.com/VoltAgent/awesome-design-md);
5. the skill's generic component foundation.

Awesome DESIGN.md is an optional visual-language reference, not a runtime dependency or UX source. Adopt only color roles, typography rhythm, atmosphere, geometry, depth, imagery treatment, and documented responsive principles. Never copy its marketing IA, desktop navigation, content, business rules, or branded identity assets. Never silently use another brand as an analogue; require the user to select that analogue in the design intake.

### 4B · Design representative screens first

Apply the confirmed direction to two to four representative screens: one home/workbench screen when selected, one customer screen when selected, and at least one primary-Journey screen. Preserve the accepted functional screen as the structural source of truth.

- Mark baseline components with `data-ux-component` and meaningful states with `data-ux-state`.
- Preserve semantic grouping, action order, required states, touch targets, scroll behavior, state transitions, and frozen native UI.
- Vary brand tokens, typography, density within limits, imagery, surface material, geometry, and motion only where the component contract permits.
- Use real supplied assets or generated image assets; do not handcraft SVG, CSS, text-symbol, or placeholder art as product imagery.

Show the representative screens in a visible browser and ask for acceptance before styling the remaining pages. Save the decision as `docs/design-acceptance.json`; do not self-approve on the user's behalf.

### 4C · Extend the accepted design

After design acceptance, apply the direction to every selected page without changing approved pages, objects, fields, or transitions. Compare each styled screen against its accepted functional counterpart and rerun the business gates before release.

## Stage 5 · Add the delivery console

Add desktop/mobile presentation and optional role/Journey controls only after mobile business and recorded design acceptance.

- Show only roles and Journeys implemented and tested in the phone product.
- Keep all review controls outside the phone and behind `?review=1`.
- Keep normal `?view=desktop` free of version, prototype, QA, and review language.
- Never let the console change mobile routes, data, or product behavior.

## Stage 6 · Record browser acceptance

Record one concise `docs/prototype-delivery-review.json` bound to the tested URL and build hash. In visible Chrome verify:

- first mobile viewport and responsive desktop phone;
- scroll and navigation;
- every selected page and visible control;
- the primary Journey and state persistence;
- native cancel/send behavior;
- console errors and broken images.

Static documents are inputs or gates, never quality proof.

## Release gates

Run, in order:

```bash
python3 scripts/check_scope_intake.py case-directory
python3 scripts/check_business_blueprint.py case-directory
python3 scripts/check_page_state_contract.py case-directory
python3 scripts/check_blueprint_implementation.py case-directory
python3 scripts/check_design_intake.py case-directory
python3 scripts/check_design_foundation_implementation.py case-directory
python3 scripts/check_design_acceptance.py case-directory
python3 scripts/check_prototype_delivery_bundle.py case-directory
python3 scripts/check_skill_version_consistency.py path/to/wecom-clienteling-prototype
```

Reject a delivery that skipped either intake, styled all pages before representative-screen acceptance, silently borrowed another brand, changed protected UX structure, generated unselected modules, used unsupported brand claims, left visible controls inert, or wrapped native group send in a business shell.

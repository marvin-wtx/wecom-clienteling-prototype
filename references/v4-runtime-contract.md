# V4.0 Runtime Contract

The runtime protects viewport, scroll, navigation, safe-area, sticky-action, and review-console mechanics. It does not define the project IA.

Before seeding it, complete:

1. `docs/scope-intake.json`;
2. `docs/business-blueprint.json`;
3. `docs/page-state-contract.json`.

The shell must implement those contracts rather than rationalise a prebuilt app. Keep `#app` at full height; route pages fill it; only page bodies scroll. Normal desktop mode remains product-only, and review controls stay outside the phone.

Release blockers include copied applications, brand-name substitution over unchanged page composition, unselected modules, unsupported brand rules, shell preview content, dead controls, and native group send wrapped in business navigation.

# Evidence And Implementation Integrity

Use this for every branded prototype, whether the user supplies rich source material or only a brand name.

## Evidence Priority

Use evidence in this order:

1. User-provided business requirements, screenshots, field lists, flows, terminology, and approved assets.
2. User-provided brand guidelines or design system.
3. Official public brand sources for public-facing visual facts, product categories, services, locations, and terminology.
4. Generic WeCom Clienteling baseline concepts.
5. Explicit assumptions that remain outside the delivered UI until confirmed.

Public brand marketing does not prove internal CRM fields, customer tiers, campaign names, task types, rooms, advisor workflows, or membership programs.

## Evidence Ledger

For every branded concept that affects UI copy, navigation, segmentation, task logic, service types, content assets, or signature interactions, record:

- Stable claim ID.
- Claim or term.
- Category: `visual`, `public-brand`, `business`, `terminology`, `asset`, or `interaction`.
- Status: `user-confirmed`, `official-public`, `generic-default`, or `assumption`.
- Source reference.
- Whether the claim is allowed in the delivered UI.
- Neutral fallback.

Rules:

- `assumption` claims are not allowed in UI.
- `user-confirmed` requires a user-provided file, screenshot, URL annotated by the user, quoted requirement, or explicit user statement. AI inference, public research, industry convention, and prior-case material can never use this status.
- `official-public` may support public product/service terminology, but not internal business systems.
- Internal-sounding segments, rooms, programs, workflows, or operational names require `user-confirmed`; otherwise use a neutral fallback.
- Do not describe competitor or category patterns as facts about the target brand.
- Do not use a source label such as "official website" without a specific page, screenshot, or user artifact.
- Treat vague source references such as `industry standard`, `common segment`, `public program`, or another prototype as insufficient for internal business terminology.

## Brand Isolation

Before delivery, list carryover terms from recent cases that must not appear. This includes prior brand names, campaigns, slogans, product categories, roles, segments, content assets, and signature interactions.

Search the prototype and token for all disallowed carryover terms.

## Implementation Contract

Bind the structural differentiation plan to the HTML:

- `data-layout-mode="<mode>"` on the page application root.
- `data-business-axis="<id>"` on the home operational root.
- `data-nav-model="<id>"` on the rendered bottom navigation.
- `data-page-architecture="<id>"` on home, customer detail, task detail, and appointment detail roots.
- `data-module-grammar="<id>"` on visible home, customer, task, and appointment structures.
- `data-signature-interaction="<id>"` on the functional signature interaction.

The visual token must carry the same IDs. Navigation labels in the token must match the implemented tab labels and order.

Do not add markers to unused or hidden duplicate elements. They must identify the visible implementation.

## Rendered Truth

In the browser:

- Compare actual navigation labels/order against the token.
- Confirm the signature interaction exists and changes state or route.
- Confirm each declared page architecture visibly changes information order or component structure.
- Check that the page is not a previous case with renamed classes and copy.
- Read every prominent brand/business term and verify its evidence status.

## Multi-Brand Similarity

When multiple brand cases are available:

- Compare home, C360, task detail, and appointment structures.
- Reject cases that preserve the same module order and tag sequence while changing only class prefixes, typography, colors, or labels.
- Require at least three structural differences across navigation, home composition, detail architecture, and signature interaction.
- Run `scripts/check_structural_similarity.py` with available prior cases.

# Prototype Delivery Discipline

Use this for every branded HTML/clickable prototype. It turns the skill into a repeatable delivery line so weaker agents cannot skip the hard thinking, while stronger agents still have room to create distinctive structures.

## Delivery Positioning

The deliverable is a **brand-aware WeCom Clienteling demo prototype plus solution blueprint**.

It is not:

- a consumer shopping app;
- a brand campaign microsite;
- a generic SaaS dashboard;
- a final production frontend;
- a full CRM/CDP specification;
- a literal copy of a public brand website.

The prototype must help a reviewer understand how frontline or manager users operate customers, tasks, appointments, content, native WeCom handoffs, and follow-up results for this brand.

## Required Delivery Recipe

Do not jump directly from prompt to screens. Complete these stages in order:

1. `evidence`: evidence ledger, source priority, assumption terms, and carryover bans.
2. `structure`: layout authority, at least three directions when open-generative, selected direction, rejected directions, and structure DNA.
3. `productLogic`: business axis, role, core journeys, page inventory, native handoff boundaries, and why this is a WeCom Clienteling workbench.
4. `dataModel`: connected customers, tasks, appointments, assets, metrics, roles, states, and IDs.
5. `pageContracts`: A/B/C page depth, required decision dimensions, page-specific module grammar, and action/result states.
6. `prototype`: HTML/clickable implementation from the protected V3 shell kit, with its preview removed and replaced by the project data, routes, navigation, page architecture, and interactions.
7. `qa`: automated checks, rendered checks, screenshot-backed case evaluation, self-critique, and delivery review.

If a stage is not applicable, record why. Missing stages are delivery blockers. A branded HTML/clickable release is a directory bundle, not a bare page: it contains `prototype/index.html`, visual token, delivery review, case evaluation, and the screenshot files the evaluation cites.

## Minimum Quality Bar

Before delivery, rate the prototype from 1 to 5 on:

- `brandFit`: the page layer reflects evidence-backed brand cues without turning into a campaign page.
- `workbenchUsability`: daily work, search, filters, task actions, appointment facts, and KPI drilldowns remain fast to scan.
- `businessCredibility`: sample data, states, native handoffs, and role differences can support a real clienteling conversation.
- `structuralOriginality`: navigation, home composition, detail architectures, and signature interaction are not just the starter shell with new colors.
- `evidenceIntegrity`: user-confirmed, official-public, generic-default, and assumption claims are separated correctly.
- `demoReadiness`: a presenter can explain the business flow, tradeoffs, and assumptions without apologizing for empty or decorative pages.

No item may be below 4 for a deliverable described as final or ready.

## Anti-Generic Failure Modes

Reject the prototype if any of these appear:

- The home page is always `今日经营 -> 优先客户 -> 今日任务 -> 预约`.
- The bottom navigation always keeps the starter five items and order without a role/journey rationale.
- C360, task detail, and appointment detail are summary cards plus one CTA.
- Page differentiation is only color, font, class prefix, or logo placement.
- Brand marketing vocabulary is used as internal CRM/customer terminology without user evidence.
- A campaign/editorial hero consumes the first viewport while operational work is pushed below it.
- Every module uses the same card grammar regardless of whether the job is triage, execution, dossier, timeline, or dashboard review.
- The prototype would still look like the same case after removing brand name, palette, and image references.

## Self-Critique Gate

Before delivery, answer these in a compact review:

1. What is the strongest structural difference from the starter shell?
2. What is the strongest structural difference from the most similar prior case?
3. Which module best expresses this brand's clienteling model, and why?
4. Which page would fail first in a real demo if its information were thinner?
5. Which visible terms are evidence-backed, and which assumptions were kept out of UI?
6. If palette, logo, and brand name were removed, what would still make this prototype structurally distinct?

Weak answers are blockers. Rewrite the prototype or token before delivery.

## Evidence-Backed Release Review

After rendered QA, create the case evaluation from `prototype-case-evaluation-template.json`.

- Capture real browser screenshots for home, C360, task detail, and appointment detail, or record a concrete scope exception.
- Record at least three interactions that change route, state, result, handoff, or write-back behavior.
- Score brand expression, workbench clarity, information depth, structural distinctness, and demo coherence against visible evidence.
- When prior cases exist, compare against each one and explain material operating differences. The same archetype requires four high-impact differences.

Run `check_prototype_case_evaluation.py`; run `check_portfolio_diversity.py` for every prior case. Passing static checks without screenshot-backed evidence is incomplete.

## Strong-Agent Creative Space

High-level agents may create stronger variety by changing business logic, not decorative treatment:

- make appointments, service, content, loyalty, product interest, replenishment, event attendance, manager exceptions, or relationship repair the business axis when evidence supports it;
- redesign navigation count, order, and center action around the dominant journey;
- change home narrative from queue to radar, agenda, cockpit, dossier, exception review, service calendar, or relationship pulse;
- use different module grammars per page, such as matrix, timeline, split view, checklist, canvas, ranked ledger, or progressive disclosure;
- invent a useful signature interaction that changes state, route, or result capture, while keeping unconfirmed brand-internal terms out of UI.

Creativity must still pass evidence, shell, page-depth, workbench, rendered QA, and `check_prototype_delivery_bundle.py` gates. The V2 demo and V3 shell-kit preview are not valid final product UI.

For open-generative or evidence-derived branded work, also complete the creative divergence system. The delivery review should be able to name the operating metaphor, the transposed inspiration mechanisms, the four or more high-impact levers, and the debranded difference.

# Prototype Execution Brief

## Objective

[State the business and prototype goal.]

## Channel Premise

- Product surface: WeCom ecosystem mini-program / embedded mobile workbench
- Desktop usage: review/demo stage only, not production primary surface
- Mobile usage: full-screen mini-program-style experience

## Source Material

- [Authoritative file/source]
- [Supporting file/source]

## In Scope

- [Capability/module]

## Conditional / Advanced Scope

- Opportunity follow-up: excluded / consult / included
- Trigger evidence:
- Decision:

## Out Of Scope

- [Excluded module or deferred detail]

## Roles

| Role | Needs | Permissions / Visibility |
|---|---|---|
| [Role] | [Need] | [Permission] |

## Terminology

- Industry:
- Frontline role term: FA / SA / BA / advisor / other
- Manager role terms:
- Language mode:
- Terms to avoid:

## Field Vocabulary

| Field Role | Confirmed Label | Source / Assumption | UI Usage |
|---|---|---|---|
| Customer identifier | [Neutral label or client label] | [Source] | [Search/C360/dashboard/task] |
| Member identifier | [Neutral label or client label] | [Source] | [Search/C360/member profile] |
| Contact method | [Neutral label or client label] | [Source] | [Search/contact action] |
| Customer grouping | [Neutral label or client label] | [Source] | [Filter/C360/dashboard] |
| Member level | [Neutral label or client label] | [Source] | [Filter/C360/member profile] |
| Profile label | [Neutral label or client label] | [Source] | [C360/filter/task targeting] |
| Lifecycle state | [Neutral label or client label] | [Source] | [C360/filter/task targeting] |

## Required Demo Flows

| Flow | Actor | Trigger | Start | Result | Exceptions |
|---|---|---|---|---|---|
| [Flow] | [Actor] | [Trigger] | [Start] | [Result] | [Exception] |

## Page Inventory

| Page | Module | Depth | Primary Action | Data Needed | Acceptance Note |
|---|---|---:|---|---|---|
| [Page] | [Module] | A/B/C | [Action] | [Data] | [Note] |

## WeCom Mini-Program Constraints

- Native/container navigation:
- WeCom contact states:
- Mini-program card or share actions:
- Bottom navigation show/hide rules:
- Sticky action bars:
- Empty/error/no-permission states:

## WeCom Native Page Replicas

| Native Replica | Trigger Flow | Required Fields | Click Depth | Return State | Acceptance Note |
|---|---|---|---|---|---|
| 新建群发 | [Task/content/send flow] | recipients; copy; attachment; frequency note | A/B/C | [Completed/failed/pending] | [Note] |

Native replica rules:
- Keep native replica visually distinct from clienteling business pages.
- Hide clienteling bottom navigation and unrelated app tools.
- Include send and cancel paths.
- Return to the originating business flow with a visible result.

## Interaction Standards

- Search fields:
- Local vs exact/global lookup:
- Filter groups:
- Sort defaults:
- Tabs / segments / chips:
- Drawers / bottom sheets:
- Page states:
- Disabled-action reasons:

## Task Execution Model

| Task Type | Source | Target Grain | Execution Channel | Native Handoff | Completion Feedback | Metric / Denominator |
|---|---|---|---|---|---|---|
| [1v1 / 1vN / Moments / native broadcast / appointment / content / offline] | [Source] | [Target] | [Channel] | [Yes/No] | [Feedback] | [Metric] |

## Extension Integrations

| Integration | Source System | Signal / State | Frontline Advisor Action | Result / Write-back | Prototype Depth |
|---|---|---|---|---|---|
| [Name] | [System] | [Signal] | [Action] | [Result] | A/B/C |

## Sample Data

- Customers:
- Frontline advisors / stores:
- Tasks:
- Opportunities, only if confirmed:
- Appointments:
- Content:

## Visual Direction

- Fidelity: wireframe / clean business prototype / high-fidelity branded prototype / executive demo
- Style direction: neutral enterprise / luxury fashion / beauty BA workbench / branded executive demo / other
- References:
- Brand assets:
- Density and tone:
- Component conventions:
- Generic placeholders:

## Prototype Presentation

- Shell source: `assets/prototype-shell/index.html` / framework port / other
- Desktop review stage: included / not included
- Mobile full-screen mode: included / not included
- Viewport behavior: automatic responsive / URL QA parameter / other
- Visible mobile/desktop selector: no
- Role selector:
- Free browse mode:
- Preset journey mode:
- Journey list:
- Journey HUD behavior:
- URL parameters:
- Stage controls hidden in mobile mode:
- Role-controlled show/hide rules:

## Shell QA

- Static checker command:
- Desktop screenshot reviewed:
- Mobile screenshot reviewed:
- Mini-program title bar and capsule present:
- Bottom tabbar behavior verified:
- Native replicas separated from clienteling pages:
- Emoji icons absent:
- Brand color used as controlled accent:

## Interaction Requirements

- [Interaction]

## Language And Terminology

- [Client terminology rules]

## Acceptance Checklist

- [ ] Capability map reviewed.
- [ ] Required flows are demo-ready.
- [ ] A/B/C page depth is clear.
- [ ] Roles and permissions are represented.
- [ ] Extension integrations are separated from core modules.
- [ ] HTML prototype shell static QA passes when HTML is in scope.
- [ ] Desktop and mobile render paths are visually verified when HTML is in scope.
- [ ] Open questions are listed.

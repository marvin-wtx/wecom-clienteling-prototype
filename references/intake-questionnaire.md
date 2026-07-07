# Intake Questionnaire

Ask only the questions needed to unblock the current deliverable. Prefer assumptions plus a short open-questions section when the user wants speed.

## Start Mode

Ask this before the detailed questionnaire when the user has not provided a clear path:

1. Do you want to start from existing materials, public research, a no-material baseline, or a hybrid of research plus baseline?
2. Should the immediate output be a written product plan/prototype brief, an HTML clickable prototype, a Figma/PPT handoff, or a QA review?
3. What industry and role term should be used: `SA`, `FA`, `BA`, advisor, consultant, or a client-specific term?

If the user has existing files, ask which source is authoritative. If the user wants research, ask which dimensions matter most. If the user wants baseline, read `references/reference-page-blueprints.md` and proceed with explicit assumptions.

## Research Dimensions

Ask when the user wants public research or gives only a brand/category:

- Should research focus on brand positioning, product/category focus, service model, member/customer vocabulary, retail advisor workflow, visual style, or competitor/category examples?
- Are public sources enough, or should the prototype stay deliberately generic because internal requirements are unknown?
- Should researched facts become visible page content, or only inform sample data, tone, and visual direction?

## Minimum Questions

1. What prototype format is expected: HTML, Figma, PPT, clickable image, or written specification?
2. What industry is this project for, and what should the frontline role be called: FA, SA, BA, advisor, consultant, or another client term?
3. Which business flows must be demo-ready?
4. Which source material should be treated as authoritative?
5. Should the output assume a WeCom ecosystem mini-program clienteling tool, or is another channel explicitly required?
6. What should be excluded from this prototype round?

## WeCom Mini-Program Channel

Default to a WeCom ecosystem mini-program / embedded mobile workbench. Ask only if unclear:
- Is this tool used inside WeCom/WeChat Work, a WeCom-linked mini-program, or another enterprise app container?
- Which actions should happen through WeCom chat: open chat, send mini-program card, send H5/content, invite, share QR code?
- Which customer states matter: added WeCom friend, not added, unmatched friend, registered mini-program member, unregistered, transferred contact?
- Are there native/container constraints from the client's mini-program shell, navigation bar, safe area, or existing app shell?
- Which actions require disabling or hiding when the customer is not a WeCom contact?

## WeCom Native Page Replication

Ask when communication execution is in scope:
- Does any flow need to reproduce a native WeCom page, such as 新建群发, group broadcast, native compose, recipient preview, or send result?
- Which actions leave the clienteling mini-program and enter native WeCom behavior?
- For 新建群发, what recipient count, message copy, attachment type, content source, and frequency/compliance note should appear?
- Should the recipient list and asset selection be clickable, structural, or placeholder?
- What happens after send, cancel, failure, or frequency-limit states?

## Capability Scope

Ask which modules are in scope:
- Add/binding and registration.
- Client list/C360.
- Task execution.
- Appointment/invitation.
- Content sharing.
- Dashboard/tracking.
- Transfer/ownership.
- Settings/admin/role management.

## Advanced Opportunity Scope

Only ask this section when the user's material mentions opportunity-like signals such as 重点客人, 重点客户, high-value customer, VIP follow-up, high-potential customer, lead, pipeline, purchase intent, next-best-action, or sustained nurturing.

Ask:
- Is this just a segment/filter for task targeting, or does it need a separate opportunity lifecycle?
- Does each opportunity have owner, reason, status, next action, follow-up cadence, and conversion result?
- Should it have a separate opportunity list/detail, or live inside C360/task?
- What states and metrics matter?
- Should this be demo-ready, structural, or deferred?

## Project-Specific Integration Scope

Do not assume a proprietary member ecosystem is present. Ask:
- Does this project include a proprietary member, loyalty, commerce, content, service, CRM/CDP/MA, or external platform integration?
- What is the integration called in the client's language?
- What customer state or signal does it provide?
- What frontline advisor action should it trigger?
- Is the action completed inside WeCom, linked out, or only reflected as a status?
- What result should be written back or shown later?
- Should this module be a primary demo flow, a supporting detail, or a placeholder?

## Page Depth

Ask:
- Which flows must be fully clickable?
- Which pages only need structure?
- Which future modules only need navigation placeholders?
- Is the prototype for business alignment, IT requirement handoff, user testing, or executive demo?

## Interaction Standards

Ask when list/detail behavior matters or source material is thin:
- Which pages need real search, filter, sort, tabs, drawers, or bottom sheets instead of static display?
- Which search fields matter: customer name, contact method, customer identifier, member identifier, WeCom nickname, task name, content title, or another field?
- Should search be local only, or should complete customer identifiers trigger exact/global lookup?
- Which filter groups are required for customer, task, content, appointment, dashboard, or transfer pages?
- Which tabs are true navigation, which are status tabs, and which should be filter chips instead?
- Which empty, no-result, no-permission, disabled-action, loading, error, and success states must be demo-ready?

## Task Execution Model

Ask when tasks are in scope:
- What task sources exist: HQ, store, system recommendation, CRM/CDP/MA, appointment, content, service, loyalty, or another source?
- What task types exist: 1v1, 1vN, Moments/朋友圈, native broadcast/新建群发, appointment, content share, data completion, or offline record?
- For each task type, what is the target grain: one customer, many customers, no direct customer list, appointment/resource, or another object?
- Which execution channels are used: clienteling page, WeCom chat, native WeCom page, mini-program card, content share, phone/offline record, or external system?
- What completion feedback is required: result, note, next follow-up date, skip/failure reason, or proof?
- Which task metrics matter, and what is the denominator?

## Prototype Presentation

For HTML/clickable prototypes, ask:
- Should I use the bundled WeCom mini-program prototype shell as the hard implementation base?
- Should the prototype use a desktop review stage with a mobile phone frame?
- Should it also support mobile full-screen mode where stage controls are hidden?
- Should the stage include role selector, free browse / journey mode switch, journey selector, and reset?
- Should viewport mode be automatic with optional QA URL parameters, rather than a visible mobile/desktop selector?
- Which roles should be switchable?
- Should journey mode control the role and disable manual role switching while active?
- Which preset journeys should be included?
- Are reproducible review links needed through URL parameters such as view, role, date, or journey?

## Weak-Source Baseline

If the user has no solid material, ask:
- Should I build a baseline WeCom Clienteling framework first and mark assumptions?
- Which industry should the baseline assume?
- Which core modules should be removed from the baseline?
- Is Opportunity intentionally needed, or should it remain excluded until confirmed?
- Should the baseline include a full page blueprint for Home, Customers/C360, Tasks, Appointment, Content, Dashboard, and role/permission states?
- Should sample data use fully neutral field labels, or does the client already have preferred names for customer/member identifiers, member levels, profile labels, and lifecycle states?

## Data And Language

Ask:
- What sample customers, stores, frontline advisors, products, tasks, appointments, and content should appear?
- What does this project call customer identifiers, member identifiers, contact fields, customer grouping, member level, profile labels, and lifecycle states?
- If there is no confirmed field vocabulary, should I use neutral generic labels such as customer identifier, member identifier, customer grouping, member level, profile label, and lifecycle state?
- Should labels be Chinese, English, bilingual, or client-specific terminology?
- Are there sensitive brands, customer names, or real data that must be anonymized?

## Visual Direction

Ask:
- Is the prototype expected to be wireframe, clean business prototype, high-fidelity branded prototype, or executive demo?
- Are there brand guidelines, app screenshots, WeCom/mini-program references, product images, content assets, logos, fonts, or colors to follow?
- Should the style be neutral enterprise, luxury fashion, beauty BA workbench, branded executive demo, or another direction?
- Should visual references be researched before design, and are there competitor or category examples to include?
- What visual elements should stay generic because they are not approved or not important for this round?

## Acceptance

Ask:
- What will reviewers check first?
- Which business rules are high risk?
- Which integrations or permissions are likely to be challenged?
- Should desktop/mobile adaptation, control show/hide, role switching, free browse, and preset journey mode be part of acceptance?
- Should native WeCom page replicas, such as 新建群发, be part of acceptance?
- What does "done" mean for this round?

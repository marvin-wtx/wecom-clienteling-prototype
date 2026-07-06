# WeCom Mini-Program Constraints

Use this reference for every page, flow, and prototype brief. The default product surface is a clienteling tool inside the WeCom/WeChat Work ecosystem, usually presented as a mini-program or embedded WebView-style mobile workbench.

## Channel Premise

Assume:
- The frontline user works inside WeCom or a WeCom-linked enterprise app context.
- Customer communication actions primarily happen through WeCom chat.
- Mini-program cards, H5 links, approved content, QR codes, and WeCom contact state are core interaction materials.
- Desktop is usually a review/demo stage for the mobile experience, not the production user surface.

Do not assume:
- A generic standalone SaaS dashboard.
- A consumer e-commerce mini-program.
- Native iOS/Android app conventions outside the WeCom container.
- Free-form messaging automation without consent, permission, or system rules.

## Native And Container-Like UI Rules

Reflect these constraints in prototype planning:
- Use a mini-program-style top navigation area with title, back affordance, and right-side safe area where relevant.
- Keep long page titles safe from right-side native controls by truncating or constraining title width.
- Use bottom navigation only for top-level pages; hide it on deep detail, creation, confirmation, or full-screen operational pages when it conflicts with action bars.
- Use sticky bottom action bars for primary completion actions.
- Avoid exposing technical backend steps as user-facing pages unless they are meaningful to business users.
- Treat loading, empty, no-permission, success, failed, and processing states as part of page behavior, not separate decorative pages.

## WeCom Interaction Rules

Model these explicitly when relevant:
- WeCom contact state: added/not added, current advisor contact, original advisor contact, transferred contact, unknown contact.
- Customer identity state: known profile, prospect, unmatched WeCom friend, registered/unregistered mini-program member.
- Communication actions: open chat, send mini-program card, send content, copy/share, invite, call/SMS/email as secondary actions only when in scope.
- Sending a mini-program card should show preconditions, target, result, and return state.
- If a customer is not a WeCom contact, disable or reroute WeCom send actions instead of pretending they work.
- If a send/broadcast action enters native WeCom behavior, read `wecom-native-page-replication.md` and model the native page separately from the clienteling mini-program page.

## Role And Permission Rules

Use permission to control visibility and interaction:
- Hide actions that should not be available to a role when hiding is the business rule.
- Disable actions only when the user should understand why the action exists but is currently unavailable.
- Make management-only tools visible only to confirmed manager/supervisor roles.
- Reflect data scope in page titles, filters, or context labels when management roles see store, region, or global data.

## Integration Rules

For any CRM/CDP/MA/member/service/content integration, document:
- Source system.
- State or signal shown inside the mini-program.
- Advisor action enabled by that signal.
- Whether the action is completed inside WeCom, linked out, or only reflected as a status.
- Result or write-back shown after action.
- Missing-data fallback.

## Prototype QA

Check:
- Primary actions respect WeCom contact and identity state.
- Mini-program card send flows have result states.
- Native WeCom send/broadcast replicas are included when source material or flow requirements call for them.
- Bottom navigation is hidden on appropriate deep pages.
- Role-only tools are hidden or shown according to permission.
- External integration data is visible as a business signal, not a technical task list.

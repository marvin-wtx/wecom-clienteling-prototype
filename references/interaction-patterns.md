# Interaction Patterns

Use this reference to standardize page-level interaction details across WeCom Clienteling prototypes. Keep these patterns generic unless source material gives a stricter client rule.

Read `terminology.md` before locking field labels. Do not reuse customer/member field names from a previous project unless the current project's source material confirms them.

## Scope

Apply these patterns to:
- Client lists, C360 drilldowns, task lists, content libraries, appointment lists, dashboards, transfer lists, and extension modules.
- Search, filter, sort, tabs, segmented controls, chips, bottom sheets, page states, and disabled-action explanations.
- Prototype briefs and QA checklists where cross-page interaction consistency matters.

## Search

Default behavior:
- Use one visible search entry per list page, with placeholder text naming the searchable object.
- Search within the current business scope first, such as my clients, my store, assigned tasks, or available content.
- Show suggestions while typing when the source supports it.
- Show the matched field when useful, such as customer name, contact method, customer/member identifier, profile label, or task/content name.
- Keep global exact search separate from local fuzzy search when the business has a central customer database.

Common customer search fields:
- Customer name.
- Contact method.
- Customer identifier.
- Member identifier.
- WeCom contact nickname when provided.
- Project-specific identifiers only when confirmed by source material.

Customer search rules to consider:
- Chinese names may suggest after one character; English names usually need more characters.
- Contact methods can be fuzzy while incomplete, then exact/global when complete if allowed.
- Customer/member identifiers can suggest after a partial threshold, then exact-match when complete.
- System primary keys should normally be exact-match only.
- Results should expose whether the customer is owned, visible only, not a WeCom friend, unregistered, or permission-limited.

Search states:
- Initial empty query.
- Loading suggestions.
- Local no result.
- Global exact no result.
- Permission-limited result.
- Network/source failure.
- Cleared query restoring the previous list context.

## Filter

Default behavior:
- Use filter entry plus selected-condition count when filters are hidden behind a drawer or bottom sheet.
- Keep reset, cancel, and apply actions visible in filter drawers.
- Show selected summary chips on the list page when multiple filters affect interpretation.
- Preserve filter state when drilling into a detail page and returning.
- Use AND across filter groups and OR inside the same multi-select group unless source material says otherwise.

Common filter groups:
- Ownership or scope: mine, store, region, global, support role.
- Customer attributes: customer grouping, member level, customer type, profile labels, lifecycle state, registration state, WeCom contact state.
- Business signals: purchase category, amount range, last purchase, birthday month, retention risk, source, tag.
- Task attributes: task type, source, priority, due time, status, execution channel.
- Content attributes: category, campaign, product line, language, validity, approval status.
- Appointment attributes: date, store, service/resource, status, advisor.

Filter states:
- No filters selected.
- Filters selected with result count.
- Filters selected but no matching result.
- Filter options loading.
- Filter source unavailable.
- Role-limited filters hidden or disabled with reason.

## Sort

Default behavior:
- Define one default sort per list page, based on the business decision the page supports.
- Show active sort label when sort affects the user's next action.
- Highlight or expose the field that explains the sort order when helpful, such as recent purchase, due time, priority, or total spend.

Common defaults:
- Client list: recent interaction or recent purchase, depending on business goal.
- Task list: due time plus priority.
- Content library: campaign priority, latest update, or relevance.
- Appointment list: upcoming time.
- Dashboard drilldown: metric contribution or variance.

## Tabs And Segments

Use different controls for different hierarchy levels:
- Bottom navigation: only top-level app sections.
- Page tabs: peer views inside one module, such as overview, interaction, purchase, preference.
- Segmented controls: small scope switches, such as my clients vs other visible WeCom friends.
- Filter chips: temporary query refinement, not navigation.
- Status tabs: stable business states, such as pending, in progress, completed, skipped, expired.

Rules:
- Do not turn every filter into a tab.
- Avoid more than five visible page tabs on mobile unless the source app already does this.
- Keep the active tab visually obvious and preserve scroll position when returning.
- Hide bottom navigation on deep detail, filter, native WeCom replica, create/edit, result, and task-execution pages when it conflicts with the active flow.
- Treat tabs, filters, drawers, and bottom sheets as interaction layers, not separate pages, unless the prototype needs a dedicated review screen.

## Page States

High-risk pages should cover:
- Normal populated state.
- Empty state before the user has data.
- No result state after search/filter.
- Loading state.
- Load failed state with retry.
- No permission state.
- Disabled action state with clear reason.
- Submitting state.
- Submit failed state with retry or alternative action.
- Success/result state.

Clienteling-specific disabled reasons:
- Customer is not a WeCom friend.
- Customer is not registered or not bound.
- Advisor does not own the customer.
- Store/region role cannot access the customer.
- Frequency, compliance, consent, or privacy limit.
- Required source-system data is missing.

## Prototype Guidance

When producing a prototype brief:
- Include reusable interaction rules once, then reference them page by page.
- Do not overbuild B/C pages; state which search/filter/tab interactions are structural only.
- For A-level pages, make search/filter/sort/tabs clickable enough to prove the business logic.
- Include representative empty/no-result/no-permission states when they affect reviewer confidence.
- Keep all interaction labels aligned to the project's industry role term: FA, SA, BA, advisor, consultant, or client-specific term.

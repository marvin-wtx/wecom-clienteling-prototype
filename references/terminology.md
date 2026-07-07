# Terminology And Role Naming

Use client and industry terminology exactly. Wrong role naming makes a prototype feel generic and unprofessional even when the flow is correct.

## Sales Associate Naming

Default rules:
- **Fashion / luxury fashion / retail fashion**: use **FA** for Fashion Advisor.
- **General retail / generic clienteling / cross-industry sales**: use **SA** for Sales Associate.
- **Beauty / cosmetics / personal care**: use **BA** for Beauty Advisor.

Do not blindly use FA across all projects. First infer from the industry, then confirm if the source material is ambiguous.

The role term is a generation-time decision, not a prototype runtime switch. Do not put FA/SA/BA in an in-prototype selector. A beauty prototype should not allow reviewers to switch the same screen to FA; a fashion prototype should not allow BA; a generic prototype should avoid implying a final term before industry is confirmed.

## How To Ask

Ask:
- What industry is this clienteling project for: fashion, beauty/personal care, general retail, jewelry, watch, home, auto, or other?
- What does the client call frontline store staff: FA, SA, BA, advisor, consultant, store associate, or another term?
- Are there role variations such as senior advisor, counter manager, store manager, supervisor, regional manager, HQ operator, or concierge?
- Should prototype copy use Chinese, English, bilingual labels, or client-specific English abbreviations?

## Field Vocabulary Mapping

Do not default to field names from a previous project. Customer identifiers, member identifiers, membership levels, profile labels, and grouping fields vary by client, system, and industry.

Ask when customer data, C360, search, filter, dashboard, or task targeting is in scope:
- What does this project call the main customer identifier?
- What does it call the member identifier or loyalty identifier, if any?
- Which contact fields can be searched or shown?
- What does the client call customer grouping, member level, lifecycle status, profile labels, or audience lists?
- Which labels are official UI labels, and which are backend/system field names that should stay hidden?
- If no field vocabulary is confirmed, should I use neutral generic labels for this prototype round?

Default neutral labels:
- Customer identifier.
- Member identifier.
- Contact method.
- Customer grouping.
- Member level.
- Profile label.
- Lifecycle state.
- Registration state.
- WeCom contact state.

Rules:
- Use client-provided field names only when they appear in source material or the user confirms them.
- Keep backend identifiers out of UI labels unless the business user recognizes them.
- For baseline prototypes, prefer neutral labels over brand-specific or system-specific terms.
- In the prototype brief, include a field vocabulary table whenever search, filter, C360, dashboard, or sample data depends on field names.

## Common Role Patterns

Use these as placeholders only until the user's source material confirms them:

| Industry | Frontline role | Manager role | Notes |
|---|---|---|---|
| Fashion / luxury fashion | FA | Store Manager / Supervisor | FA is usually expected in fashion clienteling contexts. |
| Beauty / cosmetics / personal care | BA | Counter Manager / Store Manager | BA is more natural than FA or SA. |
| General retail | SA | Store Manager / Supervisor | SA is the safer generic term. |
| Jewelry / watches | Advisor / SA | Boutique Manager | Some brands prefer advisor, specialist, or consultant. |
| Service-heavy luxury | Advisor / Consultant | Clienteling Manager | Confirm client language before writing UI. |

## Output Rules

- Use the confirmed role term consistently in page names, flows, sample data, buttons, empty states, and metrics.
- Use confirmed field vocabulary consistently in search placeholders, filters, C360 labels, sample data, dashboard dimensions, and task-targeting rules.
- If the source material mixes FA/SA/BA, call it out as a terminology risk.
- If source material mixes business labels and backend field names, call it out as a field-vocabulary risk.
- If the project has multiple business lines, allow role terms to vary by line only when the client explicitly does so.
- Keep internal system roles separate from user-facing labels. For example, "owner advisor" may be a data relationship while "BA" is the user-facing role.
- Keep industry terminology separate from permission roles. Prototype review controls may switch business roles such as frontline, store manager, regional manager, or HQ, but they must not switch the frontline term between FA/SA/BA.

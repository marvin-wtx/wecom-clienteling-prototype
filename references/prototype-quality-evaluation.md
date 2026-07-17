# Prototype Quality Evaluation

Use this after implementing a branded HTML/clickable prototype. It converts delivery QA from a self-attested checklist into a compact, reviewable evidence pack.

## Required Artifact

Create `docs/prototype-case-evaluation.json` from `assets/templates/prototype-case-evaluation-template.json`. The evaluation is not product UI and must not appear inside the mini-program.

For every evaluated surface, save an actual browser screenshot relative to the evaluation file and record what was observed. Required surfaces are:

- Home first viewport.
- C360.
- Task detail.
- Appointment detail, or an explicit out-of-scope rationale.

Record at least three state-changing interactions with expected and observed results. Static screenshots alone do not prove a clienteling workflow is connected.

## Human Quality Rubric

Score each dimension from 1 to 5, citing visible evidence rather than intentions. A delivery marked ready needs every score at 4 or 5.

| Dimension | 4-5 evidence | 1-2 failure signal |
| --- | --- | --- |
| `brandExpression` | A recognizable visual anchor, geometry, image discipline, and copy tone support the brand without masking work. | Only a logo, palette, or a generic fashion/luxury/sports trope changes. |
| `workbenchClarity` | Within the first viewport, the reviewer can identify what matters, why, and the next action; lists and states scan quickly. | A hero, decorative image, or generic KPIs push operational work below the fold. |
| `informationDepth` | C360, task detail, and appointment detail expose decision dimensions, exceptions, and result capture. | Summary cards and one CTA substitute for operational detail. |
| `structuralDistinctness` | Removing brand cues still leaves a different operating axis, navigation, home composition, detail architecture, and interaction. | The case is the starter shell or a previous case with restyled cards. |
| `demoCoherence` | A presenter can narrate one credible end-to-end role journey with connected data and realistic state changes. | Routes, data, actions, and outcomes contradict each other or are decorative. |

## Portfolio Comparison

Set `portfolioMode` to `first-case` only when no previous open-generative case is available. Otherwise set it to `compare`, cite every comparison case, and record at least four material differences for each reused archetype, or three for different archetypes.

Run `scripts/check_portfolio_diversity.py` against every available prior evaluation. This supplements, rather than replaces, `check_structural_similarity.py`: one checks documented operating decisions, the other checks the rendered HTML structure.

For repeated use, maintain `docs/prototype-portfolio-index.json` from `assets/templates/prototype-portfolio-index-template.json`. It lists every released open-generative/evidence-derived case and prevents an agent from silently comparing only the easiest prior case. When the index exists, run one complete check:

```bash
python3 scripts/check_portfolio_diversity.py docs/prototype-case-evaluation.json \
  --portfolio docs/prototype-portfolio-index.json
```

## Review Decision

Mark the case `pass` only when:

- Required screenshots exist and the observations describe what is visible.
- Required interactions reach their observed state/result.
- Every human quality score is at least 4.
- Portfolio comparison is complete when prior cases exist.
- No unresolved blocker remains.

Do not solve a low score by raising the number. Change the prototype, capture fresh evidence, and rerun the checks.

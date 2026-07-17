# WeCom Clienteling Prototype Skill

An AI-readable skill package for turning WeCom / WeChat Work mini-program clienteling materials into reusable prototype plans, capability maps, interaction standards, task-execution models, prototype shell implementations, and prototype QA checklists.

This repository is designed to be usable by AI agents that can read structured instruction files. Codex can install it as a native skill. Other AI assistants can use it as a workflow package by reading `SKILL.md` and the referenced files.

## What This Skill Does

- Extracts WeCom Clienteling business capabilities from rough or detailed source material.
- Routes work into source-backed, research-led, baseline, or hybrid modes depending on what the user has.
- Builds a reusable baseline framework with page-level blueprints and connected sample data when source material is sparse.
- Maps capabilities to IA, page inventories, demo journeys, and prototype briefs.
- Standardizes search, filter, sort, tabs, page states, and disabled-action reasons.
- Models task execution for 1v1, 1vN, Moments, native WeCom broadcast, appointment, content, and offline follow-up flows.
- Preserves WeCom mini-program constraints and native WeCom page replicas such as `新建群发` when relevant.
- Provides a reusable modern HTML shell kit with WeCom mini-program frame, configurable desktop review controls for role and Journey demos, mobile full-screen behavior, page primitives, and native page replica structure. The kit intentionally has no fixed clienteling IA or sample-data stack.
- Provides hard shell constraints for a compact desktop review console around a 390px by 844px mobile mini-program viewport, plus automatic mobile full-screen behavior.
- Checks generated HTML prototypes for shell-contract issues such as missing container, visible viewport selector, mobile blank-screen risk, and emoji icons.
- Guides visual direction, industry terminology, FA/SA/BA role naming, and customer/member field vocabulary.
- Produces coverage QA checks for business logic, interactions, permissions, and presentation behavior.

## Repository Structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── prototype-shell/
│   │   └── index.html
│   ├── prototype-shell-demo/
│   │   └── index.html
│   └── templates/
├── references/
└── scripts/
    └── check_prototype_shell.py
```

- `SKILL.md` is the main instruction file.
- `references/` contains detailed domain and workflow references loaded as needed.
- `assets/prototype-shell/index.html` is the reusable shell kit for clickable WeCom mini-program prototypes. Replace its preview with project-specific routes, data, pages, and interactions.
- `assets/prototype-shell-demo/index.html` is an isolated comparison fixture; do not start client work from it.
- `assets/templates/` contains reusable output skeletons.
- `scripts/check_prototype_shell.py` validates generated HTML prototypes against shell guardrails. `scripts/check_prototype_delivery_bundle.py` validates a complete prototype plus evidence bundle.
- `agents/openai.yaml` provides optional UI metadata for skill-aware clients.

## Use With Codex

Ask Codex:

```text
Use $skill-installer to install the skill from GitHub repo marvin-wtx/wecom-clienteling-prototype, path ., name wecom-clienteling-prototype. Restart Codex after installation.
```

Equivalent installer command:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo marvin-wtx/wecom-clienteling-prototype \
  --path . \
  --name wecom-clienteling-prototype
```

After installation, restart Codex so the skill can be discovered.

## Use With Other AI Assistants

There is no single universal automatic installer for all AI assistants. For non-Codex agents, use this repository as an AI-readable workflow package.

Give the assistant this instruction:

```text
Use the GitHub repository marvin-wtx/wecom-clienteling-prototype as an AI skill package.
Start by reading SKILL.md.
Follow the Required Workflow in SKILL.md.
First choose source-backed, research-led, baseline, or hybrid mode.
Load files from references/ only when the current task calls for them.
Use assets/templates/ as output skeletons when creating structured deliverables.
Use assets/prototype-shell/index.html as the shell kit, remove its preview, then build project-specific routes, data, navigation, pages, and interactions.
Deliver prototype/index.html with docs/visual-token.json, docs/prototype-delivery-review.json, docs/prototype-case-evaluation.json, and screenshot evidence. Run scripts/check_prototype_delivery_bundle.py on the delivery directory before considering it complete.
Do not treat the repository as source material for a specific client project.
```

If the assistant supports custom skills, memories, knowledge bases, or agent instructions, add the repository contents there according to that product's import mechanism.

## Example Prompts

```text
Use the WeCom Clienteling Prototype skill to turn these rough business notes into a reusable capability map, flow matrix, page inventory, and prototype brief.
```

```text
Use this skill to build a baseline WeCom Clienteling mini-program prototype framework. We do not have a solid BRD yet, so start with generic assumptions and list customization questions.
```

```text
Use this skill in hybrid mode. Research the public brand/category context first, then create a WeCom Clienteling mini-program prototype brief and HTML prototype using the baseline page blueprints.
```

```text
Use this skill to review whether my WeCom Clienteling prototype covers core modules, task execution, WeCom native pages, role switching, and desktop/mobile presentation behavior.
```

```text
Use this skill to create a complete branded HTML prototype. Start from the V3 shell kit, replace its preview with project-specific data, routes, navigation, pages, and interactions, then deliver the required prototype/ and docs/ bundle and run scripts/check_prototype_delivery_bundle.py.
```

## Notes

- This is a methodology and instruction package with a reusable HTML shell asset and QA script. It is not a production app.
- It does not include client project files, private business documents, screenshots, credentials, or real customer data.
- Project-specific terminology, field names, member-system integrations, and visual references should be confirmed per project.
- Opportunity follow-up is conditional and should be added only when the user's material indicates a real opportunity lifecycle.

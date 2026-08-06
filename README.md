# Investment Research Assistant

**A local-first investment research operating system with Agent skills and a visual research workbench.**

Investment Research Assistant turns project-based investment DD into a repeatable local workflow.

You put project materials, meeting notes, research reports and knowledge base files into a local Markdown workspace. The Agent reads that workspace and pushes the project forward through screening, industry research, technical research, company deep dive, expert interviews and IC reports. The built-in visual workbench then turns the same files into a browser-based project dashboard.

It is not just a prompt library. It is also not just a notebook viewer. It is a complete local research loop:

```text
Source materials + meetings
          ↓
Agent research skills
          ↓
Structured reports + project master files
          ↓
Visual workbench
          ↓
Reusable knowledge base
```

## Why It Is Different

- **Project-based DD, not one-off chat**: each company/project has its own materials, reports, meetings, state and next actions.
- **A visual workbench is included**: browse project pipeline, reports, meetings and knowledge base from a local web UI.
- **Strong research templates**: every Skill has a role, inputs, dependencies, output structure and quality checklist.
- **Meeting-first research**: management calls, expert interviews, roadshows and shareholder conversations become first-class evidence.
- **Cross-project memory**: reusable industry frameworks, company entities, technical routes and expert views can be saved into a knowledge base.
- **Local-first by design**: no database, no hosted backend, no SaaS account required. Your workspace is just files on your machine.
- **Model-agnostic**: use Claude, OpenAI, DeepSeek, GLM or any Agent environment that can read local files and follow `CLAUDE.md`.

## What You Get

```text
Investment Research Assistant
├── CLAUDE.md                  # Agent system prompt and global research rules
├── skills/                    # Investment research skills
├── workbench/                 # Local visual research workbench
├── workspace.example/         # Example project, report, meeting and knowledge base
├── scripts/                   # Workspace init and privacy scan
└── config.example.yaml        # User-adjustable local paths
```

## Visual Workbench

The workbench is part of this project. It is a local browser UI generated from your Markdown workspace.

```bash
python3 workbench/serve.py
```

It opens a local page at `http://localhost:8765` and shows:

| View | What it shows |
|---|---|
| Project Pipeline | Project stage, investment verdict, material inventory, completed research and linked meetings |
| Research Reports | Markdown reports generated or curated for each project |
| Meeting Records | Management calls, expert interviews, roadshows and shareholder conversations |
| Knowledge Base | Cross-project company entities, technical routes, industry concepts and reusable expert views |

The workbench does not require a server database. `workbench/refresh_data.py` scans your local `workspace/` and writes `workbench/data.js`; `workbench/index.html` renders it into a readable interface.

```text
workspace/ markdown files
        ↓ refresh_data.py
workbench/data.js
        ↓ index.html
local browser dashboard
```

## Agent Skills

Core skills included:

| Skill | Purpose |
|---|---|
| `pre-judge` | Fast screening: Go / Conditional Go / No Go |
| `industry-research` | Industry structure, KSFs and competitive landscape |
| `tech-research` | Technical routes, metrics and feasibility |
| `company-research` | Company deep dive across team, product, commercialization and risks |
| `competitor-analysis` | Competitor matrix, generation gap and dynamic scenarios |
| `expert-interview` | Hypothesis validation and expert interview design |
| `management-interview` | Management interview checklist by topic and priority |
| `ic-report` | IC-ready investment narrative from upstream research |
| `meeting-minutes` | Turn ASR/transcripts into investment-grade meeting notes |

## End-to-End Workflow

```text
Project Materials
      ↓
Ingest / Inventory
      ↓
Pre-judge
      ↓
Industry Research → Tech Research → Competitor Analysis
      ↓
Company Deep Dive
      ↓
Expert Interviews / Management Interview Checklist
      ↓
IC Report
      ↓
Workbench + Knowledge Base
```

Typical usage:

1. Create a project folder under `workspace/projects/[Project Name]/`.
2. Put BP, Datapack, reference reports and raw files under `materials/`.
3. Put meeting notes under `workspace/meetings/`.
4. Ask your Agent to run one of the research Skills.
5. Save generated reports under `reports/`.
6. Open the workbench to inspect the project status and evidence base.

## Quick Start

```bash
git clone https://github.com/coco1998/Investment-Research-Assistant.git
cd "Investment Research Assistant"
cp config.example.yaml config.yaml
python3 scripts/init_workspace.py
python3 workbench/serve.py
```

The browser should open `http://localhost:8765`. If it does not, open that URL manually.

You can immediately try the included fake example project. Your real project files should go into `workspace/`, which is ignored by Git.

## Workspace Layout

The default workspace is `./workspace`. You can keep it inside this repository for local testing, or point it to any folder on your machine.

```text
workspace/
├── projects/
│   └── [Project Name]/
│       ├── master.md
│       ├── reports/
│       ├── materials/
│       └── runs/
├── meetings/
├── knowledge/
│   └── 2_wiki/
│       ├── entities/
│       └── concepts/
└── materials/
```

## Configuration

The default workspace is `workspace/` inside this repository. You can also set an environment variable:

```bash
export IRA_WORKSPACE_ROOT="/path/to/your/research-workspace"
```

Or edit `config.yaml`:

```yaml
workspace_root: ./workspace
```

## Use With Claude Code Or Other Agents

Recommended setup:

1. Open this repository as your Agent workspace.
2. Ask the Agent to read `CLAUDE.md`.
3. Install or copy selected folders from `skills/` into your Agent skill directory if your environment supports skills.
4. Put project materials under `workspace/projects/[Project Name]/materials/`.

This repository is not tied to any model provider. You can use Claude, OpenAI, DeepSeek, GLM or any compatible Agent environment. API keys are configured in your own Agent/runtime environment, not in this repository.

## Refresh The Workbench

```bash
python3 workbench/refresh_data.py
```

Or click the refresh button in the lower-left corner of the workbench after starting the local server.

The workbench reads files from:

- `workspace/projects/*/master.md`
- `workspace/projects/*/reports/*.md`
- `workspace/projects/*/materials/**/*`
- `workspace/meetings/*.md`
- `workspace/knowledge/2_wiki/entities/*.md`
- `workspace/knowledge/2_wiki/concepts/*.md`

## Privacy By Default

This repository ships with fake example data only. Your real materials live in your own `workspace/`, which is ignored by Git by default.

Before publishing a fork or sharing your customized version, run:

```bash
python3 scripts/privacy_scan.py .
```

## Why This Exists

Most investment work is not a single report. It is a chain of messy, high-context steps: reading decks, checking management claims, interviewing experts, building industry maps, rewriting judgment after every new meeting, and turning scattered notes into an IC-ready view.

Investment Research Assistant is designed around that reality. It gives the Agent a strong research operating system, and gives the human a clean local surface to inspect what has been done.

## License

MIT License

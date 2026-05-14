# Android Agentic Template

> Stop letting AI guess your architecture.
> One script. A context-governed workflow. Drop into any Android project and run.

---

## What this does

AI coding assistants don't know your Koin modules, your Room schema, or your Navigation graph.
They're probabilistic text generators with finite context windows — they will pass `NavController`
into Composables and hardcode strings until you give them guardrails.

This script wires a practical context-governed workflow around GitHub Copilot, Gemini Code Assist, or both:

| Area | What it does | File |
|---|---|---|
| Context hygiene | Keeps generated files, assets, and locale XMLs out of passive context where supported | `.copilotignore` / `.aiexclude` |
| Project instructions | Project rules + canonical Kotlin patterns | `.github/copilot-instructions.md` |
| Planning checkpoint | Visible planning and risk checks for non-trivial changes | Inside `copilot-instructions.md` |
| Architecture map | Package map + KSP/generated-code conventions | `AGENTS.md` |
| Explicit routing | Reminds the assistant which files to read/include for architecture-sensitive tasks | Inside `copilot-instructions.md` + `AGENTS.md` |
| Script distillation | Bulk data ops via small terminal scripts instead of loading huge files into chat | `scripts/query_data.py` |
| Decision log | Append-only project-readable history of why decisions were made | `docs/history/` |

---

## Quick start

**1. Download the setup script**

```bash
git clone https://github.com/lluzalves/Android-Agentic-Template
```

**2. Copy `setup_agent.py` to your Android project root**

```bash
cd /path/to/your/android/project
```

**3. Preview what will be created (no changes yet)**

```bash
python3 setup_agent.py report
```

You will be asked which AI assistant you use:
```
Which AI assistant are you setting up?
  1) GitHub Copilot
  2) Gemini Code Assist
  3) Both
```

Or skip the prompt with the `--tool` flag:

```bash
python3 setup_agent.py report --tool copilot   # Copilot only
python3 setup_agent.py report --tool gemini    # Gemini only
python3 setup_agent.py report --tool both      # both
```

Example output (`--tool both`):
```json
{
  "files": [
    { "rel_path": "AGENTS.md",                                         "action": "create" },
    { "rel_path": "scripts/query_data.py",                             "action": "create" },
    { "rel_path": "docs/history/CHANGELOG.md",                         "action": "create" },
    { "rel_path": "docs/history/phases/phase-00-initial-setup.md",     "action": "create" },
    { "rel_path": ".copilotignore",                                    "action": "create" },
    { "rel_path": ".github/copilot-instructions.md",                   "action": "create" },
    { "rel_path": ".github/instructions/database.instructions.md",     "action": "create" },
    { "rel_path": ".aiexclude",                                        "action": "create" }
  ]
}
→ 8 file(s) would be created, 0 already exist (would be skipped).
```

**4. Apply**

```bash
python3 setup_agent.py apply --tool both
```

```
✅ 8 file(s) created, 0 skipped.

Next steps:
  • .copilotignore                            → adjust paths (enterprise only; Tab Hygiene for individuals)
  • .github/copilot-instructions.md           → paste your real ViewModel pattern + project rules
  • .github/instructions/database.instructions.md → update the applyTo glob to your package path
  • .aiexclude                                → adjust paths to your build / asset directories
  • AGENTS.md                                 → fill in your package map, nav destinations, and patterns
  • scripts/query_data.py                     → implement lookup logic for your data
  • docs/history/phases/phase-00-initial-setup.md → fill in your first decisions + alternatives considered

Remember: start a fresh chat session when switching to an unrelated task.
```

> **Safe to re-run** — existing files are never overwritten.

---

## Files by tool

| File | Copilot | Gemini |
|---|:---:|:---:|
| `AGENTS.md` | ✅ | ✅ |
| `scripts/query_data.py` | ✅ | ✅ |
| `docs/history/CHANGELOG.md` | ✅ | ✅ |
| `docs/history/phases/phase-00-initial-setup.md` | ✅ | ✅ |
| `.copilotignore` | ✅ | — |
| `.github/copilot-instructions.md` | ✅ | — |
| `.github/instructions/database.instructions.md` | ✅ | — |
| `.aiexclude` | — | ✅ |

---

## After running — what to customise

Every generated file has `# TODO:` markers. The five that matter most:

### 1. `.copilotignore` / `.aiexclude`
Adjust asset and build paths to match your project structure.
> ⚠️ `.copilotignore` only has practical effect on Copilot Enterprise plans.
> For individuals, the practical context hygiene habit is **Tab Hygiene** — keep irrelevant files closed.

### 2. `.github/copilot-instructions.md`
Paste your real ViewModel/UiState pattern so the assistant has a concrete local example to follow:
```kotlin
// TODO: replace with your real pattern + DI annotation
data class MyUiState(val isLoading: Boolean = true, val error: String? = null)

@KoinViewModel  // or @HiltViewModel
class MyViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(MyUiState())
    val uiState: StateFlow<MyUiState> = _uiState.asStateFlow()
}
```

Concrete local examples make the assistant more likely to follow your project's style than a generic rule alone.

### 3. `AGENTS.md`
Fill in your actual package map, navigation destinations, and KSP conventions.

### 4. `scripts/query_data.py`
Replace the stub with real lookup logic for your project's data.

### 5. `docs/history/phases/phase-00-initial-setup.md`
Fill in the **Goal**, **Changes**, **Alternatives considered**, and **Verification** sections
after your first session. This is the seed of your project's decision history for AI-assisted work.

---

## The Decision Log

The log gives the assistant a project-readable history that survives across chat sessions. Without it, the assistant may
re-propose libraries you already rejected and undo architectural trade-offs you spent
days finalising.

Each phase file follows this structure:

```markdown
# Phase 01 — Navigation Refactor

## Goal
Move to callback-only navigation.

## Changes
- Removed NavController from all Composables.

## Alternatives considered
| Option | Why rejected |
|---|---|
| Keep NavController | Breaks Compose previews and unit tests |

## Verification
- [ ] Build confirmed clean
- [ ] Lint check passes
```

**Rules:** never delete or rewrite phase files. Append a new one for every significant change.
Record rejections — what you didn't pick is as important as what you did.

---

## Using the HITL script

`scripts/query_data.py` is a compliant stub. Replace the stub logic with real lookups for
your project (exercise JSONs, translations, local DB, etc.):

```bash
# Preview (no side effects)
python3 scripts/query_data.py report --term "chest"

# Execute
python3 scripts/query_data.py query --term "chest"
```

Output is always JSON — paste it back into the AI chat.

---

## Script contract

Every script in `scripts/` must satisfy four rules:

| Rule | Why |
|---|---|
| **Idempotent** | Safe to re-run without side effects |
| **`report` mode** | Previews without applying |
| **Structured output** | JSON — parseable by the AI in the next turn |
| **Registered** | Listed in `AGENTS.md` routing rules so the AI knows it exists |

---

## Requirements

- Python 3.10+
- No external dependencies — stdlib only

---

## Full article

**[Stop Letting AI Go Off-Script: Building a Context-Governed Workflow](#)**

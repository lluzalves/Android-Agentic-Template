# Android Agentic Template

> Stop letting AI guess your architecture.
> One script. Six layers. Drop into any Android project and run.

---

## What this does

AI coding assistants don't know your Koin modules, your Room schema, or your Navigation graph.
They're probabilistic text generators with finite context windows — they will pass `NavController`
into Composables and hardcode strings until you give them guardrails.

This script wires a **6-layer Deterministic Constraint System** into your existing Android project:

| Layer | What it creates | Why |
|---|---|---|
| 1 — Eviction | `.copilotignore` + `.aiexclude` | Blocks KSP stubs, assets, locale XMLs from passive scan |
| 2 — System Prompt | `.github/copilot-instructions.md` | Your non-negotiable Android rules |
| 3 — CoT Protocol | (inside the system prompt) | Forces plan-before-code on every architecture change |
| 4 — Architecture Map | `AGENTS.md` | Package map + Room/Koin/Compose KSP conventions |
| 5 — Keyword Routing | (inside the system prompt) | `@DB`, `@Nav`, `@AI` trigger deterministic file injection |
| 6 — HITL Script | `scripts/query_data.py` | Bulk data ops via human-gated terminal commands |

---

## Quick start

**1. Download the setup script**

```bash
git clone https://github.com/your-handle/android-agentic-template.git
```

**2. Copy the setup_agent.py file to your Android project root**

```bash
cd /path/to/your/android/project
```

**3. Preview what will be created (no changes yet)**

```bash
python3 setup_agent.py report
```

Output:
```json
{
  "root": "/your/project",
  "files": [
    { "rel_path": ".copilotignore",                    "action": "create" },
    { "rel_path": ".aiexclude",                        "action": "create" },
    { "rel_path": ".github/copilot-instructions.md",   "action": "create" },
    { "rel_path": "docs/project-rules.md",             "action": "create" },
    { "rel_path": "AGENTS.md",                         "action": "create" },
    { "rel_path": "scripts/query_data.py",             "action": "create" },
    { "rel_path": "docs/history/CHANGELOG.md",         "action": "create" }
  ]
}
→ 7 file(s) would be created, 0 already exist (would be skipped).
```

**4. Apply**

```bash
python3 setup_agent.py apply
```

```
✅ 7 file(s) created, 0 skipped.

Next steps:
  1. Open .copilotignore    → adjust paths to your build/asset directories
  2. Open .github/copilot-instructions.md → paste your real ViewModel pattern
  3. Open AGENTS.md         → fill in your package map and nav destinations
  4. Open scripts/query_data.py → implement lookup logic for your data
```

> **Safe to re-run** — existing files are never overwritten.

---

## After running — three files to customise

The generated files are intentionally generic with `# TODO:` markers.
You only need to update three before your first AI session:

### 1. `.copilotignore`
Adjust the asset paths to match your project:
```gitignore
# TODO: change this to your actual assets directory
app/src/main/assets/**
```

### 2. `.github/copilot-instructions.md`
Paste your real ViewModel pattern. The AI will mirror it:
```kotlin
// TODO: replace XUiState with your real pattern
data class MyUiState(val isLoading: Boolean = true, val error: String? = null)

@KoinViewModel  // TODO: swap for @HiltViewModel if using Hilt
class MyViewModel : ViewModel() { ... }
```

### 3. `AGENTS.md`
Fill in your actual package map and navigation destinations:
```markdown
## Package Map
app/
  data/db/    YourDatabase.kt
  ui/
    navigation/ YourDestinations.kt
```

---

## Using the HITL script

`scripts/query_data.py` is a compliant stub — replace the stub logic with real lookups:

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

1. **Idempotent** — safe to re-run
2. **`report` mode** — previews without applying
3. **Structured output** — JSON
4. **Registered** — listed in `AGENTS.md` routing rules

---

## Full article

**[I Got Tired of Copilot Hallucinating My Android Architecture. Here's the 6-Layer System I Built.]([https://medium.com/p/fe7c47dc7363?postPublishedType=initial])**

---

## Requirements

- Python 3.10+
- No external dependencies — stdlib only

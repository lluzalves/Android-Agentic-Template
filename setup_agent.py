#!/usr/bin/env python3
"""
setup_agent.py — Deterministic Constraint System bootstrapper.

Run this script from the ROOT of your Android project:
    python3 setup_agent.py report   # preview what will be created (no changes)
    python3 setup_agent.py apply    # create the files

Existing files are NEVER overwritten. Safe to re-run.
"""

import argparse
import json
import sys
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# File definitions
# Each entry: (relative_path, file_content)
# ──────────────────────────────────────────────────────────────────────────────

FILES = {

    # ── Layer 1: Context Eviction ─────────────────────────────────────────────
    ".copilotignore": """\
# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 1 — Context Eviction
# Blocks heavy directories from the AI's passive background scan.
# The model can still read these files when you explicitly ask it to.
# ═══════════════════════════════════════════════════════════════════════════════

# ── KSP / Build output ────────────────────────────────────────────────────────
# KSP generates Room_Impl, Koin factories, Compose singletons — all noise.
# This single rule has the biggest impact on context quality.
**/build/generated/ksp/**
app/build/
build/

# ── Bundled data assets ───────────────────────────────────────────────────────
# Large JSON datasets, raw audio, ML models.
# TODO: adjust these paths to match your project's actual asset directories.
app/src/main/assets/**
app/src/main/res/raw/**

# ── Locale translation strings ────────────────────────────────────────────────
# Each locale file is ~400 lines of dead context. Inject on demand instead.
# TODO: if you only have one locale, you can remove this block.
app/src/main/res/values-*/

# ── Binary and media ──────────────────────────────────────────────────────────
**/*.mp3
**/*.png
**/*.jpg
**/*.webp

# ── Phase history ─────────────────────────────────────────────────────────────
# Historical logs — useful for humans, waste for the AI on every session.
docs/history/
""",

    # ── Same eviction rules for Gemini / local tools ──────────────────────────
    ".aiexclude": """\
# Same as .copilotignore — used by Gemini Code Assist and local LLM tools.
# Keep both files in sync.
**/build/generated/ksp/**
app/build/
build/
app/src/main/assets/**
app/src/main/res/raw/**
app/src/main/res/values-*/
**/*.mp3
**/*.png
**/*.jpg
**/*.webp
docs/history/
""",

    # ── Layer 2 + 3 + 5: System Prompt (Copilot) ─────────────────────────────
    ".github/copilot-instructions.md": """\
# AI Coding Rules — GitHub Copilot
# This file is auto-loaded by Copilot every session. Keep it focused.

## ═══════════════════════════════════════════════════════════════
## LAYER 3 — Interaction Protocol (Chain-of-Thought Enforcement)
## ═══════════════════════════════════════════════════════════════
## Forces the AI to plan before it writes code.
## DO NOT REMOVE — this is the most impactful single rule.

**For new features, new screens, DB migrations, or any architecture change:**
Before writing ANY code, you MUST:
1. **Restate** what you understood from the request in 2–3 lines.
2. **Propose** the implementation approach with a short pros/cons table.
3. **List at least one alternative** approach with its trade-offs.
4. **Ask** if the user wants to proceed.
Only write code after the user explicitly confirms.

**For bug fixes or refactors touching ≤ 3 files:**
Restate what you understood + confirm approach. No full pros/cons table needed.

**For single-file changes, renames, or obvious one-liners:**
Just do it.

---

## ═══════════════════════════════════════════════════════════════
## LAYER 2 — Non-Negotiable Project Rules
## ═══════════════════════════════════════════════════════════════
## TODO: replace these examples with your actual project rules.
## The more specific, the better — include your real DI framework,
## navigation approach, and naming conventions.

<!-- EXAMPLE RULES (customise or replace) -->
1. No hardcoded strings — use `stringResource(R.string.*)`.
2. No NavController in Composables — navigation via callbacks only.
3. `@KoinViewModel` on every ViewModel.
   <!-- TODO: if using Hilt, replace with @HiltViewModel -->
4. Entity != Domain model — map at the repository boundary.
5. Apply `navigationBarsPadding()` + `statusBarsPadding()` on every screen root.

## TODO: paste your canonical ViewModel / UiState pattern below.
## The AI will mirror whatever pattern you show it here.
<!--
```kotlin
data class XUiState(val isLoading: Boolean = true, val error: String? = null)

@KoinViewModel  // TODO: swap for your DI annotation
class XViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(XUiState())
    val uiState: StateFlow<XUiState> = _uiState.asStateFlow()
}

@Composable
fun XScreen(onNavigate: () -> Unit, viewModel: XViewModel = koinViewModel()) {
    val s by viewModel.uiState.collectAsStateWithLifecycle()
    // no NavController here — callbacks only
}
```
-->

---

## ═══════════════════════════════════════════════════════════════
## LAYER 5 — Mandatory Routing Rules
## ═══════════════════════════════════════════════════════════════
## Deterministic file injection — the AI fetches these on keyword match.
## TODO: add routing rules for every major architecture boundary in your project.

- IF the task involves DB schema, DAOs, or migrations
  → fetch `data/db/AppDatabase.kt` immediately.
- IF adding a new screen or destination
  → read `ui/navigation/Destinations.kt` first.
- IF prompt starts with `@DB`  → fetch AppDatabase.kt.
- IF prompt starts with `@Nav` → fetch Destinations.kt.
- IF prompt starts with `@AI`  → read the AI integration guide first.
- IF working on bulk data files
  → do NOT read files directly. Propose:
    `python3 scripts/query_data.py report --term "<value>"`
- IF asked about history
  → read `docs/history/CHANGELOG.md` first.

## TODO: add your own @-shortcuts here for frequently accessed files:
# - IF prompt starts with `@Theme` → fetch `ui/theme/Color.kt`.

---

## ═══════════════════════════════════════════════════════════════
## Full reference docs (fetch on demand — not loaded every session)
## ═══════════════════════════════════════════════════════════════
- Architecture + package map: `AGENTS.md`
- Phase history: `docs/history/CHANGELOG.md`
## TODO: add paths to your own deep-dive docs here.
""",

    # ── Layer 2 + 3 + 5: Same rules for Gemini Code Assist ───────────────────
    "docs/project-rules.md": """\
# AI Coding Rules — Gemini Code Assist
# Inject this file at the start of complex tasks: @project-rules.md

## Interaction Protocol
Same three-tier protocol as copilot-instructions.md.
Tag @project-rules.md at the start of every architecture-level task.

## Mandatory Context Routing
<!-- Tag these files explicitly in your Gemini prompts -->
- DB task           → ALWAYS tag `@AppDatabase.kt`
- New screen        → ALWAYS tag `@Destinations.kt`
- Architecture task → ALWAYS tag `@AGENTS.md`

## TODO: Add your project-specific rules below (same content as copilot-instructions.md).
""",

    # ── Layer 4: Architecture Map ─────────────────────────────────────────────
    "AGENTS.md": """\
# Agent Architecture Guide
# Fetch this file when the AI needs to understand project structure.
# Keep it focused — only what the AI needs to navigate, not everything.

---

## Package Map
<!-- TODO: replace with your real package structure -->
```
app/
  data/
    db/           AppDatabase.kt       (Room + optional encryption)
    dao/          one DAO per entity
    repository/
      interfaces/ domain-level contracts
      room/       Room implementations
  domain/
    model/        pure Kotlin — NO Room annotations here
  ui/
    navigation/   Destinations.kt, Navigation.kt
    components/   shared Composables
    theme/        Color.kt, Type.kt
  di/             AppModule.kt (Koin / Hilt wiring)
MainActivity.kt
```

---

## Generated Code Conventions (KSP — never write these manually)
| Generator | Naming convention              | Example                          |
|-----------|--------------------------------|----------------------------------|
| Room      | `<ClassName>_Impl`             | `AppDatabase_Impl`               |
| Koin KSP  | factory functions              | generated under `di/` package    |
| Compose   | `ComposableSingletons$<File>Kt`| internal — never reference       |

<!-- TODO: add conventions for any other code generators your project uses -->

---

## Navigation Destinations
<!-- TODO: list your NavKeys / NavDestinations so the AI can suggest the right one -->
| Key              | Screen                  |
|------------------|-------------------------|
| `Home`           | Main screen             |
| `Settings`       | App settings            |
<!-- add more rows -->

---

## When to fetch reference docs (mandatory)
- IF touching DB schema or DAOs → fetch `data/db/AppDatabase.kt` first
- IF adding a new screen       → read `ui/navigation/Destinations.kt` first
- IF working on bulk data      → use `python3 scripts/query_data.py report --term "<value>"`
- IF asked about history       → read `docs/history/CHANGELOG.md` first
- IF creating/modifying scripts → verify the script contract:
    (1) idempotent  (2) has a `report` mode  (3) prints structured output  (4) registered here

---

## Full reference docs
<!-- TODO: add paths to deep-dive docs for major subsystems -->
- Phase history: `docs/history/CHANGELOG.md`
""",

    # ── Layer 6: HITL Script ──────────────────────────────────────────────────
    "scripts/query_data.py": """\
#!/usr/bin/env python3
\"\"\"
query_data.py — HITL bulk-data query stub.

Satisfies the script contract:
  (1) Idempotent       — safe to re-run, no side effects
  (2) report mode      — previews results without modifying anything
  (3) Structured output — JSON, parseable by the AI in the next turn
  (4) Registered       — listed in AGENTS.md routing rules

Usage:
  python3 scripts/query_data.py report --term "<value>"   # preview (no changes)
  python3 scripts/query_data.py query  --term "<value>"   # execute lookup

TODO: replace the stub logic below with real data lookup for your project.
      Examples:
        - Search exercise JSON files by muscle group
        - Query a local SQLite database
        - Grep translation strings by key
\"\"\"
import argparse
import json


def report(term: str) -> None:
    \"\"\"Preview what would be returned — no side effects.\"\"\"
    # TODO: implement real search logic here
    result = {
        "mode": "report",
        "term": term,
        "matches": [],
        "note": "TODO: replace with real data lookup logic."
    }
    print(json.dumps(result, indent=2))


def query(term: str) -> None:
    \"\"\"Execute lookup and return structured output for the AI.\"\"\"
    # TODO: implement real search logic here
    result = {
        "mode": "query",
        "term": term,
        "matches": [],
        "note": "TODO: replace with real data lookup logic."
    }
    print(json.dumps(result, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bulk-data query tool — run report first, then query."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for cmd in ("report", "query"):
        sub = subparsers.add_parser(cmd, help=f"{cmd} mode")
        sub.add_argument("--term", required=True, help="Search term")

    args = parser.parse_args()
    if args.command == "report":
        report(args.term)
    else:
        query(args.term)


if __name__ == "__main__":
    main()
""",

    # ── Phase history scaffold ─────────────────────────────────────────────────
    "docs/history/CHANGELOG.md": """\
# Phase History Index
<!-- Append one line per phase: - [Phase NN — Title](phases/phase-NN-slug.md) `YYYY-MM-DD` -->
<!-- Example: - [Phase 01 — Initial Setup](phases/phase-01-initial-setup.md) `2026-05-03` -->
""",

    # ── Phases directory placeholder ───────────────────────────────────────────
    "docs/history/phases/.gitkeep": "",
}


# ──────────────────────────────────────────────────────────────────────────────
# Core logic
# ──────────────────────────────────────────────────────────────────────────────

def collect_plan(root: Path) -> list[dict]:
    """Return a list of actions the script would take."""
    plan = []
    for rel_path, content in FILES.items():
        target = root / rel_path
        plan.append({
            "rel_path": rel_path,
            "action": "skip" if target.exists() else "create",
            "size_bytes": len(content.encode()),
            "_content": content,   # internal — stripped before JSON output
            "_target": target,     # internal — stripped before JSON output
        })
    return plan


def _public(plan: list[dict]) -> list[dict]:
    """Strip internal keys before printing."""
    return [{k: v for k, v in item.items() if not k.startswith("_")} for item in plan]


def run_report(root: Path) -> None:
    plan = collect_plan(root)
    print(json.dumps({"root": str(root), "files": _public(plan)}, indent=2))
    creates = sum(1 for f in plan if f["action"] == "create")
    skips   = sum(1 for f in plan if f["action"] == "skip")
    print(f"\n→ {creates} file(s) would be created, {skips} already exist (would be skipped).")


def run_apply(root: Path) -> None:
    plan = collect_plan(root)
    results = []

    for item in plan:
        target: Path = item["_target"]
        if item["action"] == "skip":
            results.append({"rel_path": item["rel_path"], "result": "skipped"})
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(item["_content"], encoding="utf-8")
        if target.suffix == ".py":
            target.chmod(0o755)
        results.append({"rel_path": item["rel_path"], "result": "created"})

    print(json.dumps({"root": str(root), "files": results}, indent=2))
    created = [r for r in results if r["result"] == "created"]
    skipped = [r for r in results if r["result"] == "skipped"]
    print(f"\n✅ {len(created)} file(s) created, {len(skipped)} skipped (already existed).")

    if created:
        print("\nNext steps:")
        print("  1. Open .copilotignore                   → adjust paths to your build/asset directories")
        print("  2. Open .github/copilot-instructions.md  → paste your real ViewModel pattern")
        print("  3. Open AGENTS.md                        → fill in your package map and nav destinations")
        print("  4. Open scripts/query_data.py            → implement lookup logic for your data")


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bootstrap a 6-layer Deterministic Constraint System in your Android project.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 setup_agent.py report            # preview without making changes
  python3 setup_agent.py apply             # create files (skips existing ones)
  python3 setup_agent.py apply --root /path/to/project
        """
    )
    parser.add_argument(
        "command",
        choices=["report", "apply"],
        help="report = preview only | apply = create files"
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current directory)"
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()

    if not root.exists():
        print(f"❌ Directory not found: {root}", file=sys.stderr)
        sys.exit(1)

    print(f"🤖 Deterministic Constraint System — {args.command.upper()}")
    print(f"   Project root: {root}\n")

    if args.command == "report":
        run_report(root)
    else:
        run_apply(root)


if __name__ == "__main__":
    main()


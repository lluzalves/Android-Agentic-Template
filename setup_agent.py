#!/usr/bin/env python3
"""
setup_agent.py — Context-governed AI assistant bootstrapper.

Run this script from the ROOT of your Android project:
    python3 setup_agent.py report   # preview what will be created (no changes)
    python3 setup_agent.py apply    # create the files

You will be asked which AI assistant you use: Copilot, Gemini, or Both.
Existing files are NEVER overwritten. Safe to re-run.

Generated workflow:
  - Context hygiene        .copilotignore / .aiexclude
  - Project instructions   .github/copilot-instructions.md
  - Planning checkpoint    (inside copilot-instructions.md)
  - Architecture map       AGENTS.md
  - Explicit routing       (inside copilot-instructions.md + AGENTS.md)
  - Script distillation    scripts/query_data.py
  - Decision log           docs/history/CHANGELOG.md + phases/phase-00-initial-setup.md
"""

import argparse
import json
import sys
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# Shared files — created regardless of tool choice
# ──────────────────────────────────────────────────────────────────────────────

SHARED_FILES = {

    # ── Architecture map ──────────────────────────────────────────────────────
    # Keep this file as a compact project reference. Tool support varies by IDE,
    # extension version, and mode, so explicitly attach/reference it when needed.
    "AGENTS.md": """\
# Agent Architecture Guide
# Keep this file under ~150 lines — only what the AI needs to navigate.
# Tool support varies by IDE and mode. Explicitly attach/reference this file
# when the task depends on architecture, navigation, database, or generated-code rules.

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

## Canonical Patterns
<!-- TODO: paste your real ViewModel / UiState snippet here.
     This gives the assistant a concrete example to follow. -->
```kotlin
data class XUiState(val isLoading: Boolean = true, val error: String? = null)

// TODO: swap annotation for your DI framework (@HiltViewModel, etc.)
@KoinViewModel
class XViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(XUiState())
    val uiState: StateFlow<XUiState> = _uiState.asStateFlow()
}

@Composable
fun XScreen(onNavigate: () -> Unit, viewModel: XViewModel = koinViewModel()) {
    val s by viewModel.uiState.collectAsStateWithLifecycle()
    // no NavController passed in — callbacks only
}
```

---

## Generated Code Conventions (KSP — never write these manually)
| Generator | Naming convention               | Example                           |
|-----------|---------------------------------|-----------------------------------|
| Room      | `<ClassName>_Impl`              | `AppDatabase_Impl`                |
| Koin KSP  | factory functions               | generated under `di/` package     |
| Compose   | `ComposableSingletons$<File>Kt` | internal — never reference        |
<!-- TODO: add conventions for any other code generators your project uses -->

---

## Navigation Destinations
<!-- TODO: list your NavKeys / NavDestinations so the AI picks the right one -->
| Key        | Screen       |
|------------|--------------|
| `Home`     | Main screen  |
| `Settings` | App settings |
<!-- add more rows -->

---

## Bulk Action Routing
- IF task involves searching large datasets
  → do NOT attempt to parse files directly.
    Propose: `python3 scripts/query_data.py report --term "<value>"`
    Wait for the structured result before continuing.
- IF auditing generated or language files
  → propose `python3 scripts/query_data.py report --term "<value>"` (dry-run first).

---

## Explicit Context Routing
- Architecture task      → include/reference `AGENTS.md`
- DB schema / DAO task   → include/reference `AppDatabase.kt` and relevant entity/DAO files
- New screen / routing   → include/reference `Destinations.kt` and `Navigation.kt`

---

## When to read reference docs
- IF touching DB schema or DAOs     → read `data/db/AppDatabase.kt` first
- IF adding a new screen            → read `ui/navigation/Destinations.kt` first
- IF working on bulk data           → use `python3 scripts/query_data.py report --term "<value>"`
- CRITICAL: IF asked about project history, previous tech stack decisions,
  why a library was chosen, or before proposing a major refactor
  → read `docs/history/CHANGELOG.md` and the relevant files in `docs/history/phases/`
- IF creating / modifying scripts   → verify the script contract:
    (1) idempotent  (2) has a `report` mode  (3) prints structured output  (4) registered here

---

## Full reference docs (read on demand)
<!-- TODO: add paths to deep-dive docs for major subsystems -->
- Decision log index: `docs/history/CHANGELOG.md`
""",

    # ── Layer 6: HITL bulk-data query stub ────────────────────────────────────
    "scripts/query_data.py": """\
#!/usr/bin/env python3
\"\"\"
query_data.py — Human-proxied bulk-data query tool.

Instead of loading large JSON / asset files into the chat window, the AI proposes
this command. You run it, paste the structured output back, and the AI continues.

Satisfies the script contract:
  (1) Idempotent        — safe to re-run, no side effects
  (2) report mode       — previews results without modifying anything
  (3) Structured output — JSON, parseable by the AI in the next turn
  (4) Registered        — listed in AGENTS.md and copilot-instructions.md routing guidance

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

    # ── Phase history scaffold ──────────────────────────��──────────────────────
    "docs/history/CHANGELOG.md": """\
# Phase History Index
<!-- Append one line per phase: - [Phase NN — Title](phases/phase-NN-slug.md) `YYYY-MM-DD` -->
<!-- Example: - [Phase 01 — Initial Setup](phases/phase-01-initial-setup.md) `2026-05-03` -->
- [Phase 00 — Initial Setup](phases/phase-00-initial-setup.md)  `TODO: add date`
""",

    # ── Phase 00 template — fill in after your first session ──────────────────
    "docs/history/phases/phase-00-initial-setup.md": """\
# Phase 00 — Initial Setup

**Date:** TODO: add date

## Goal
<!-- TODO: one sentence — what was this phase trying to achieve? -->
Bootstrap a context-governed workflow so AI-assisted work has clear project
constraints, reference files, and verification habits.

## Changes
<!-- TODO: list every file that was created or modified. -->
- Created `.copilotignore` / `.aiexclude` (context hygiene)
- Created `.github/copilot-instructions.md` (project rules + planning protocol + routing guidance)
- Created `AGENTS.md` (architecture map)
- Created `scripts/query_data.py` (HITL bulk-data stub)
- Created `docs/history/CHANGELOG.md` + this file (decision log)

## Alternatives considered
<!-- TODO: record what you evaluated and why you rejected it.
     This is the highest-value section — it prevents the AI from re-proposing
     options you already dismissed. Be specific about the trade-offs. -->
| Option | Why rejected |
|---|---|
| Hilt instead of Koin | TODO: fill in |
| NavController in Composables | TODO: fill in |
| ... | ... |

## Verification
<!-- TODO: how did you confirm this phase worked correctly? -->
- [ ] Ran `python3 setup_agent.py report` — expected files listed as "create"
- [ ] Ran `python3 setup_agent.py apply` — expected files created
- [ ] Opened a new chat session and referenced the relevant project instruction files
- [ ] Tested history routing: asked "why did we choose X?" and confirmed the assistant used CHANGELOG.md first

## Rules (do not delete)
- Never delete or rewrite phase files — append a new phase for every significant change.
- Record rejections, not just choices — what you didn't pick is as important as what you did.
""",
}

# ──────────────────────────────────────────────────────────────────────────────
# Copilot-specific files
# ──────────────────────────────────────────────────────────────────────────────
# NOTE: .copilotignore has limited / no practical effect for individual developers —
# content exclusion is a server-side enterprise feature. The main hygiene strategy
# for Copilot is Tab Hygiene: keep irrelevant files closed. The file is still
# generated here so teams with enterprise licences benefit, and as a clear
# declaration of intent.
COPILOT_FILES = {

    ".copilotignore": """\
# ═══════════════════════════════════════════════════════════════════════════════
# GitHub Copilot — Context Hygiene
#
# ⚠️  For individual developers this file has limited / no practical effect.
#     Content exclusion is a server-side enterprise feature.
#     Your most reliable hygiene strategy is Tab Hygiene: close files you are
#     not actively editing — Copilot weights open tabs heavily.
#
# For teams on a Copilot Enterprise plan: the patterns below do take effect.
# ═══════════════════════════════════════════════════════════════════════════════

# ── KSP / Build output ────────────────────────────────────────────────────────
# Room_Impl, Koin factories, Compose singletons — all generated noise.
**/build/generated/ksp/**
app/build/
build/

# ── Bundled data assets ───────────────────────────────────────────────────────
# TODO: adjust these paths to match your actual asset directories.
app/src/main/assets/**
app/src/main/res/raw/**

# ── Locale translation strings ────────────────────────────────────────────────
# Each locale file is ~400 lines of dead context. Inject on demand instead.
# TODO: remove this block if you only have one locale.
app/src/main/res/values-*/

# ── Binary and media ──────────────────────────────────────────────────────────
**/*.mp3
**/*.png
**/*.jpg
**/*.webp

# ── Phase history ─────────────────────────────────────────────────────────────
docs/history/
""",

    # ── Project instructions + planning + routing ────────────────────────────
    # Auto-loaded by Copilot at the start of every chat session.
    ".github/copilot-instructions.md": """\
# AI Coding Rules — GitHub Copilot
# Auto-loaded every session. Keep this file focused and under ~200 lines.

## ═══════════════════════════════════════════════════════════════
## Planning and Verification Protocol
## ═══════════════════════════════════════════════════════════════
## Visible planning checkpoint for non-trivial changes.

**New feature / new screen / DB migration / any architecture change:**
Before writing code, you MUST:
1. **Restate** what you understood from the request in 2–3 lines.
2. **Propose** the implementation approach and name the key files/layers affected.
3. **List** at least one alternative or notable trade-off.
4. **Check** missing context, risks, or architectural constraints.
Ask for confirmation before editing when the change is ambiguous or high-impact.
For straightforward requested changes, proceed after the protocol.

**Bug fix or refactor touching ≤ 3 files:**
Restate what you understood + confirm approach. No full pros/cons table needed.

**Single-file change, rename, or obvious one-liner:**
Just do it.

---

## ═══════════════════════════════════════════════════════════════
## Non-Negotiable Project Rules
## ═══════════════════════════════════════════════════════════════
## TODO: replace these examples with your actual rules.

1. No hardcoded strings — use `stringResource(R.string.*)`.
2. No NavController in Composables — navigation via callbacks only.
3. `@KoinViewModel` on every ViewModel.
   <!-- TODO: swap for @HiltViewModel if using Hilt -->
4. Entity != Domain model — map at the repository boundary; never expose Room entities above `data/`.
5. Apply `navigationBarsPadding()` + `statusBarsPadding()` on every screen root.

## TODO: paste your canonical ViewModel / UiState pattern here.
## Copilot is more likely to follow a concrete local example than a generic rule.
<!--
```kotlin
data class XUiState(val isLoading: Boolean = true, val error: String? = null)

@KoinViewModel
class XViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(XUiState())
    val uiState: StateFlow<XUiState> = _uiState.asStateFlow()
}
```
-->

---

## ═══════════════════════════════════════════════════════════════
## Explicit Context Routing
## ═══════════════════════════════════════════════════════════════
## Do not rely on semantic search alone. Read/include the relevant source of truth
## before architecture-sensitive changes.
## TODO: add a rule for every architecture boundary in your project.

- IF the task involves DB schema, DAOs, or migrations
  → read/include `data/db/AppDatabase.kt` and relevant entity/DAO files first.
- IF adding a new screen or destination
  → read/include `ui/navigation/Destinations.kt` first.
- IF prompt starts with `@DB`    → read/include AppDatabase.kt.
- IF prompt starts with `@Nav`   → read/include Destinations.kt + Navigation.kt.
- IF prompt starts with `@AI`    → read/include the AI integration guide first.
- IF working on large datasets or bulk JSON files
  → do NOT read files directly. Instead, propose:
    `python3 scripts/query_data.py report --term "<value>"`
    Wait for the user to provide the structured result before continuing.
- IF asked why a certain library or architecture was chosen,
  OR before proposing a major refactor
  → FIRST read `docs/history/CHANGELOG.md` to identify the relevant phase,
    THEN read that phase file to understand the existing constraints.

## TODO: add your own @-shortcuts for frequently accessed files, e.g.:
# - IF prompt starts with `@Theme` → read/include `ui/theme/Color.kt`.

---

## ═══════════════════════════════════════════════════════════════
## Full reference docs (read on demand — NOT loaded every session)
## ═══════════════════════════════════════════════════════════════
- Architecture + package map: `AGENTS.md`
- Phase history: `docs/history/CHANGELOG.md`
## TODO: add paths to your own deep-dive docs here.
""",

    # ── Path-matched instruction file for DB context ──────────────────────────
    # Copilot injects this automatically only when the developer has a DB file open,
    # keeping the token budget efficient.
    ".github/instructions/database.instructions.md": """\
---
applyTo: "**/data/db/**/*.kt"
---
# Database Architecture Constraints

- NEVER expose Room entities above the `data/` layer.
- All data MUST be mapped to Domain Models at the repository boundary before
  reaching the Domain or UI layers.
- Use `@Transaction` for queries that join multiple tables.
- Run `report` mode on any migration script before applying it.
- TODO: add your real entity → domain mapping pattern here as a code example.
""",
}

# ──────────────────────────────────────────────────────────────────────────────
# Gemini-specific files
# ──────────────────────────────────────────────────────────────────────────────
GEMINI_FILES = {

    # ── Context hygiene ───────────────────────────────────────────────────────
    # .aiexclude uses gitignore-style patterns and blocks Gemini Code
    # Assist from indexing heavy folders for both chat and code completion.
    # This is the primary context hygiene mechanism for Gemini users.
    ".aiexclude": """\
# ═══════════════════════════════════════════════════════════════════════════════
# Gemini Code Assist — Context Hygiene
# Uses gitignore-style patterns: blocks Gemini from indexing these paths in the
# background, for both chat and code completion.
# You can still explicitly tag any of these files with @ when you need them.
# ═══════════════════════════════════════════════════════════════════════════════

# ── KSP / Build output ────────────────────────────────────────────────────────
# KSP generates thousands of stub files (_Impl, factories, Compose singletons).
# This single rule has the biggest impact on context quality.
**/build/generated/ksp/**
app/build/
build/

# ── Bundled data assets ───────────────────────────────────────────────────────
# Large JSON datasets, raw audio, ML models.
# TODO: adjust paths to match your actual asset directories.
app/src/main/assets/exercises/**
app/src/main/res/raw/**

# ── Locale translation strings ────────────────────────────────────────────────
# 9 locales × ~400 lines = dead context. Inject on demand via @-tags instead.
# TODO: remove this block if you only have one locale.
app/src/main/res/values-*/

# ── Binary, media, and heavy history ─────────────────────────────────────────
**/*.mp3
**/*.png
**/*.jpg
**/*.webp
docs/history/
""",
}

# ──────────────────────────────────────────────────────────────────────────────
# Tool selection helpers
# ──────────────────────────────────────────────────────────────────────────────

TOOL_CHOICES = {
    "copilot": "GitHub Copilot",
    "gemini":  "Gemini Code Assist",
    "both":    "Both (GitHub Copilot + Gemini Code Assist)",
}


def ask_tool_choice() -> str:
    """Interactively ask the user which AI assistant they use."""
    print("Which AI assistant are you setting up?")
    print("  1) GitHub Copilot")
    print("  2) Gemini Code Assist")
    print("  3) Both")
    while True:
        raw = input("\nEnter 1, 2, or 3: ").strip()
        if raw == "1":
            return "copilot"
        if raw == "2":
            return "gemini"
        if raw == "3":
            return "both"
        print("  Please enter 1, 2, or 3.")


def files_for_tool(tool: str) -> dict:
    """Return the merged file dict for the chosen tool."""
    files = dict(SHARED_FILES)
    if tool in ("copilot", "both"):
        files.update(COPILOT_FILES)
    if tool in ("gemini", "both"):
        files.update(GEMINI_FILES)
    return files


def looks_like_android_project(root: Path) -> bool:
    """Heuristic guard to avoid writing scaffolding in the wrong directory."""
    root_markers = (
        "settings.gradle",
        "settings.gradle.kts",
        "build.gradle",
        "build.gradle.kts",
        "gradlew",
    )
    if any((root / marker).exists() for marker in root_markers):
        return True
    return (root / "app" / "build.gradle").exists() or (root / "app" / "build.gradle.kts").exists()


# ──────────────────────────────────────────────────────────────────────────────
# Core logic
# ──────────────────────────────────────────────────────────────────────────────

def collect_plan(root: Path, files: dict) -> list[dict]:
    plan = []
    for rel_path, content in files.items():
        target = root / rel_path
        plan.append({
            "path": str(target),
            "rel_path": rel_path,
            "action": "skip (already exists)" if target.exists() else "create",
            "size_bytes": len(content.encode()),
        })
    return plan


def run_report(root: Path, files: dict, tool: str) -> None:
    plan = collect_plan(root, files)
    print(f"\nTool: {TOOL_CHOICES[tool]}")
    print(json.dumps({"root": str(root), "files": plan}, indent=2))
    creates = sum(1 for f in plan if f["action"] == "create")
    skips   = sum(1 for f in plan if f["action"].startswith("skip"))
    print(f"\n→ {creates} file(s) would be created, {skips} already exist (would be skipped).")


def run_apply(root: Path, files: dict, tool: str) -> None:
    plan = collect_plan(root, files)
    results = []

    for item in plan:
        target = Path(item["path"])
        if target.exists():
            results.append({"path": item["rel_path"], "result": "skipped"})
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(files[item["rel_path"]], encoding="utf-8")
        if target.suffix == ".py":
            target.chmod(0o755)
        results.append({"path": item["rel_path"], "result": "created"})

    print(f"\nTool: {TOOL_CHOICES[tool]}")
    print(json.dumps({"root": str(root), "files": results}, indent=2))
    created = [r for r in results if r["result"] == "created"]
    skipped = [r for r in results if r["result"] == "skipped"]
    print(f"\n✅ {len(created)} file(s) created, {len(skipped)} skipped (already existed).")

    if created:
        print("\nNext steps:")
        if tool in ("copilot", "both"):
            print("  • .copilotignore                           → adjust paths (enterprise only; Tab Hygiene for individuals)")
            print("  • .github/copilot-instructions.md          → paste your real ViewModel pattern + project rules")
            print("  • .github/instructions/database.instructions.md → update the applyTo glob to your package path")
        if tool in ("gemini", "both"):
            print("  • .aiexclude                               → adjust paths to your build / asset directories")
        print("  • AGENTS.md                                → fill in your package map, nav destinations, and patterns")
        print("  • scripts/query_data.py                    → implement lookup logic for your data")
        print("  • docs/history/phases/phase-00-initial-setup.md → fill in your first decisions + alternatives considered")
        print("\nRemember: start a fresh chat session for every new task (Reset Habit).")


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bootstrap a context-governed AI assistant workflow in your Android project.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 setup_agent.py report   # preview without making changes
  python3 setup_agent.py apply    # create files (skips existing ones)
        """
    )
    parser.add_argument(
        "command",
        choices=["report", "apply"],
        help="report = preview only | apply = create files",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--tool",
        choices=["copilot", "gemini", "both"],
        help="AI assistant to configure (skips interactive prompt)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow running even if --root does not look like an Android project",
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()

    if not root.exists():
        print(f"❌ Directory not found: {root}", file=sys.stderr)
        sys.exit(1)

    if not args.force and not looks_like_android_project(root):
        print(
            f"❌ {root} does not look like an Android project root.\n"
            "   Expected settings.gradle(.kts), build.gradle(.kts), gradlew, or app/build.gradle(.kts).\n"
            "   Re-run with --force if this is intentional.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("🤖 Context-Governed AI Assistant Workflow — " + args.command.upper())
    print(f"   Project root: {root}\n")

    tool = args.tool or ask_tool_choice()
    files = files_for_tool(tool)

    if args.command == "report":
        run_report(root, files, tool)
    else:
        run_apply(root, files, tool)


if __name__ == "__main__":
    main()

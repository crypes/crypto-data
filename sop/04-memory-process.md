# SOP: Multi-Level Memory Process

> Persistent memory system — Filesystem is the only Source of Truth

## Core Philosophy

Context window is temporary and subject to compaction. If an important detail, decision, or lesson is not written to a file, it does not exist.

## Memory Structure

```
workspace/
├── NOW.md                    # Active workbench (short-term)
└── memory/
    ├── INDEX.md              # Navigation hub (long-term)
    ├── YYYY-MM-DD.md         # Daily event stream (mid-term)
    ├── reflections/          # Nightly reflections
    ├── lessons/              # Categorized knowledge
    ├── decisions/            # Key decisions & reasoning
    └── people/               # Person-specific context
```

## Operational Rules

### 1. NOW.md — Short-Term (Session/Heartbeat)

- **When:** Session start + every heartbeat (30 min)
- **Action:** Overwrite with current state
- **Content:**
  - Current time (UTC)
  - Active tasks & progress
  - "Life-raft" info (critical context if context window clears)
  - Recent conversation context

### 2. Daily Log — Mid-Term

- **When:** Significant events, decisions, or conversations
- **Action:** Append only (never overwrite)
- **File:** `memory/YYYY-MM-DD.md`
- **Format:** `### HH:MM — [Title]` + concise summary

### 3. INDEX.md — Long-Term Navigation

- **When:** Created once, updated on structure changes
- **Action:** Maintain as table of contents for knowledge vault
- **Content:** File structure overview + categories + recent log links

### 4. Categorized Knowledge — Permanent

- **When:** Insights extracted from reflections or conversations
- **Action:** Read-before-write (see below)
- **Folders:**
  - `memory/lessons/` — Learned patterns & insights
  - `memory/decisions/` — Key decisions & reasoning
  - `memory/people/` — Person-specific context

## Read-Before-Write Protocol

Before updating lessons/, decisions/, or people/:

1. **Read** the existing file
2. **Compare:**
   - New info → ADD
   - Updates old fact → UPDATE entry, mark old as "superseded"
   - Contradicts → MARK AS CONFLICT with ⚠️, keep old data
3. **Update YAML frontmatter:** status, priority, last_verified

## Retrieval Strategy

When asked about the past:

1. **Scan** `memory/INDEX.md` for relevant file
2. **Read** the specific file identified
3. **Fallback:** Scan recent `memory/YYYY-MM-DD.md` logs

## Backup

All memory files included in personality-backup (via `daily_push.sh`):
- NOW.md copied directly
- memory/ folder tarred + encrypted → memory.tar.gz.enc

Run: `./personality-backup/daily_push.sh`

## Future SOPs

When establishing new processes, ask: "Should this be an SOP?"
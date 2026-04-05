# SOP: Nightly Reflection

> Run daily around 23:45 UTC — must complete before date ticks over

## Trigger

- Time-based: ~23:45 UTC
- Source: Cron or manual trigger

## Steps

### 1. Read Context

Read in this order:
1. `NOW.md` — active workbench state
2. `memory/YYYY-MM-DD.md` — today's log (use current date)
3. `memory/INDEX.md` — check for relevant knowledge files
4. Any files referenced in INDEX that relate to today's events

### 2. Write Reflection

Create `memory/reflections/YYYY-MM-DD.md`:

```markdown
# YYYY-MM-DD — Nightly Reflection

## Plan vs Reality

- [What was planned?]
- [What actually happened?]

## What Went Right

- 

## What Went Wrong

- 

## Tomorrow

- [Changes to make]
```

### 3. Extract & Classify Insights

For each notable point from the reflection:

- **Lesson learned?** → Add to `memory/lessons/`
- **Decision made?** → Add to `memory/decisions/`
- **Person update?** → Add to `memory/people/`

### 4. Read-Before-Write (Critical)

Before adding to lessons/, decisions/, or people/:

1. **Read** the existing file
2. Compare:
   - New info → ADD
   - Updates old fact → UPDATE entry, mark old as "superseded"
   - Contradicts → MARK AS CONFLICT with ⚠️, keep old data
3. **Update YAML frontmatter**: status, priority, last_verified

## Timing

Must finish before midnight UTC to use the correct date stamp.

### 5. Push to GitHub (Important)

Changes MUST be pushed to GitHub so that personality is preserved in case of mishaps.

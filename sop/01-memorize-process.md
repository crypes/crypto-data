# SOP: Memorize a Standard Operating Procedure

Purpose
- Teach the assistant (or another agent) how to ingest a new SOP file, validate it, and add a short summary to the agent's memory so it can recall the SOP later.

When to run
- When a new SOP Markdown file is added to the sop/ directory or an existing SOP is updated.

Prerequisites
- The SOP file exists in /root/.openclaw/.openclaw/workspace/sop/ and follows the filename convention: NN-short-name.md
- The assistant has write access to memory/ and can run the memory write helper (write tool) to create a dated memory note.

Step-by-step commands (agent/human)
1. Validate filename and frontmatter
   - Confirm the filename uses a two-digit numeric prefix and hyphenated name (e.g., 02-backup-personality.md).
   - Optionally check that the file includes the required top-level sections: Purpose, When to run, Prerequisites, Steps, Expected outcome, Safety notes, Prompt template.

2. Summarize the SOP
   - Create a concise 2–3 sentence summary that captures the goal, when to use it, and any critical warnings.

3. Add to memory
   - Write an entry to memory/YYYY-MM-DD.md with the summary and a source citation (filepath). Example entry:

     YYYY-MM-DD
     - Memorized SOP: 02-backup-personality.md — summary: "Back up personality and memory to GitHub with encrypted memory archive; stores key on-host for automation."
     - Source: /root/.openclaw/.openclaw/workspace/sop/02-backup-personality.md

4. Optionally notify stakeholders (human)
   - If the SOP is security-sensitive, prompt the human owner for review before adding to memory.

Expected outcome
- The assistant can recall the SOP name, location, and summary via memory search.

Safety/rollback notes
- Do not add plaintext secrets to memory entries. If an SOP contains sensitive commands or keys, redact them and store secrets in a secure vault instead.

Prompt template (for other agents)

"Read the SOP file at <path>. Validate its filename and structure. Produce a 2–3 sentence summary that captures the purpose and critical warnings. Append a memory note to memory/YYYY-MM-DD.md with the summary and a source citation. If the SOP contains plaintext secrets, stop and ask the human."

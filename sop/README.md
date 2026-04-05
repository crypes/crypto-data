SOP (Standard Operating Procedures)

This directory stores standard operating procedures as Markdown prompts and recipes intended for use by the assistant or other agents. Each SOP should be written so an automated agent (or a human following exact commands) can execute the process reliably.

Files in this directory:
- 01-memorize-process.md — SOP and prompt for how to ingest and "memorize" new SOPs so they become part of agent memory and are discoverable.
- 02-backup-personality.md — SOP and prompt for performing the personality backup, encryption, push, and verification process.
- verify_backup.sh is stored separately in the backup files; this directory should contain human/agent-facing SOPs, not the implementation scripts themselves (though linking to them is fine).

Guidelines for new SOPs
- Filename: two-digit prefix for ordering, short hyphenated name, .md extension (e.g. 03-rotate-keys.md)
- Top-level sections: Purpose, When to run, Prerequisites, Step-by-step commands, Expected outcome, Safety/rollback notes, Prompt template
- Keep each SOP focused and runnable. Avoid long digressions; link to longer references if needed.

When you create or update an SOP, consider running the "memorize" SOP so the assistant records the new process into memory for later recall.

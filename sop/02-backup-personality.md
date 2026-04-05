# SOP: Backup Personality and Memory

Purpose
- Regularly back up the assistant's core personality files and daily memory to a GitHub repository, ensuring the memory files are encrypted and backups are verifiable for restore.

When to run
- On-demand, and automatically daily (cron) for incremental updates. Additionally verify monthly using the verification script.

Prerequisites
- GitHub repository exists and the host has push access (SSH deploy key configured for the repo).
- OpenSSL, git, and ssh available on host.
- A symmetric passphrase stored securely (on-host at /root/.personality_key or off-host in a password vault).

Files involved (location in workspace)
- SOUL.md, IDENTITY.md, AGENTS.md, USER.md, TOOLS.md, HEARTBEAT.md, BOOTSTRAP.md (placeholder if missing)
- MEMORY.md (long-term memory) — encrypted as files/MEMORY.md.enc
- memory/ (daily notes) — archived to memory.tar.gz.enc
- Scripts: restore_personality.sh, daily_push.sh, verify_backup.sh

High-level steps
1. Collect core personality files into personality-backup/files/.
2. Encrypt MEMORY.md to files/MEMORY.md.enc using passphrase (do not store passphrase in repo).
3. Archive memory/ to memory.tar.gz and encrypt to files/memory.tar.gz.enc using passphrase.
4. Commit and push to the backup branch (main). Preserve previous main by creating main-backup.
5. Configure a cron job to run daily_push.sh daily and verify_backup.sh monthly.
6. Verify by cloning the repo, running restore_personality.sh into a temporary directory, decrypting memory archive, and confirming restored files match live workspace.

Commands (example)
- Encrypt MEMORY.md:
  openssl enc -aes-256-cbc -salt -pbkdf2 -iter 100000 -in MEMORY.md -out files/MEMORY.md.enc -pass file:/root/.personality_key

- Archive and encrypt memory dir:
  tar -czf memory.tar.gz memory/
  openssl enc -aes-256-cbc -salt -pbkdf2 -iter 100000 -in memory.tar.gz -out files/memory.tar.gz.enc -pass file:/root/.personality_key

- Commit/push:
  git add -A && git commit -m "Daily backup: $(date -u +%Y-%m-%dT%H:%M:%SZ)" && git push origin main

Restore notes
- Use restore_personality.sh to copy files from files/ into the workspace (it backs up existing files first).
- Decrypt memory archive:
  openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 -in files/memory.tar.gz.enc -out memory.tar.gz -pass pass:YOUR_PASSPHRASE
  tar -xzf memory.tar.gz -C /root/.openclaw/.openclaw/workspace

Safety and secrets
- Do not store passphrases or private keys in the repo. Use deploy keys for SSH and store symmetric passphrase in a password manager; place a copy on-host only if automation requires it (and protect it with strict filesystem permissions).

Prompt template (for an agent to perform the backup)

"Perform the personality backup:
1. Ensure /root/.personality_key exists and is readable.
2. Copy core files SOUL.md, IDENTITY.md, AGENTS.md, USER.md, TOOLS.md, HEARTBEAT.md, BOOTSTRAP.md into personality-backup/files/.
3. Encrypt MEMORY.md to files/MEMORY.md.enc using the passphrase in /root/.personality_key.
4. Archive memory/ to memory.tar.gz and encrypt to files/memory.tar.gz.enc.
5. Commit all changes and push to origin main, preserving old main as main-backup.
6. Run the verification script or perform a manual restore to confirm backups.
7. Report success or any errors, and do not expose the passphrase."
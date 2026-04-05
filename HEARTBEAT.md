# HEARTBEAT.md

Heartbeats run every 30 minutes.

## On Each Heartbeat

1. Read current NOW.md to understand active context
2. Update NOW.md with:
   - Current time (UTC)
   - Any new active tasks or progress
   - Update "life-raft" info if anything changed
3. If there are tasks in NOW.md that need attention, report them
4. If nothing needs attention, reply: HEARTBEAT_OK

## Important

- Your context window may clear between heartbeats
- NOW.md is your only source of truth for persistent state
- Always read NOW.md first, then overwrite with updated state
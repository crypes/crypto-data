# SOP: Ask Before Major Platform Changes

## Purpose
Avoid downgrading platform components (Ruby, Rails, etc.) without user approval.

## Scope
The following changes require explicit user approval **before** implementation:

- Changing Ruby version (upgrade or downgrade)
- Changing Rails version (upgrade or downgrade)
- Changing database engines
- Removing or replacing core dependencies
- Modifying system packages that affect the runtime environment

## Process

1. **Identify the conflict** (e.g., "Rails 8.1 requires Ruby 3.2+ but system has 3.1")
2. **Present options** to the user:
   - Upgrade the platform component (preferred)
   - Use a different version with tradeoffs
   - Wait / defer the task
3. **Wait for user confirmation** before proceeding
4. **Implement** only after approval
5. **Document** the change in memory/ and update relevant files

## Rationale
Downgrading Rails to work around a Ruby version mismatch was the wrong call. The correct approach is to upgrade Ruby to meet the Rails requirements, or ask the user what they prefer.
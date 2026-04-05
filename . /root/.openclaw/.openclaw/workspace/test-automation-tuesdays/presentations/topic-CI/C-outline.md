# CI/CD Topic C: Triggering Ruby/WDIO/Mabl from GitHub Actions

## Learning Objectives
By the end of this session, participants will be able to:
- Understand how to execute different test frameworks (WDIO, Ruby, Mabl) within GitHub Actions
- Configure necessary runtimes (Node.js, Ruby, Mabl CLI) in CI pipelines
- Trigger tests based on specific conditions or events

### Presentation Outline (20-25 minutes)

1.  **Introduction: Unified CI/CD (3 min)**
    *   The challenge of managing diverse test suites in CI.
    *   Goal: A single pipeline orchestrating different tools.

2.  **Executing WebdriverIO in Actions (5 min)**
    *   Recap of Topic 5: `npm ci` and `npm run wdio`.
    *   Ensuring Node.js runtime (`actions/setup-node`).
    *   Handling secrets for cloud services.

3.  **Executing Ruby Tests (Watir/Cucumber) (6 min)**
    *   Setting up Ruby runtime (`actions/setup-ruby`).
    *   Installing gems (`bundle install`).
    *   Running Cucumber tests (`bundle exec cucumber`).
    *   Managing Ruby-specific secrets.

4.  **Executing Mabl Tests (6 min)**
    *   **Option 1: Mabl CLI:**
        *   Install Mabl CLI on the runner.
        *   Trigger a data center test using API key and environment ID.
        ```yaml
        - name: Run Mabl tests
          run: mabl datacenter login --api-key ${{ secrets.MABL_API_KEY }}
          run: mabl datacenter run --environment <env_id> --branch <branch_name>
        ```
    *   **Option 2: Mabl API:**
        *   Trigger runs via job calls in the workflow.
    *   Considerations for environment setup for Mabl runs.

5.  **Orchestration & Conditions (3 min)**
    *   Using `if:` conditions in workflow steps.
    *   Running jobs sequentially or in parallel based on tool type.
    *   Combining results (potentially complex).

6.  **Q&A / Wrap-Up (2 min)**
    *   Best practices for multi-tool CI.
    *   Preview of Test Data & Environments topic.

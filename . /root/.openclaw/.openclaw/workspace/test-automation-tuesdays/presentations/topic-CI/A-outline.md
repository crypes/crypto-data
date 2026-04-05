# CI/CD Topic A: Migrating from Bamboo to GitHub Actions

## Learning Objectives
By the end of this session, participants will be able to:
- Understand the key differences between Bamboo and GitHub Actions
- Plan a migration strategy from Bamboo to GitHub Actions
- Implement basic CI/CD workflows in GitHub Actions for WebdriverIO tests

### Presentation Outline (20-25 minutes)

1.  **Introduction: Why Migrate? (3 min)**
    *   Benefits of GitHub Actions (integration, community, cost)
    *   Limitations of Bamboo for modern workflows

2.  **Comparing Bamboo & GitHub Actions (7 min)**
    *   **Core Concepts:** Plans vs. Workflows, Jobs vs. Steps, Agents vs. Runners
    *   **Syntax:** YAML vs. XML/UI configuration
    *   **Integration:** GitHub ecosystem vs. Atlassian ecosystem
    *   **Community:** GitHub Actions marketplace vs. Bamboo plugins
    *   **Cost:** GitHub Runners vs. self-hosted/Bamboo agents

3.  **Migration Strategy (5 min)**
    *   **Assessment:** Analyze existing Bamboo plans and jobs.
    *   **Planning:** Identify key workflows to replicate.
    *   **Phased Approach:** Migrate critical pipelines first.
    *   **Testing:** Validate migrated workflows thoroughly.

4.  **Demo: Basic GitHub Actions Workflow for WDIO (7 min)**
    *   Show a simple `.github/workflows/ci.yml` file.
    *   Steps: Checkout, Setup Node, Install dependencies, Run tests.
    *   Demonstrate artifact upload.

5.  **Q&A / Wrap-Up (3 min)**
    *   Common migration challenges
    *   Tips for a smooth transition
    *   Preview of next topic (Triggering various tools)

### Demo: Basic GitHub Actions Workflow for WDIO (7 min)
**Objective:** Show a simple GitHub Actions workflow to run WebdriverIO tests.

**Steps:**
1.  **Create Workflow File:**
    *   Create `.github/workflows/ci.yml` in the repo root.
2.  **Define Workflow:**
```yaml
name: Node CI for WebdriverIO

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
    - uses: actions/checkout@v4

    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'

    - name: Install Dependencies
      run: npm ci

    - name: Run WebdriverIO Tests
      run: npm run wdio
      env:
        CI: true

    - name: Upload Artifacts (Optional)
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: wdio-test-results
        path: results/
```
3.  **Explain Workflow Components:**
    *   `name`, `on`, `jobs`, `runs-on`, `strategy`, `steps`.
    *   Key actions: `checkout`, `setup-node`, `upload-artifact`.
    *   Running tests via `npm run wdio`.
4.  **Push & Observe:**
    *   Commit the workflow file.
    *   Push to GitHub and show the Actions tab execution.

### Resources
- WDIO GitHub Actions Docs: https://webdriver.io/docs/githubactions/
- GitHub Actions Docs: https://docs.github.com/en/actions
- `research.md` for this topic

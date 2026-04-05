# CI/CD Topic A: Migrating from Bamboo to GitHub Actions

## Blog Posts & Articles
- **GitHub Actions Documentation** | https://docs.github.com/en/actions
  - Official guides on workflows, triggers, runners.
- **WebdriverIO GitHub Actions Integration** | https://webdriver.io/docs/githubactions/
  - Specific guidance for WDIO tests in Actions.
- **Migrating from Jenkins to GitHub Actions** | Various CI/CD Blogs
  - Search: "migrate Jenkins to GitHub Actions CI/CD"
  - General principles apply to Bamboo as well.

## Key Concepts for Migration
1.  **Workflow Syntax:** YAML structure for GitHub Actions.
2.  **CI/CD Triggers:** Push, Pull Request, Schedule, Manual.
3.  **Runners:** GitHub-hosted vs. Self-hosted runners.
4.  **Secrets Management:** Storing sensitive keys (API keys, tokens).
5.  **Artifacts:** Storing build outputs (reports, logs, screenshots).
6.  **Caching Dependencies:** Speeding up builds (`actions/cache`).
7.  **Matrix Builds:** Running jobs across multiple OS, Node versions, or browsers.
8.  **Community Actions:** Reusable workflow components.

## Migration Steps
1.  **Analyze Bamboo Pipelines:** Document existing jobs, environments, dependencies, and triggers.
2.  **Map to GitHub Actions:** Replicate jobs using YAML workflows.
    *   Setup Node.js environment (`actions/setup-node`).
    *   Install dependencies (`npm ci` or `yarn install`).
    *   Run tests (`npm run wdio`).
    *   Archive artifacts (`actions/upload-artifact`).
    *   Manage secrets (`secrets.YOUR_SECRET_NAME`).
3.  **Set up Runners:** Choose appropriate runners (e.g., `ubuntu-latest`).
4.  **Implement Caching:** Cache `node_modules` for faster installs.
5.  **Configure Triggers:** Set up triggers for desired events (e.g., push to main, PRs).
6.  **Test and Refine:** Run workflows, debug issues, and optimize performance.

## Considerations
- **Learning Curve:** GitHub Actions has a different syntax and approach than Bamboo.
- **Runner Management:** Decide between GitHub-hosted and self-hosted runners.
- **Community Actions:** Leverage existing actions to reduce custom scripting.
- **Reporting Integration:** Ensure reports (e.g., Allure) are generated and available as artifacts.

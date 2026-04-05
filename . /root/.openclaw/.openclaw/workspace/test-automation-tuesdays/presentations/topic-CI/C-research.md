# Research: Triggering Ruby/WDIO/Mabl from GitHub Actions

## Blog Posts & Articles
- **GitHub Actions for WebdriverIO** | https://webdriver.io/docs/githubactions/
  - Covers running WDIO tests in GH Actions.
- **Running Ruby/Cucumber Tests in CI** | Various blogs
  - Search: "run Ruby Cucumber GitHub Actions", "Watir GitHub Actions CI"
- **Mabl GitHub Actions Integration** | Mabl Documentation
  - Look for specific integrations or examples. Likely involves API calls or CLI usage.

## Key Concepts
1.  **Tool Execution:** How to run different types of test scripts from GitHub Actions.
    *   **Node.js (WDIO):** `npm run wdio`, `npx playwright test`, etc.
    *   **Ruby (Watir/Cucumber):** `bundle exec cucumber`
    *   **Mabl:** Use Mabl CLI or API to trigger data center runs.
2.  **Environment Variables:** Passing configuration and secrets.
3.  **Runner Setup:** Ensuring the runner has necessary runtimes (Node, Ruby, Docker).
4.  **Triggering Logic:** Conditional execution based on branch, tags, or file changes.
5.  **Artifact Handling:** Collecting results from different tools.

## Specific Tool Integration Examples
### WebdriverIO
- Covered in Topic 5 research. Basic setup:
  ```yaml
  - name: Run WDIO Tests
    run: npm run wdio
  ```

### Ruby (Watir/Cucumber)
- Requires Ruby setup: `actions/setup-ruby`
- Example step:
  ```yaml
  - name: Run Ruby tests
    run: |
      gem install bundler
      bundle install
      bundle exec cucumber
  ```

### Mabl
- **Using Mabl CLI:**
  - Requires installing Mabl CLI on the runner.
  - Trigger a data center test using API key and environment ID.
  ```yaml
  - name: Run Mabl tests
    run: mabl datacenter login --api-key ${{ secrets.MABL_API_KEY }}
    run: mabl datacenter run --environment <env_id> --branch <branch_name>
  ```
- **Using Mabl API:** Trigger runs via job calls in the workflow.

## Challenges
- Diverse runtime requirements (Node, Ruby, Docker, Mabl CLI).
- Managing secrets for different services.
- Correlating results from multiple tools in a single report.

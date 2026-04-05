# Research: Advanced BDD Patterns

## Official Documentation
- **WebdriverIO Retry Flaky Tests** | https://webdriver.io/docs/retry/
  - How to handle test flakiness with retry configuration
- **Cucumber Hooks** | https://webdriver.io/docs/frameworks/#cucumber-specific-configuration
  - Before/After hooks for setup and teardown

## Blog Posts & Articles
- **Building a Robust WebDriverIO Test Automation Framework** | Jignect (Dec 2025)
  - https://jignect.tech/building-a-robust-test-automation-framework-with-webdriverio-best-practices/
  - Covers hooks, tags, and parallel execution strategies

## Video Resources
- **Cucumber Hooks and Tags Tutorial** | YouTube
  - Search: "Cucumber hooks tags tutorial"

## Key Concepts
1. Hooks (Before, After, BeforeStep, AfterStep)
2. Tags (@smoke, @regression, @wip)
3. Parallel execution with Cucumber
4. Retry strategies for flaky tests
5. Data tables in Gherkin
6. Scenario Outlines with Examples

## Code Examples
- Tag-based test selection: `--cucumberOpts.tagExpression='@smoke'`
- Parallel execution: `maxInstances: 4`
- Retry configuration: `specFileRetries: 2`

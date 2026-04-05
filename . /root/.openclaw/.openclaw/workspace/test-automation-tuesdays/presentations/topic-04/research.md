# Research: Flaky Tests & Reliability

## Official Documentation
- **WebdriverIO Retry Flaky Tests** | https://webdriver.io/docs/retry/
  - How to handle test flakiness with retry configuration
- **Best Practices** | https://webdriver.io/docs/bestpractices/
  - Proper waits and assertions

## Blog Posts & Articles
- **Flaky Tests in Automation** | Ranorex (Nov 2025)
  - https://www.ranorex.com/blog/flaky-tests/
  - Causes and solutions for flakiness
- **Building a Robust WebDriverIO Framework** | Jignect (Dec 2025)
  - https://jignect.tech/building-a-robust-test-automation-framework-with-webdriverio-best-practices/
  - Covers reliable locators and dynamic waits

## GitHub Issues
- **Retry Flaky Tests Discussion** | https://github.com/webdriverio/webdriverio/issues/564
  - Historical context on flaky test handling

## Key Concepts
1. Explicit waits vs Implicit waits
2. Reliable locators (data-testid vs CSS/XPath)
3. Retry strategies (specFileRetries, this.retries())
4. Test isolation
5. Handling async operations
6. Network stability

## Common Causes of Flakiness
- Race conditions
- Timing issues
- Environment dependencies
- Data pollution
- Browser state leaks

# Research: Accessibility Testing (Automated)

## Official Documentation
- **WebdriverIO Accessibility Testing** | https://webdriver.io/docs/accessibility/
  - Official accessibility testing guide
- **Axe Core Integration** | https://webdriver.io/docs/accessibility-testing/axe-core/
  - Using @axe-core/webdriverio

## Blog Posts & Articles
- **Accessibility Testing with Axe and WebdriverIO** | TestingBot
  - https://testingbot.com/support/accessibility/webdriverio.html
  - Step-by-step guide with wdio
- **Automated Accessibility: Comparing axe + WDIO and Pa11y-ci** | Abstracta (May 2025)
  - https://abstracta.us/blog/accessibility-testing/automated-accessibility-testing-comparing-axe-wdio-and-pa11y-ci/
  - Comparison of accessibility testing approaches
- **Salesforce sa11y Library** | https://github.com/salesforce/sa11y
  - WebdriverIO integration patterns for a11y testing

## GitHub Issues & PRs
- **WebdriverIO Accessibility Docs PR** | https://github.com/webdriverio/webdriverio/pull/9392
  - Context on wdio accessibility capabilities
- **WDIO Automated Accessibility Test Discussion** | Issue #2303
  - Historical discussion on accessibility in WDIO

## Key Concepts
1. WCAG 2.0/2.1 AA compliance
2. Axe Core integration
3. Automated vs manual a11y testing
4. Section 508 compliance
5. WAI-ARIA validation
6. Accessibility reporting and thresholds

## Axe-Core Configuration
```typescript
import AxeBuilder from '@axe-core/webdriverio';
const builder = new AxeBuilder({ client: browser });
const results = await builder.analyze();
```

## Standards
- WCAG 2.1 Level AA (most common target)
- Section 508 (US Government)
- EN 301 549 (European accessibility standard)

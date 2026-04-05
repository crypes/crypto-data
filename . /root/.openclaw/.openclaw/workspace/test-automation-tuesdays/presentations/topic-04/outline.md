# Topic 4: Flaky Tests & Reliability
## Learning Objectives
By the end of this session, participants will be able to:
- Identify common causes of flaky tests
- Implement strategies to improve test reliability
- Utilize retry mechanisms for unstable tests

### Presentation Outline (15-20 minutes)

1.  **Introduction: The Flaky Test Problem (3 min)**
    *   What are flaky tests?
    *   Impact on confidence and CI/CD pipelines
    *   Common culprits.

2.  **Causes of Flakiness (7 min)**
    *   **Timing Issues:** Race conditions, missing waits
    *   **Environment Dependencies:** Unstable test data, shared state
    *   **Locator Fragility:** Poorly chosen selectors
    *   **Async Operations:** Unhandled promises
    *   **Browser State:** Cross-test contamination

3.  **Strategies for Reliability (7 min)**
    *   **Explicit Waits:** Using `browser.waitUntil`, `element.waitForExist`, etc.
    *   **Reliable Locators:** Preferring `data-testid` or unique attributes.
    *   **Test Isolation:** Resetting state between tests.
    *   **Mocking:** Isolating dependencies.
    *   **Retry Mechanisms:** Configuring retries in WebdriverIO.

4.  **Demo: Implementing Retries & Waits (5 min)**
    *   Show adding `browser.waitUntil` to a previously unstable step.
    *   Configure `specFileRetries` in `wdio.conf.ts`.
    *   Demonstrate a test that fails once and passes on retry.

5.  **Q&A / Wrap-Up (3 min)**
    *   Best practices summary
    *   Preview of CI/CD Integration

### Demo Script (5 minutes)

**Objective:** Show how to implement waits and retries.

**Step 1: Add Explicit Wait (2 min)**
- Modify login test to wait for the alert message element:
```typescript
// In login.steps.ts
Then(/^I should see the welcome message$/, async () => {
    // Instead of direct expect, wait for element to exist first
    await expect($('#flash')).toBeExisting(); // WDIO automatically waits here
    await expect($('#flash')).toHaveText(expect.stringContaining('You logged into a secure area!'));
});
```

**Step 2: Configure Retries (2 min)**
- In `wdio.conf.ts`:
```typescript
export const config = {
    // ... other configs
    specFileRetries: 2, // Retry a failing spec up to 2 times
    specFileRetriesDelay: 5, // Wait 5 seconds before retrying
};
```

**Step 3: Simulate Flakiness (Optional - 1 min)**
- Briefly show how a test might fail randomly (e.g., by adding a random condition).
- Run the test and observe the retry mechanism in action.

### Resources
- WDIO Docs on Retries: https://webdriver.io/docs/retry/
- WDIO Docs on Waits: https://webdriver.io/docs/timeouts/
- Articles on identifying flaky test causes

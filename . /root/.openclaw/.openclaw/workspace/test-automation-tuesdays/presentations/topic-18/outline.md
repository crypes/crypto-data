# Topic 18: Testing SPAs (React, Vue, Angular)
## Learning Objectives
By the end of this session, participants will be able to:
- Understand the unique challenges of testing SPAs
- Apply strategies for robust SPA testing with tools like WebdriverIO
- Differentiate between component and E2E testing for SPAs

### Presentation Outline (20-25 minutes)

1.  **Introduction to SPAs (3 min)**
    *   What are SPAs? (Client-side routing, dynamic rendering)
    *   How they differ from traditional multi-page apps
    *   Examples: React, Vue, Angular

2.  **Challenges in SPA Testing (5 min)**
    *   Waiting for dynamic content & async operations
    *   Client-side routing and deep links
    *   State management complexities
    *   Debugging nuances

3.  **Testing Strategies & Tools (10 min)**
    *   **Component Testing:**
        *   Tools: Testing Library (React, Vue, Angular), Jest/Vitest
        *   Focus: Isolating UI components
    *   **End-to-End (E2E) Testing:**
        *   Tools: WebdriverIO, Playwright, Cypress
        *   Focus: User journeys, full application flow
    *   **Key Techniques:**
        *   Explicit waits
        *   Robust locators
        *   API mocking (MSW)

# Demo Script (10 min)

**Objective:** Show how to write robust E2E tests for an SPA using WebdriverIO.

**Scenario:** Test a simple SPA login flow with dynamic content.

**Tool:** A simple React SPA demo app (or use http://the-internet.herokuapp.com/login if SPA features are limited)

**Step 1: Project Setup (2 min)**
- Assume basic WDIO + TS setup.
- Highlight `wdio.conf.ts` for waits and services.

**Step 2: Test Login Flow (5 min)**
- **Given:** I am on the login page. (`await browser.url(...)`)
- **When:** I enter username and password. (`await $('#username').setValue(...)`)
- **And:** I click the login button. (`await $('button[type="submit"]').click()`)
- **Then:** I should see the welcome message. (`await expect($('#flash')).toHaveText(...)`)

**Step 3: Handling Dynamic Content (3 min)**
- **Scenario:** A user dashboard that loads after login.
- Show how to wait for a specific element to appear or for text to change.
```typescript
// In login.steps.ts
// Waiting for dynamic content after login
Then(/^I should see the dashboard$/, async () => {
    await expect($('#dashboard-welcome')).toBeExisting(); // Wait for dashboard element
    await expect($('#dashboard-welcome')).toHaveTextContaining('Welcome,'); // Wait for specific text
});
```

### Resources
- WDIO Docs on Waits: https://webdriver.io/docs/timeouts
- Testing Library (React/Vue/Angular)
- MSW for API mocking

### Assessment Questions
1. What is the main difference between component testing and E2E testing for SPAs?
2. Why are explicit waits crucial for SPAs?
3. How can API mocking improve SPA test stability?

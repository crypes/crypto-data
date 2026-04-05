# Topic 3: Test Architecture Patterns
## Learning Objectives
By the end of this session, participants will be able to:
- Understand common test automation design patterns (POM, Screenplay)
- Differentiate between patterns and their use cases
- Apply best practices for structuring test code

### Presentation Outline (15-20 minutes)

1.  **Introduction: Why Design Patterns? (3 min)**
    *   Maintainability, reusability, readability
    *   Scalability of test suites

2.  **The Page Object Model (POM) (5 min)**
    *   Concept: Encapsulating elements and actions per page.
    *   Benefits: DRY principle, better organization.
    *   Demo: Simple POM implementation.

3.  **The Screenplay Pattern (5 min)**
    *   Concept: Actor-centric, interaction-based testing.
    *   Benefits: More readable, business-oriented tests.
    *   Comparison with POM.

4.  **Other Patterns (3 min)**
    *   App Actions / Component Objects
    *   Data Builders / Factories

5.  **Q&A / Wrap-Up (2 min)**
    *   Choosing the right pattern for your project
    *   Preview of Flaky Tests topic

### Demo Script (POM Example - 5 min)
**Objective:** Illustrate the Page Object Model structure.

**Scenario:** Login test.

**Step 1: Create Page Object (`LoginPage.ts`)**
```typescript
class LoginPage {
    get usernameInput() { return $('#username'); }
    get passwordInput() { return $('#password'); }
    get submitButton() { return $('button[type="submit"]'); }

    async login(username: string, password: string) {
        await this.usernameInput.setValue(username);
        await this.passwordInput.setValue(password);
        await this.submitButton.click();
    }
}
export default new LoginPage();
```

**Step 2: Update Step Definition (`login.steps.ts`)**
```typescript
import LoginPage from '../pages/LoginPage'; // Import the page object

When(/^I enter valid credentials$/, async () => {
    await LoginPage.login('tomsmith', 'SuperSecretPassword!');
});
```

### Resources
- WDIO Docs on Page Objects: https://webdriver.io/docs/pageobjects/
- Screenplay Pattern resources links
- POM vs Screenplay comparison articles

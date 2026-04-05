# Topic 2: Advanced BDD Patterns
## Hooks, Tags, Retry & Parallel Execution

### Learning Objectives
By the end of this session, participants will be able to:
- Implement Cucumber hooks for setup/teardown
- Use tags to organize and filter tests
- Configure parallel execution
- Implement retry strategies for flaky tests

### Presentation Outline (15-20 minutes)

1. **Recap of Topic 1 (2 min)**
   - Quick review of basic BDD setup

2. **Cucumber Hooks (5 min)**
   - Before/After hooks
   - BeforeStep/AfterStep hooks
   - Hook scope and order

3. **Tags for Organization (4 min)**
   - Tag syntax and naming conventions
   - Running tests by tags
   - Tag-based CI/CD integration

4. **Parallel Execution (4 min)**
   - Configuring maxInstances
   - Spec file parallelization
   - Feature-level vs Scenario-level parallelism

5. **Handling Flaky Tests (4 min)**
   - Retry strategies
   - Identifying root causes
   - Best practices

6. **Q&A (1 min)**

### Demo Script Steps

**Step 1: Set up Hooks (3 min)**
Create `features/support/hooks.ts`:
```typescript
import { Before, After, BeforeStep, AfterStep } from '@wdio/cucumber-framework';

Before(async function (scenario) {
    console.log(`Starting scenario: ${scenario.pickle.name}`);
    // Reset app state
});

After(async function (scenario) {
    if (scenario.result?.status === 'FAILED') {
        const screenshot = await browser.takeScreenshot();
        this.attach(screenshot, 'image/png');
    }
});
```

**Step 2: Add Tags to Features (3 min)**
Modify features:
```gherkin
@smoke @critical
Feature: Login
  
  @fast
  Scenario: Successful login
    ...
    
  @slow @regression
  Scenario: Forgot password flow
    ...
```

**Step 3: Configure wdio.conf.ts (4 min)**
```typescript
export const config = {
    // Parallel execution
    maxInstances: 3,
    
    // Retry failing specs
    specFileRetries: 2,
    specFileRetriesDelay: 5, // seconds
    
    cucumberOpts: {
        // Run only smoke tests
        tagExpression: '@smoke and not @wip',
    }
};
```

**Step 4: Run Tagged Tests (3 min)**
```bash
# Run only smoke tests
npm run wdio -- --cucumberOpts.tagExpression='@smoke'

# Run tests excluding slow
npm run wdio -- --cucumberOpts.tagExpression='not @slow'
```

**Step 5: Show Retry in Action (2 min)**
Deliberately add a flaky test and show retry behavior.

### Assessment Questions
1. When would you use BeforeStep vs Before?
2. How do you run only @smoke tests in CI?
3. What's the difference between specFileRetries and retries?

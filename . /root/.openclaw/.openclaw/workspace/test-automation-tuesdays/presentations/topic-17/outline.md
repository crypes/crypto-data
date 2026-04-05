# Topic 17: Test Data & Environment Management
## Learning Objectives
By the end of this session, participants will be able to:
- Understand different types of test data and sources
- Implement strategies for managing test data reliably
- Configure and manage test environments effectively
- Address data privacy and isolation challenges

### Presentation Outline (20-25 minutes)

1.  **Introduction: Why Data & Environments Matter (3 min)**
    *   Impact on test reliability and accuracy
    *   Common pitfalls (data corruption, environment drift)

2.  **Test Data Management (8 min)**
    *   **Types of Test Data:** Valid, invalid, boundary, edge cases
    *   **Data Sources:** Databases, APIs, files, synthetic generation
    *   **Data Generation Tools:** Faker.js, Mockaroo
    *   **Data Masking & Anonymization:** Importance for privacy (GDPR/CCPA)
    *   **Data Isolation:** Ensuring tests don't interfere

3.  **Environment Management (7 min)**
    *   Dev/Test/Staging/Prod paradigms
    *   Containerization (Docker) for consistency
    *   CI/CD integration for automated environments
    *   Cloud-based environments

4.  **Demo: Simple Data Generation & Reset (5 min)**
    *   Use Faker.js to generate user data for a signup form test.
    *   Show a simple data reset strategy (e.g., database rollback or cleanup script).

5.  **Q&A / Wrap-Up (2 min)**
    *   Best practices for test data & environments
    *   Preview of SPA Testing

### Demo Script (3-5 minutes)

**Objective:** Demonstrate generating test data and a basic environment reset.

**Tools:** Node.js, Faker.js, basic test script (e.g., a simple form submission)

**Step 1: Introduce Faker.js (2 min)**
- Install Faker: `npm install @faker-js/faker`
- Show basic data generation:
```javascript
const { faker } = require('@faker-js/faker');

const username = faker.internet.userName();
const password = faker.internet.password();
console.log(`Generated User: ${username}, ${password}`);
```

**Step 2: Integrate into Test (2 min)**
- Show a simple test script that uses generated data to fill a form.
- `await page.locator('#username').fill(username);`

**Step 3: Environment Reset Strategy (1 min)**
- Explain the concept: database rollback, API delete call, or cleanup function.
- Show a placeholder for a cleanup function: `async function cleanupTestData() { /* ... */ }`

### Resources
- Faker.js documentation
- Docker documentation
- Links from `research.md`

### Assessment Questions
1. What is the difference between valid and invalid test data?
2. Why is data isolation important?
3. How does Docker help with environment management?

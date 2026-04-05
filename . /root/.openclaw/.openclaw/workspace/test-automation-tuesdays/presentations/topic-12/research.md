# Research: Mock Server Integration & Backend Stubs

## Official Documentation
- **WebdriverIO Mocks and Spies** | https://webdriver.io/docs/mocksandspies/
  - Built-in network mocking
- **WebdriverIO WireMock Service** | https://webdriver.io/docs/wdio-wiremock-service/
  - HTTP stubbing with WireMock
- **WireMock Service (Old)** | https://webdriver.io/docs/wdio-wiremock-service.html
  - Original documentation
- **WebdriverIO WireMock Blog** | https://webdriver.io/blog/2019/12/05/wiremock.html
  - Tutorial on WireMock integration

## Key Concepts
1. WireMock for HTTP stubbing
2. MSW (Mock Service Worker)
3. Local API mocking
4. JSON Server for fake backends
5. Mock persistence
6. Dynamic response generation

## Mocking Strategies
- Frontend interception (browser-level)
- Backend stubbing (separate service)
- Full API mocking
- Selective request interception

## Use Cases
1. Testing error scenarios (500, 404)
2. Unfinished backend features
3. Third-party service isolation
4. Performance testing
5. Regressive testing with known states

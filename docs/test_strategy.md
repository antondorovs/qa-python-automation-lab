# Test strategy

- **API:** exercise the local HTTP server through the same network boundary a
  real client uses. Cover success, missing resources, invalid input and response
  shape. Every test starts with fresh in-memory users.
- **Data:** run SQL rules against an in-memory SQLite fixture. The baseline
  records known training defects; a separate test adds a defect to show that
  the rules detect drift.
- **UI:** use Playwright with a real Chromium browser against the local page.
  It runs separately because browser installation is larger than core pytest.
- **CI:** lint and core tests run in one job; the browser has its own job on
  GitHub Actions and GitLab CI. Both publish JUnit and QA summary reports even
  if a test fails.

When adapting this lab to a real system, replace the local server with an
environment-specific base URL and avoid putting credentials in source files.

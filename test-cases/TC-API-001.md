# TC-API-001: Reject a user without an email

- Area: local users API
- Priority: high
- Preconditions: the local test server is running with its initial users
- Test data: `{"name": "Carla"}`

## Steps

1. Send `POST /api/users` with the JSON test data.
2. Read the HTTP status and response body.
3. Send `GET /api/users`.

## Expected result

The POST returns HTTP 400 and `{"error": "name and email are required"}`.
The users collection still has two records; no incomplete user was created.

Automated coverage: `tests/api/test_users.py::test_invalid_create_is_rejected`.

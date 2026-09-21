# BUG-DATA-001: Duplicate email appears in the users fixture

Training example based on an intentional data defect in `data/fixture.sql`.

- Environment: local SQLite training fixture
- Severity: medium
- Priority: normal
- Preconditions: load `data/fixture.sql` into a fresh SQLite database

## Steps to reproduce

1. Group users by `lower(trim(email))`.
2. Filter groups with more than one record.

## Expected result

Each normalized email belongs to one user.

## Actual result

`anna@example.com` and `ANNA@example.com` belong to two different users.
The `duplicate_emails` rule reports one duplicate group.

## Evidence

```sql
SELECT lower(trim(email)), COUNT(*)
FROM users
GROUP BY lower(trim(email))
HAVING COUNT(*) > 1;
```

Automated coverage: `tests/data/test_quality.py::test_known_quality_baseline`.

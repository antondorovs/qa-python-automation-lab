from pathlib import Path

import pytest

from qa_python_lab.data_quality import BASELINE, evaluate_rules, load_fixture


@pytest.mark.data
@pytest.mark.contract
def test_schema_contract(fixture_sql: Path) -> None:
    expected_columns = {
        "users": ["id", "name", "email"],
        "orders": ["id", "user_id", "status", "amount"],
        "payments": ["id", "order_id", "status"],
    }
    with load_fixture(fixture_sql) as connection:
        actual_columns = {
            table: [row[1] for row in connection.execute(f"PRAGMA table_info({table})")]
            for table in expected_columns
        }
    assert actual_columns == expected_columns


@pytest.mark.data
@pytest.mark.contract
def test_known_quality_baseline(fixture_sql: Path) -> None:
    with load_fixture(fixture_sql) as connection:
        results = evaluate_rules(connection)
    assert {result.name: result.actual for result in results} == BASELINE
    assert all(result.passed for result in results)


@pytest.mark.data
def test_new_bad_order_changes_baseline(fixture_sql: Path) -> None:
    with load_fixture(fixture_sql) as connection:
        connection.execute("INSERT INTO orders VALUES (5, 999, 'PAID', -1)")
        results = {result.name: result for result in evaluate_rules(connection)}
    assert results["orphan_orders"].actual == BASELINE["orphan_orders"] + 1
    assert results["non_positive_amounts"].actual == BASELINE["non_positive_amounts"] + 1
    assert results["paid_without_payment"].actual == BASELINE["paid_without_payment"] + 1
    assert not results["orphan_orders"].passed

from qa_python_lab.qa_report import QaTestResult, build_summary, render_markdown


def test_ready_gate_counts_skipped_separately() -> None:
    summary = build_summary([
        QaTestResult("tests/api/test_users.py::test_get", "passed", 12, ("api", "smoke")),
        QaTestResult("tests/ui/test_home.py::test_home", "skipped", 0, ("ui",)),
    ])
    assert summary["executed"] == 1
    assert summary["pass_rate"] == 100.0
    assert summary["tag_counts"] == {"api": 1, "smoke": 1, "ui": 1}
    assert summary["quality_gate"] == {"status": "ready", "reasons": []}
    markdown = render_markdown(summary)
    assert "## Markers" in markdown
    assert "- `api`: 1" in markdown
    assert "**passed**" in markdown


def test_failed_and_interrupted_tests_block_gate() -> None:
    summary = build_summary([
        QaTestResult("test_one", "failed", 20, error="assert 1 == 2"),
        QaTestResult("test_two", "interrupted", 0),
    ], exit_code=1)
    assert summary["pass_rate"] == 0.0
    assert summary["quality_gate"]["status"] == "blocked"
    assert summary["quality_gate"]["reasons"] == [
        "1 failed test(s)",
        "1 interrupted test(s)",
    ]


def test_empty_run_is_blocked() -> None:
    summary = build_summary([], exit_code=5)
    assert summary["quality_gate"]["status"] == "blocked"
    assert "No tests executed" in summary["quality_gate"]["reasons"]


def test_markdown_shows_duration_tags_and_failure_hint() -> None:
    summary = build_summary([
        QaTestResult(
            "tests/api/test_users.py::test_get",
            "failed",
            27,
            ("api", "smoke"),
            "assert response.status == 200\nAssertionError: got 500\n",
        ),
    ])
    markdown = render_markdown(summary)
    assert "Duration: 27 ms" in markdown
    assert "(27 ms; tags: api, smoke)" in markdown
    assert "Failure: AssertionError: got 500" in markdown

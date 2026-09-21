from qa_python_lab.bug_report import BugReport


def test_bug_report_contains_reproduction_and_outcome() -> None:
    report = BugReport(
        title="User lookup returns 500",
        steps=("Open the users endpoint", "Request user 1"),
        expected="HTTP 200 with user data",
        actual="HTTP 500",
    )
    markdown = report.to_markdown()
    assert "1. Open the users endpoint" in markdown
    assert "2. Request user 1" in markdown
    assert "HTTP 200 with user data" in markdown
    assert "HTTP 500" in markdown

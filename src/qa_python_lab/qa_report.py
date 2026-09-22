"""Compact, machine-readable QA run summary and quality gate."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

Status = Literal["passed", "failed", "skipped", "interrupted"]


@dataclass(frozen=True)
class QaTestResult:
    nodeid: str
    status: Status
    duration_ms: int
    tags: tuple[str, ...] = ()
    error: str | None = None


def build_summary(results: list[QaTestResult], exit_code: int = 0) -> dict[str, object]:
    counts = {status: sum(result.status == status for result in results) for status in (
        "passed", "failed", "skipped", "interrupted"
    )}
    executed = counts["passed"] + counts["failed"] + counts["interrupted"]
    pass_rate = round(100 * counts["passed"] / executed, 2) if executed else 0.0
    reasons: list[str] = []
    if executed == 0:
        reasons.append("No tests executed")
    if counts["failed"]:
        reasons.append(f"{counts['failed']} failed test(s)")
    if counts["interrupted"]:
        reasons.append(f"{counts['interrupted']} interrupted test(s)")
    if exit_code and not counts["failed"] and not counts["interrupted"]:
        reasons.append(f"pytest exited with code {exit_code}")

    return {
        "total": len(results),
        "executed": executed,
        "passed": counts["passed"],
        "failed": counts["failed"],
        "skipped": counts["skipped"],
        "interrupted": counts["interrupted"],
        "pass_rate": pass_rate,
        "duration_ms": sum(result.duration_ms for result in results),
        "quality_gate": {"status": "blocked" if reasons else "ready", "reasons": reasons},
        "tests": [asdict(result) for result in results],
    }


def render_markdown(summary: dict[str, object]) -> str:
    gate = summary["quality_gate"]
    assert isinstance(gate, dict)
    tests = summary["tests"]
    assert isinstance(tests, list)
    lines = [
        "# QA run summary",
        "",
        f"Quality gate: **{gate['status']}**",
        "",
        f"Executed: {summary['executed']} / {summary['total']}",
        f"Passed: {summary['passed']}",
        f"Failed: {summary['failed']}",
        f"Skipped: {summary['skipped']}",
        f"Interrupted: {summary['interrupted']}",
        f"Pass rate: {summary['pass_rate']}%",
        f"Duration: {summary['duration_ms']} ms",
    ]
    reasons = gate["reasons"]
    if reasons:
        lines.extend(["", "## Blocking reasons", ""])
        lines.extend(f"- {reason}" for reason in reasons)
    lines.extend(["", "## Tests", ""])
    for result in tests:
        tags = f"; tags: {', '.join(result['tags'])}" if result["tags"] else ""
        lines.append(
            f"- **{result['status']}** `{result['nodeid']}` "
            f"({result['duration_ms']} ms{tags})"
        )
        if result["error"]:
            last_line = next(
                (line.strip() for line in reversed(result["error"].splitlines()) if line.strip()),
                None,
            )
            if last_line:
                lines.append(f"  - Failure: {last_line}")
    return "\n".join(lines) + "\n"

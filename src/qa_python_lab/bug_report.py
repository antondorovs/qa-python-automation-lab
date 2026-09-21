"""Turn a reproducible failure into a short Markdown bug report."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BugReport:
    title: str
    steps: tuple[str, ...]
    expected: str
    actual: str
    environment: str = "local"

    def to_markdown(self) -> str:
        steps = "\n".join(f"{number}. {step}" for number, step in enumerate(self.steps, 1))
        return (
            f"# {self.title}\n\nEnvironment: {self.environment}\n\n"
            f"## Steps to reproduce\n{steps}\n\n"
            f"## Expected\n{self.expected}\n\n## Actual\n{self.actual}\n"
        )

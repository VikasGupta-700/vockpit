from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True, order=False)
class Finding:
    rule: str
    severity: str
    location: str
    message: str

    def __str__(self) -> str:
        return f"{self.rule} {self.severity} {self.location}: {self.message}"

    def __lt__(self, other: Finding) -> bool:
        if not isinstance(other, Finding):
            return NotImplemented
        return (self.rule, self.location, self.message, self.severity) < (
            other.rule,
            other.location,
            other.message,
            other.severity,
        )


def format_findings(findings: Sequence[Finding]) -> str:
    sorted_findings = sorted(findings)
    return "\n".join(str(f) for f in sorted_findings)

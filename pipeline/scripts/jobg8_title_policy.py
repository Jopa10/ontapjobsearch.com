"""Hard title exclusions shared by JobG8 selection and publication guards."""

from __future__ import annotations

import re
from typing import Any


ACCOUNTANT_ROLE_TITLE_RE = re.compile(
    r"\baccountants?\b|\baccounts?\s+(?:senior|semi[-\s]?senior)\b",
    re.IGNORECASE,
)


def is_jobg8_accountant_title(job: dict[str, Any]) -> bool:
    """Whether a JobG8 row has an owner-excluded Accountant title.

    Missing source values are treated as JobG8, matching the legacy output
    convention used by the pipeline. Other providers remain unaffected.
    """
    source = job.get("source", "JobG8")
    source = source.strip().casefold() if isinstance(source, str) else ""
    if source != "jobg8":
        return False
    title = job.get("title", "")
    title = " ".join(title.casefold().split()) if isinstance(title, str) else ""
    return bool(ACCOUNTANT_ROLE_TITLE_RE.search(title))

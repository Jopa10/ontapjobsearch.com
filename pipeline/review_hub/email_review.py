from __future__ import annotations

import argparse
from email.message import EmailMessage
import os
from pathlib import Path
import re
import smtplib

from .master_review import DEFAULT_MASTER


def _summary(path: Path) -> tuple[int, list[str], list[str]]:
    text = path.read_text(encoding="utf-8-sig")
    count_match = re.search(r"\*\*(\d+) job\(s\) need a human decision\.\*\*", text)
    count = int(count_match.group(1)) if count_match else 0
    rows: list[str] = []
    attention: list[str] = []
    in_table = False
    for raw in text.splitlines():
        line = raw.strip()
        if line == "| Source | Status | Review date | Needs review | Note |":
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and not line.startswith("|"):
            break
        if not in_table or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        source, state, review_date, needs, _note = cells[:5]
        rows.append(f"{source}: {needs} to review — {state} ({review_date})")
        if state not in {"OK", "FUTURE"}:
            attention.append(source)
    return count, rows, attention


def send(path: Path = DEFAULT_MASTER) -> bool:
    to_addr = os.getenv("ONTAP_REVIEW_EMAIL_TO", "").strip()
    host = os.getenv("ONTAP_SMTP_HOST", "").strip()
    username = os.getenv("ONTAP_SMTP_USERNAME", "").strip()
    password = os.getenv("ONTAP_SMTP_PASSWORD", "")
    from_addr = os.getenv("ONTAP_REVIEW_EMAIL_FROM", "").strip() or username
    if not all((to_addr, host, from_addr)):
        print(
            "Review email not configured; set ONTAP_REVIEW_EMAIL_TO, "
            "ONTAP_SMTP_HOST and ONTAP_REVIEW_EMAIL_FROM/ONTAP_SMTP_USERNAME."
        )
        return False

    count, rows, attention = _summary(path)
    suffix = (
        f" — ATTENTION: {len(attention)} source(s) stale/missing"
        if attention
        else ""
    )
    msg = EmailMessage()
    msg["Subject"] = f"Ontap daily review — {count} jobs need review{suffix}"
    msg["From"] = from_addr
    msg["To"] = to_addr
    review_url = os.getenv(
        "ONTAP_REVIEW_URL",
        "https://github.com/Jopa10/ontapjobsearch.com/blob/main/"
        "pipeline/reviews/daily/ontap-daily-review.md",
    )
    body = [
        f"{count} jobs need your decision today.",
        "",
        *rows,
        "",
        f"Open the one review file: {review_url}",
        "",
        "The same review file is attached to this email for reference.",
        "",
        "Edit only action: lines (select / exclude), commit the GitHub file, then run "
        "Apply and publish Ontap daily review.",
    ]
    if attention:
        body.extend(
            [
                "",
                "Attention: "
                + ", ".join(attention)
                + " did not provide a current review and must not be treated "
                "as zero inventory.",
            ]
        )
    msg.set_content("\n".join(body) + "\n")
    msg.add_attachment(
        path.read_bytes(),
        maintype="text",
        subtype="markdown",
        filename=path.name,
    )

    port = int(os.getenv("ONTAP_SMTP_PORT", "").strip() or "587")
    use_ssl = os.getenv("ONTAP_SMTP_SSL", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }
    smtp_cls = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP
    with smtp_cls(host, port, timeout=30) as client:
        if not use_ssl:
            client.starttls()
        if username:
            client.login(username, password)
        client.send_message(msg)
    print(f"Sent Ontap review email to {to_addr}")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", type=Path, default=DEFAULT_MASTER)
    args = parser.parse_args(argv)
    send(args.review)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

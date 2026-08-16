"""Source-mix guard for Ontap slice composition.

This module belongs at composition/publish time, after individual sources have
been fetched, normalised, selected and deduplicated. It never deletes existing
rows. It decides which new rows may be added without allowing external inventory
to dominate a normal Ontap slice.

Default policy:
* all non-JobG8 rows combined: <= 30% of the composed slice;
* any one external source: <= 25% of the composed slice.

Rows that cannot be added are returned as deferred with explicit reasons. They
are not silently discarded.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable

JOBG8_SOURCE = "JobG8"
MAX_NON_JOBG8_SHARE = 0.30
MAX_SINGLE_EXTERNAL_SOURCE_SHARE = 0.25

REASON_NON_JOBG8_CAP = "NON_JOBG8_CAP"
REASON_SINGLE_EXTERNAL_SOURCE_CAP = "SINGLE_EXTERNAL_SOURCE_CAP"
REASON_MISSING_SOURCE = "MISSING_SOURCE"


def _text(value: object) -> str:
    return str(value or "").strip()


def _source_key(value: object) -> str:
    return _text(value).casefold()


def _source_label(row: dict[str, Any]) -> str:
    return _text(row.get("source"))


@dataclass(frozen=True)
class MixMetrics:
    total: int
    jobg8: int
    non_jobg8: int
    non_jobg8_share: float
    source_counts: dict[str, int]
    source_shares: dict[str, float]


@dataclass(frozen=True)
class DeferredRow:
    row: dict[str, Any]
    reasons: tuple[str, ...]


@dataclass
class SourceMixResult:
    existing_rows: list[dict[str, Any]]
    accepted_rows: list[dict[str, Any]]
    deferred_rows: list[DeferredRow]
    max_non_jobg8_share: float
    max_single_external_source_share: float

    @property
    def final_rows(self) -> list[dict[str, Any]]:
        return [*self.existing_rows, *self.accepted_rows]

    @property
    def metrics(self) -> MixMetrics:
        return mix_metrics(self.final_rows)


def mix_metrics(
    rows: Iterable[dict[str, Any]],
    *,
    jobg8_source: str = JOBG8_SOURCE,
) -> MixMetrics:
    materialised = list(rows)
    total = len(materialised)
    jobg8_key = _source_key(jobg8_source)

    canonical_labels: dict[str, str] = {}
    keyed_counts: Counter[str] = Counter()
    for row in materialised:
        label = _source_label(row) or "(unknown source)"
        key = _source_key(label)
        canonical_labels.setdefault(key, label)
        keyed_counts[key] += 1

    jobg8 = keyed_counts.get(jobg8_key, 0)
    non_jobg8 = total - jobg8
    counts = {
        canonical_labels[key]: count
        for key, count in sorted(
            keyed_counts.items(),
            key=lambda item: canonical_labels[item[0]].casefold(),
        )
    }
    shares = {
        label: (count / total if total else 0.0)
        for label, count in counts.items()
    }
    return MixMetrics(
        total=total,
        jobg8=jobg8,
        non_jobg8=non_jobg8,
        non_jobg8_share=(non_jobg8 / total if total else 0.0),
        source_counts=counts,
        source_shares=shares,
    )


def _candidate_reasons(
    current_rows: list[dict[str, Any]],
    candidate: dict[str, Any],
    *,
    jobg8_source: str,
    max_non_jobg8_share: float,
    max_single_external_source_share: float,
) -> tuple[str, ...]:
    source = _source_label(candidate)
    if not source:
        return (REASON_MISSING_SOURCE,)

    source_key = _source_key(source)
    jobg8_key = _source_key(jobg8_source)
    if source_key == jobg8_key:
        return ()

    proposed = [*current_rows, candidate]
    metrics = mix_metrics(proposed, jobg8_source=jobg8_source)
    reasons: list[str] = []
    epsilon = 1e-12

    if metrics.non_jobg8_share > max_non_jobg8_share + epsilon:
        reasons.append(REASON_NON_JOBG8_CAP)

    source_count = sum(
        1 for row in proposed if _source_key(_source_label(row)) == source_key
    )
    source_share = source_count / len(proposed)
    if source_share > max_single_external_source_share + epsilon:
        reasons.append(REASON_SINGLE_EXTERNAL_SOURCE_CAP)

    return tuple(reasons)


def apply_source_mix_policy(
    existing_rows: Iterable[dict[str, Any]],
    candidate_rows: Iterable[dict[str, Any]],
    *,
    jobg8_source: str = JOBG8_SOURCE,
    max_non_jobg8_share: float = MAX_NON_JOBG8_SHARE,
    max_single_external_source_share: float = MAX_SINGLE_EXTERNAL_SOURCE_SHARE,
) -> SourceMixResult:
    """Accept as many candidate rows as fit the configured source-mix limits.

    Existing rows are never removed, even if a slice is already above a limit.
    In that situation further external additions are deferred until the mix
    returns within policy. JobG8 additions are always permitted because they can
    only reduce the external share.
    """
    if not 0 <= max_non_jobg8_share < 1:
        raise ValueError("max_non_jobg8_share must be in [0, 1)")
    if not 0 <= max_single_external_source_share < 1:
        raise ValueError("max_single_external_source_share must be in [0, 1)")

    existing = [dict(row) for row in existing_rows]
    accepted: list[dict[str, Any]] = []
    deferred: list[DeferredRow] = []

    for source_row in candidate_rows:
        row = dict(source_row)
        current = [*existing, *accepted]
        reasons = _candidate_reasons(
            current,
            row,
            jobg8_source=jobg8_source,
            max_non_jobg8_share=max_non_jobg8_share,
            max_single_external_source_share=max_single_external_source_share,
        )
        if reasons:
            deferred.append(DeferredRow(row=row, reasons=reasons))
        else:
            accepted.append(row)

    return SourceMixResult(
        existing_rows=existing,
        accepted_rows=accepted,
        deferred_rows=deferred,
        max_non_jobg8_share=max_non_jobg8_share,
        max_single_external_source_share=max_single_external_source_share,
    )


def prioritise_nhs_open_switch(
    rows: Iterable[dict[str, Any]],
    *,
    source: str = "NHS Jobs",
) -> list[dict[str, Any]]:
    """Stable-order NHS candidates so OPEN_SWITCH rows get capacity first.

    Non-NHS rows keep their relative position. This helper is intended when an
    NHS candidate batch is passed to the source-mix guard; it does not classify
    jobs itself.
    """
    materialised = [dict(row) for row in rows]
    target = _source_key(source)

    indexed = list(enumerate(materialised))
    return [
        row
        for _index, row in sorted(
            indexed,
            key=lambda item: (
                0
                if (
                    _source_key(_source_label(item[1])) == target
                    and _source_key(item[1].get("switchability")) == "open_switch"
                )
                else 1,
                item[0],
            ),
        )
    ]


def workflow_summary_line(slice_label: str, result: SourceMixResult) -> str:
    """Return one concise line suitable for a GitHub Actions step summary."""
    metrics = result.metrics
    deferred = len(result.deferred_rows)
    status = "CAP APPLIED" if deferred else "OK"
    return (
        f"{slice_label}: {status} — accepted {len(result.accepted_rows)}, "
        f"deferred {deferred}; non-JobG8 {metrics.non_jobg8}/{metrics.total} "
        f"({metrics.non_jobg8_share:.1%})."
    )

# Teaching Vacancies regional operating playbook

## Purpose and source boundary

This is the cradle-to-grave operating process for Teaching Vacancies as an
Ontap external source.

Teaching Vacancies covers state-funded school and college vacancies in
**England**. Discovery is source-wide and region-neutral: it is not restricted
to Yorkshire, but it must not be described as providing Scottish, Welsh or
Northern Irish coverage.

The process supports any Ontap region that:

1. can be resolved through the existing geographic lookup;
2. has an explicit admin/service entry in the existing slice register; and
3. has a current non-empty JobG8/other regional output to compose with.

## Authorities that must not be duplicated

Two existing files remain authoritative:

- `pipeline/geo/geo_lookup.xlsx` assigns factual locations to geographic
  clusters and Ontap regions.
- `pipeline/registers/region_category_slice_register.csv` controls whether a
  region/category is `LIVE`, `CANDIDATE` or otherwise unavailable.

There is no Teaching Vacancies regional registry.

A missing slice entry never implies `LIVE`. Unresolved geography is never
inferred or silently assigned. `CANDIDATE` vacancies may be discovered,
routed and reviewed, but they cannot produce an approved snapshot or enter a
live combined output.

## End-to-end architecture

The controlled stages are:

1. **Discovery** — complete England-wide source sweep and factual manifest.
2. **Routing** — exact geographic assignment plus unresolved output.
3. **Regional review** — separate review files, classification and regional
   JobG8 duplicate checks.
4. **Regional approval** — one explicitly approved `LIVE` region at a time.
5. **Composition** — replace only that source's subset while preserving
   JobG8, NEJobs, VONNE and other jobs.
6. **Publication** — the existing verified publisher remains the final gate.

Each stage verifies the previous stage's hashes, counts or fingerprints. Later
stages do not silently repair or guess around incomplete earlier evidence.

## Stage 1 — run the England-wide review workflow

Run the GitHub Actions workflow:

**Run Teaching Vacancies regional review**

The workflow:

- fetches every advertised page from the national Administration, HR, data and
  finance listing and the configured national keyword coverage routes;
- performs two complete sweeps and requires the same URL/provenance set;
- fetches every discovered vacancy detail page;
- writes a factual pre-geography manifest and completeness evidence;
- routes every record through `geo_lookup.xlsx`;
- writes a separate unresolved-geography CSV;
- attaches `LIVE`, `CANDIDATE` or `UNREGISTERED` status from the slice register;
- compares each routed vacancy only with the current JobG8 rows for that
  region;
- writes separate regional CSV and Markdown reviews; and
- commits only manifests and review artifacts.

It cannot write approved snapshots, combined pipeline output or `app/` files.

The principal artifacts are:

```text
pipeline/manifests/external/teaching-vacancies/
  teaching-vacancies-discovery-YYYY-MM-DD.csv
  teaching-vacancies-discovery-YYYY-MM-DD-summary.json
  teaching-vacancies-routed-YYYY-MM-DD.csv
  teaching-vacancies-unresolved-YYYY-MM-DD.csv
  teaching-vacancies-routing-YYYY-MM-DD-summary.json

pipeline/reviews/external/teaching-vacancies/
  <region-slug>-admin-service-review.csv
  <region-slug>-admin-service-summary.md
  west-yorkshire-migration.csv
```

A failed or unstable discovery run writes no authoritative replacement
manifest.

## Stage 2 — review each region

Open the regional Markdown summary, not the source-wide manifest, for the
actual vacancy decision.

Edit only the `action:` line:

- an `HC` vacancy is selected automatically unless set to `action: exclude`;
- a `POSS` vacancy remains unpublished while `action:` is blank;
- `action: select` promotes a `POSS` vacancy;
- `action: exclude` rejects a `POSS` vacancy or removes an automated selection;
- a `HARD_PASS` cannot be promoted through the review file.

The review shows the region's slice status. Actions in a `CANDIDATE` or
`UNREGISTERED` region are review evidence only and still cannot publish.

After editing and committing the Markdown file, rerun **Run Teaching Vacancies
regional review** on the same London calendar date. The rerun copies only
same-day actions whose stable ID and factual fingerprint still match into the
CSV and regenerated Markdown. If the vacancy changed, it returns for review
rather than inheriting an old decision.

## West Yorkshire migration

The first regional run compares the completed West Yorkshire process with the
new source-wide process.

An existing West Yorkshire action is migrated only when:

- the stable source ID matches;
- title, employer, location, salary/pay scale, closing date, classification
  reason and canonical URL all match; and
- an old `select` action is also present in the old approved snapshot.

Blank old `POSS` decisions remain blank. Changed or missing jobs are reported
as requiring review or no longer current. The legacy West Yorkshire review,
approved snapshot, compositor and workflows remain in the repository for
rollback.

## Stage 3 — approve one LIVE region

After the regional CSV and Markdown agree, run:

**Build approved Teaching Vacancies regional snapshot**

Enter:

- `region`: the exact Ontap region name from the slice register;
- `approval`: `PUBLISH` exactly.

The workflow blocks unless:

- the requested `admin_service` slice is explicitly `LIVE`;
- the review is dated today in London;
- the CSV and Markdown vacancy sets, actions and fingerprints agree;
- every selected vacancy has the required factual fields and a valid deadline;
- no selected vacancy is a confirmed JobG8 duplicate;
- any migrated record marked `REVIEW_REQUIRED` has an explicit new decision;
- the approved snapshot and evidence hashes reconcile; and
- exactly one current regional output contains non-Teaching-Vacancies base
  rows for that region.

It creates only the requested region's files:

```text
pipeline/output-external/teaching-vacancies-regional/
  <region-slug>-admin-service.json

pipeline/manifests/external/teaching-vacancies/approved/
  <region-slug>-admin-service-evidence.json
```

It then invokes the generic composer with `--region` so another region cannot
be recomposed during the approval run.

## Stage 4 — composition rules

`compose_teaching_vacancies_regional.py` is source-specific but
region-neutral. It identifies the region from the current output rows rather
than from a hard-coded regional filename table.

For each eligible region it:

- verifies the approved snapshot against its evidence hash and job-ID list;
- checks the current slice register again;
- removes only the previous `source: Teaching Vacancies` subset;
- preserves JobG8, NEJobs, VONNE and any other source rows;
- removes expired Teaching Vacancies jobs;
- deduplicates against current base jobs by job ID and factual fingerprint; and
- writes only a non-empty combined output containing at least one non-Teaching-
  Vacancies base row.

The two daily admin workflows run compositors in this order:

1. `compose_northeast_admin`;
2. legacy `compose_west_yorkshire_admin`;
3. generic `compose_teaching_vacancies_regional`.

This order is deliberate. The first two preserve established behavior; the
last step takes over a region only when a separately approved, verified
regional snapshot exists. Without one, it leaves that region unchanged.

## Stage 5 — publication

Approval and composition do not modify `app/`.

After checking the combined regional count, use the existing verified
publisher for that live slice. The publisher still:

- reads `LIVE` status from the slice register;
- refuses malformed or duplicate output;
- leaves the current live page unchanged when the selected source output is
  empty; and
- verifies the destination after writing.

Teaching Vacancies therefore does not create a second publishing route.

## Daily retention and expiry behavior

A daily JobG8 run regenerates the regional base output, reattaches established
North East and legacy West external sources, then reattaches every verified
Teaching Vacancies regional snapshot for a `LIVE` slice.

The latest approved snapshot remains authoritative until replaced. On every
composition run:

- expired vacancies are omitted;
- duplicates against the new JobG8/base set are omitted;
- open approved vacancies are retained; and
- a missing regional snapshot does not overwrite the current combined output.

An approved empty snapshot is valid when the reviewed region has no selected
open Teaching Vacancies jobs. It removes the previous Teaching Vacancies subset
while preserving the base output.

## Moving a region from CANDIDATE to LIVE

Do not change status merely because jobs have been discovered.

Before promotion, confirm:

1. geography is resolving cleanly in `geo_lookup.xlsx`;
2. the regional review is producing credible admin/service candidates;
3. the JobG8/other base pipeline creates a current non-empty regional output;
4. the relevant verified publisher mapping/page exists; and
5. the region name used by the lookup, slice register, output rows and page
   mapping is identical.

Then change the existing slice-register row from `CANDIDATE` to `LIVE`, rerun
the register and Teaching Vacancies tests, generate a fresh regional review,
and use the one-region approval workflow.

## Failure behavior

| Failure | Required behavior |
| --- | --- |
| Listing totals, pagination or two sweeps disagree | Stop; do not replace discovery evidence |
| Any discovered detail page fails | Stop; do not write authoritative manifest |
| Geography has no exact approved match | Write to unresolved CSV; never publish |
| Slice is missing, CANDIDATE or UNREGISTERED | Reviewable but approval/composition blocked |
| Review date, set or fingerprint is stale | Approval blocked |
| Selected vacancy is expired, incomplete or a JobG8 duplicate | Approval blocked |
| Snapshot or evidence hash differs | Composition blocked |
| Current regional output is empty | Leave it unchanged |
| Current output contains only Teaching Vacancies | Block external-only overwrite |
| No approved regional snapshot exists | Retain current output unchanged |
| Publisher source output is empty | Retain current live page unchanged |

## Rollback

The branch and PR must remain the first rollback boundary until review is
complete. Nothing in this architecture should be introduced directly on
`main`.

After merge, an operational rollback is:

1. remove or revert the generic composer line from the two daily workflows;
2. rerun the service-admin pipeline;
3. allow the existing North East compositor to restore NEJobs/VONNE;
4. allow the legacy West Yorkshire compositor to restore the old approved West
   Yorkshire Teaching Vacancies snapshot; and
5. run the verified publisher only after checking the rebuilt counts.

For other regions, regenerating the base output with the generic composer
disabled removes the regional Teaching Vacancies subset. No `app/` rollback is
needed unless the verified publisher had already been run; in that case publish
the rebuilt verified base output through the normal publisher.

## Maintenance checklist

Before changing discovery, geography, status or composition:

- preserve the source-wide, no-region discovery contract;
- preserve query/page provenance and two-sweep evidence;
- update `geo_lookup.xlsx` rather than adding code-level place exceptions;
- update the existing slice register rather than creating another registry;
- keep unresolved geography visible;
- keep regional JobG8 comparison scoped to the same region;
- retain stable source IDs and factual fingerprints;
- keep blank `POSS` decisions unpublished;
- keep approval one region at a time;
- keep the legacy West and North East compositors until rollback is no longer
  required; and
- run the complete Teaching Vacancies and slice-register CI suites before
  merging.

## Developer command sequence

The GitHub workflows are the normal operator route. For controlled development,
run from `pipeline/` with a single London review date:

```bash
python -m external_sources.teaching_vacancies_discovery --fetch-live

python -m external_sources.teaching_vacancies_routing \
  --manifest-csv manifests/external/teaching-vacancies/teaching-vacancies-discovery-YYYY-MM-DD.csv \
  --discovery-summary-json manifests/external/teaching-vacancies/teaching-vacancies-discovery-YYYY-MM-DD-summary.json \
  --write-routing

python -m external_sources.teaching_vacancies_regional_review \
  --routed-csv manifests/external/teaching-vacancies/teaching-vacancies-routed-YYYY-MM-DD.csv \
  --routing-summary-json manifests/external/teaching-vacancies/teaching-vacancies-routing-YYYY-MM-DD-summary.json \
  --write-reviews

python -m external_sources.teaching_vacancies_regional_approved \
  --review-csv reviews/external/teaching-vacancies/<region-slug>-admin-service-review.csv \
  --summary-md reviews/external/teaching-vacancies/<region-slug>-admin-service-summary.md \
  --write-approved-json \
  --confirm-approved PUBLISH

python -m external_sources.compose_teaching_vacancies_regional \
  --region "Exact Ontap Region" \
  --write
```

Do not use the local commands to bypass the review, approval, commit-scope or
verified-publisher gates.

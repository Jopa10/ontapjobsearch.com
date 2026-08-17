# External review decision ledgers

NEJobs and VONNE review workflows create small CSV ledgers here after the first run. Each explicit `select` or `exclude` decision is stored against the source job ID and a fingerprint of the reviewed vacancy facts. A later refresh reuses the decision only when those facts are unchanged; changed vacancies return to review.

These ledgers do not publish jobs or bypass the existing same-day review and explicit `PUBLISH` approval gates.

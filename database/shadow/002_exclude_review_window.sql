-- Apply only to the verified ontap-db-test database after owner approval.
-- This records the start of the three-day review window for full payloads that
-- are excluded in every production family. It does not delete any data.
ALTER TABLE ontap_shadow.supplier_adverts
    ADD COLUMN IF NOT EXISTS exclude_review_started_on date;

CREATE INDEX IF NOT EXISTS supplier_adverts_exclude_review
    ON ontap_shadow.supplier_adverts(exclude_review_started_on)
    WHERE raw_payload IS NOT NULL;

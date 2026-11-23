-- Apply as the Neon Production owner before selecting Neon as the deployment source.
-- The restricted daily writer role receives only the permissions needed to replace
-- and read back the current publisher snapshot. Older daily snapshots are pruned on update.
BEGIN;

CREATE TABLE IF NOT EXISTS ontap_shadow.publisher_snapshots (
  feed_date date PRIMARY KEY,
  production_run_id bigint NOT NULL,
  row_count integer NOT NULL CHECK (row_count >= 0),
  uncompressed_sha256 text NOT NULL CHECK (uncompressed_sha256 ~ '^[a-f0-9]{64}$'),
  compressed_payload bytea NOT NULL
);

GRANT SELECT, INSERT, UPDATE
ON TABLE ontap_shadow.publisher_snapshots
TO ontap_prod_daily_writer;

COMMIT;

-- Preview-only archive/version metadata. No existing payloads are removed.
CREATE TABLE IF NOT EXISTS ontap_shadow.advert_payload_versions (
 advert_id uuid NOT NULL,
 job_id uuid NOT NULL,
 content_hash text NOT NULL,
 payload_sha256 text NOT NULL,
 archive_receipt jsonb,
 archived_at timestamptz,
 PRIMARY KEY(advert_id,content_hash),
 FOREIGN KEY(advert_id,job_id) REFERENCES ontap_shadow.supplier_adverts(id,job_id)
);
ALTER TABLE ontap_shadow.activity_events ADD COLUMN IF NOT EXISTS advert_content_hash text;
DO $$ BEGIN
 IF NOT EXISTS(SELECT 1 FROM pg_constraint WHERE conname='activity_events_advert_version' AND conrelid='ontap_shadow.activity_events'::regclass) THEN
  ALTER TABLE ontap_shadow.activity_events ADD CONSTRAINT activity_events_advert_version FOREIGN KEY(advert_id,advert_content_hash) REFERENCES ontap_shadow.advert_payload_versions(advert_id,content_hash);
 END IF;
END $$;

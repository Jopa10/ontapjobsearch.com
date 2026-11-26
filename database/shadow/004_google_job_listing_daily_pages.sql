BEGIN;

CREATE TABLE IF NOT EXISTS ontap_shadow.google_job_listing_daily_totals (
  report_date date PRIMARY KEY,
  clicks bigint NOT NULL CHECK (clicks >= 0),
  impressions bigint NOT NULL CHECK (impressions >= 0),
  page_count integer NOT NULL CHECK (page_count >= 0),
  page_clicks_sum bigint NOT NULL CHECK (page_clicks_sum >= 0),
  page_impressions_sum bigint NOT NULL CHECK (page_impressions_sum >= 0),
  pages_reconcile boolean NOT NULL,
  fetched_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ontap_shadow.google_job_listing_daily_pages (
  report_date date NOT NULL,
  page_url text NOT NULL,
  clicks bigint NOT NULL CHECK (clicks >= 0),
  impressions bigint NOT NULL CHECK (impressions >= 0),
  ctr double precision,
  average_position double precision,
  fetched_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (report_date, page_url)
);

GRANT SELECT, INSERT, UPDATE, DELETE
  ON ontap_shadow.google_job_listing_daily_totals
  TO ontap_prod_daily_writer;
GRANT SELECT, INSERT, UPDATE, DELETE
  ON ontap_shadow.google_job_listing_daily_pages
  TO ontap_prod_daily_writer;

COMMIT;

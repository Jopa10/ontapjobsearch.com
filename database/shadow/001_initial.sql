-- Draft migration: apply only to an explicitly verified Neon TEST database.
-- Intentionally separate from the legacy public Prisma schema and production.
DO $$
BEGIN
CREATE SCHEMA ontap_shadow;
SET LOCAL search_path TO ontap_shadow, public;

CREATE TABLE suppliers (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code text NOT NULL UNIQUE,
    name text NOT NULL,
    active boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE jobs (
    id uuid PRIMARY KEY,
    public_id text NOT NULL UNIQUE,
    title text NOT NULL,
    employer text,
    location text,
    region text,
    role_family text,
    sector text NOT NULL DEFAULT 'unknown' CHECK (sector IN ('public', 'private', 'charity', 'unknown')),
    role_level text NOT NULL DEFAULT 'unknown' CHECK (role_level IN ('core', 'step_up', 'unknown')),
    classification_evidence jsonb NOT NULL DEFAULT '{}',
    salary_min numeric,
    salary_max numeric,
    salary_period text,
    salary_text text,
    first_seen date NOT NULL,
    last_seen date NOT NULL,
    inactive_since date,
    publication_status text NOT NULL DEFAULT 'unassessed'
        CHECK (publication_status IN ('unassessed', 'withheld', 'published', 'expired')),
    preferred_advert_id uuid,
    CHECK (last_seen >= first_seen),
    CHECK (inactive_since IS NULL OR inactive_since >= last_seen)
);

CREATE TABLE supplier_adverts (
    id uuid PRIMARY KEY,
    supplier_id bigint NOT NULL REFERENCES suppliers(id),
    supplier_job_id text NOT NULL,
    job_id uuid NOT NULL REFERENCES jobs(id),
    title text NOT NULL,
    advertiser_name text,
    location text,
    apply_url text NOT NULL,
    raw_payload jsonb,
    content_hash text NOT NULL,
    first_seen date NOT NULL,
    last_seen date NOT NULL,
    inactive_since date,
    supplier_expires_at timestamptz,
    availability text NOT NULL DEFAULT 'seen' CHECK (availability IN ('seen', 'missing', 'expired')),
    match_method text NOT NULL DEFAULT 'supplier_identity',
    match_evidence jsonb NOT NULL DEFAULT '{}',
    content_purged_at timestamptz,
    UNIQUE (supplier_id, supplier_job_id),
    UNIQUE (id, job_id),
    UNIQUE (id, supplier_id),
    CHECK (last_seen >= first_seen),
    CHECK (inactive_since IS NULL OR inactive_since >= last_seen)
);
ALTER TABLE jobs ADD CONSTRAINT preferred_advert_belongs_to_job
    FOREIGN KEY (preferred_advert_id, id) REFERENCES supplier_adverts(id, job_id)
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX supplier_adverts_job ON supplier_adverts(job_id);
CREATE INDEX supplier_adverts_retention ON supplier_adverts(inactive_since) WHERE raw_payload IS NOT NULL;

CREATE TABLE feed_runs (
    id uuid PRIMARY KEY,
    supplier_id bigint NOT NULL REFERENCES suppliers(id),
    feed_key text NOT NULL,
    feed_date date NOT NULL,
    source_checksum text NOT NULL,
    status text NOT NULL CHECK (status IN ('staged', 'accepted', 'rejected', 'failed')),
    started_at timestamptz NOT NULL DEFAULT now(),
    completed_at timestamptz,
    received_count integer NOT NULL CHECK (received_count >= 0),
    published_count integer CHECK (published_count >= 0),
    rules_revision text,
    diagnostics jsonb NOT NULL DEFAULT '{}',
    UNIQUE (supplier_id, feed_key),
    UNIQUE (id, supplier_id),
    CHECK (status <> 'accepted' OR completed_at IS NOT NULL)
);

CREATE TABLE advert_appearances (
    advert_id uuid NOT NULL,
    seen_on date NOT NULL,
    supplier_id bigint NOT NULL,
    feed_run_id uuid NOT NULL,
    PRIMARY KEY (advert_id, seen_on),
    FOREIGN KEY (advert_id, supplier_id) REFERENCES supplier_adverts(id, supplier_id),
    FOREIGN KEY (feed_run_id, supplier_id) REFERENCES feed_runs(id, supplier_id)
);
CREATE INDEX advert_appearances_run ON advert_appearances(feed_run_id);

CREATE TABLE selection_decisions (
    id uuid PRIMARY KEY,
    advert_id uuid NOT NULL REFERENCES supplier_adverts(id),
    feed_run_id uuid NOT NULL REFERENCES feed_runs(id),
    scope text NOT NULL,
    decision text NOT NULL CHECK (decision IN ('include', 'review', 'exclude', 'unknown')),
    reason text NOT NULL,
    rules_revision text NOT NULL,
    evidence jsonb NOT NULL DEFAULT '{}',
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (advert_id, feed_run_id, scope)
);

CREATE TABLE subscribers (
    id uuid PRIMARY KEY,
    email text NOT NULL,
    email_key text NOT NULL UNIQUE,
    brevo_contact_id text UNIQUE,
    status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'unsubscribed', 'suppressed')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE subscriber_preferences (
    id uuid PRIMARY KEY,
    subscriber_id uuid NOT NULL REFERENCES subscribers(id),
    preference_key text NOT NULL,
    criteria jsonb NOT NULL,
    signup_job_id uuid REFERENCES jobs(id),
    active boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (subscriber_id, preference_key),
    UNIQUE (id, subscriber_id)
);

CREATE TABLE consent_history (
    id uuid PRIMARY KEY,
    subscriber_id uuid NOT NULL REFERENCES subscribers(id),
    purpose text NOT NULL,
    action text NOT NULL CHECK (action IN ('granted', 'withdrawn')),
    wording_version text NOT NULL,
    wording_text text NOT NULL,
    source text NOT NULL,
    occurred_at timestamptz NOT NULL,
    evidence jsonb NOT NULL DEFAULT '{}'
);
CREATE INDEX consent_history_subscriber ON consent_history(subscriber_id, purpose, occurred_at DESC);

CREATE TABLE emails_sent (
    id uuid PRIMARY KEY,
    subscriber_id uuid NOT NULL REFERENCES subscribers(id),
    idempotency_key text NOT NULL UNIQUE,
    provider_message_id text UNIQUE,
    status text NOT NULL CHECK (status IN ('queued', 'sending', 'sent', 'failed', 'uncertain')),
    queued_at timestamptz NOT NULL DEFAULT now(),
    sent_at timestamptz,
    error_code text,
    UNIQUE (id, subscriber_id),
    CHECK (status <> 'sent' OR (sent_at IS NOT NULL AND provider_message_id IS NOT NULL))
);

CREATE TABLE job_recommendations (
    id uuid PRIMARY KEY,
    email_id uuid NOT NULL,
    subscriber_id uuid NOT NULL,
    preference_id uuid,
    signup_job_id uuid REFERENCES jobs(id),
    recommended_job_id uuid NOT NULL REFERENCES jobs(id),
    outbound_advert_id uuid,
    reason text NOT NULL,
    matcher_revision text NOT NULL,
    matching_evidence jsonb NOT NULL DEFAULT '{}',
    signup_sector text,
    recommended_sector text,
    created_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (email_id, subscriber_id) REFERENCES emails_sent(id, subscriber_id),
    FOREIGN KEY (preference_id, subscriber_id) REFERENCES subscriber_preferences(id, subscriber_id),
    FOREIGN KEY (outbound_advert_id, recommended_job_id) REFERENCES supplier_adverts(id, job_id),
    UNIQUE (email_id, recommended_job_id)
);

CREATE TABLE activity_events (
    id uuid PRIMARY KEY,
    event_type text NOT NULL CHECK (event_type IN ('email_job_click', 'apply_click', 'unsubscribe', 'application_confirmed')),
    occurred_at timestamptz NOT NULL,
    subscriber_id uuid REFERENCES subscribers(id),
    recommendation_id uuid REFERENCES job_recommendations(id),
    job_id uuid REFERENCES jobs(id),
    advert_id uuid,
    source_page text,
    referrer_category text,
    automated boolean,
    provider_event_id text UNIQUE,
    conversion_evidence jsonb,
    CHECK (advert_id IS NULL OR job_id IS NOT NULL),
    FOREIGN KEY (advert_id, job_id) REFERENCES supplier_adverts(id, job_id),
    CHECK (event_type <> 'application_confirmed' OR
        (conversion_evidence IS NOT NULL AND conversion_evidence <> '{}'::jsonb))
);
CREATE INDEX activity_events_job ON activity_events(job_id, occurred_at);
CREATE INDEX activity_events_recommendation ON activity_events(recommendation_id, occurred_at);
CREATE INDEX jobs_publication ON jobs(publication_status, region, role_family);
END;
$$;

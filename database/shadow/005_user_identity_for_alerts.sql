-- Add canonical user and address identities to the Preview-only Ontap shadow schema.
-- Prerequisite: 001_initial.sql through 004_master_cleanup_versions.sql have been
-- applied to the isolated Neon test database. Run this migration once, in a transaction.
BEGIN;
SET LOCAL search_path TO ontap_shadow, public;

CREATE TABLE users (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE user_emails (
  id uuid PRIMARY KEY,
  user_id uuid NOT NULL REFERENCES users(id),
  email text NOT NULL,
  email_key text NOT NULL UNIQUE,
  alert_status text NOT NULL DEFAULT 'pending'
    CHECK (alert_status IN ('pending', 'active', 'unsubscribed', 'suppressed')),
  verified_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (id, user_id)
);

-- Preserve every existing subscriber UUID as its permanent user_id.
INSERT INTO users (id, created_at)
SELECT id, created_at FROM subscribers ON CONFLICT (id) DO NOTHING;
INSERT INTO user_emails (id, user_id, email, email_key, alert_status, created_at, updated_at)
SELECT id, id, email, email_key, status, created_at, updated_at FROM subscribers
ON CONFLICT (email_key) DO NOTHING;

ALTER TABLE subscribers ADD COLUMN user_id uuid;
ALTER TABLE subscribers ADD COLUMN user_email_id uuid;
UPDATE subscribers SET user_id = id, user_email_id = id;
ALTER TABLE subscribers ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE subscribers ALTER COLUMN user_email_id SET NOT NULL;
ALTER TABLE subscribers ADD CONSTRAINT subscribers_user_fk FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE subscribers ADD CONSTRAINT subscribers_user_email_fk
  FOREIGN KEY (user_email_id, user_id) REFERENCES user_emails(id, user_id);
CREATE INDEX subscribers_user ON subscribers(user_id);

ALTER TABLE subscriber_preferences ADD COLUMN user_id uuid;
ALTER TABLE subscriber_preferences ADD COLUMN signup_job_public_id text;
UPDATE subscriber_preferences p SET user_id = s.user_id FROM subscribers s WHERE s.id = p.subscriber_id;
ALTER TABLE subscriber_preferences ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE subscriber_preferences ADD CONSTRAINT subscriber_preferences_user_fk FOREIGN KEY (user_id) REFERENCES users(id);
CREATE INDEX subscriber_preferences_user ON subscriber_preferences(user_id, active);

ALTER TABLE consent_history ADD COLUMN user_email_id uuid;
ALTER TABLE consent_history ADD COLUMN idempotency_key text UNIQUE;
UPDATE consent_history c SET user_email_id = s.user_email_id FROM subscribers s WHERE s.id = c.subscriber_id;
ALTER TABLE consent_history ALTER COLUMN user_email_id SET NOT NULL;
ALTER TABLE consent_history ADD CONSTRAINT consent_history_user_email_fk FOREIGN KEY (user_email_id) REFERENCES user_emails(id);
CREATE INDEX consent_history_email ON consent_history(user_email_id, purpose, occurred_at DESC);

ALTER TABLE emails_sent ADD COLUMN user_id uuid;
ALTER TABLE emails_sent ADD COLUMN user_email_id uuid;
UPDATE emails_sent e SET user_id = s.user_id, user_email_id = s.user_email_id FROM subscribers s WHERE s.id = e.subscriber_id;
ALTER TABLE emails_sent ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE emails_sent ALTER COLUMN user_email_id SET NOT NULL;
ALTER TABLE emails_sent ADD CONSTRAINT emails_sent_user_fk FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE emails_sent ADD CONSTRAINT emails_sent_user_email_fk FOREIGN KEY (user_email_id) REFERENCES user_emails(id);

ALTER TABLE job_recommendations ADD COLUMN user_id uuid;
ALTER TABLE job_recommendations ADD COLUMN user_email_id uuid;
UPDATE job_recommendations r SET user_id = s.user_id, user_email_id = s.user_email_id FROM subscribers s WHERE s.id = r.subscriber_id;
ALTER TABLE job_recommendations ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE job_recommendations ALTER COLUMN user_email_id SET NOT NULL;
ALTER TABLE job_recommendations ADD CONSTRAINT recommendations_user_fk FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE job_recommendations ADD CONSTRAINT recommendations_user_email_fk FOREIGN KEY (user_email_id) REFERENCES user_emails(id);

ALTER TABLE activity_events ADD COLUMN user_id uuid;
ALTER TABLE activity_events ADD COLUMN user_email_id uuid;
UPDATE activity_events e SET user_id = s.user_id, user_email_id = s.user_email_id FROM subscribers s WHERE s.id = e.subscriber_id;
ALTER TABLE activity_events ADD CONSTRAINT activity_events_user_fk FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE activity_events ADD CONSTRAINT activity_events_user_email_fk FOREIGN KEY (user_email_id) REFERENCES user_emails(id);
CREATE INDEX activity_events_user ON activity_events(user_id, occurred_at);
COMMIT;

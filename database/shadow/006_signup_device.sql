-- Record a coarse device category for each alert signup/consent event.
-- Apply after 005_user_identity_for_alerts.sql in the isolated Preview database.
BEGIN;
ALTER TABLE ontap_shadow.consent_history
  ADD COLUMN signup_device text NOT NULL DEFAULT 'unknown'
  CHECK (signup_device IN ('mobile', 'laptop', 'unknown'));
COMMIT;

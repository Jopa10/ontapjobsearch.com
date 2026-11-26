# Private alert signup Preview test

Status: private test only on `feat/cpc-alert-neon-signup`; not merged or live. Public delivery remains off.

## Before the owner submits the form

1. Use the separate Free Neon project `ontap-email-preview` in London; its project ID is `withered-bread-65990253`.
2. The Preview project has the base schema plus `004_master_cleanup_versions.sql`, `005_user_identity_for_alerts.sql` and `006_signup_device.sql` applied. Do not run them again.
3. Set `ONTAP_EMAIL_PREVIEW_DATABASE_URL` and `ONTAP_EMAIL_PREVIEW_NEON_PROJECT_ID` only for the `feat/cpc-alert-neon-signup` Vercel Preview deployment.
4. Add the same project's restricted writer URL as `ONTAP_EMAIL_PREVIEW_DATABASE_URL` in the `ontap-brevo-private-test` GitHub environment. Do not replace the shared `ONTAP_SHADOW_DATABASE_URL` secret.
5. Verify `jpbt801@gmail.com` is still unsubscribed in Brevo before the owner chooses to submit the new form. The earlier unsubscribe test is already complete; do not repeat it.

## Signup test

On the Preview site, open an eligible JobG8 vacancy, submit the new alert form using `jpbt801@gmail.com`, and tick the explicit consent box. The email is allowed only for the Preview signup path; it is not added to the daily sender's recipient allowlist.

The API first saves the user, email address, preferences, clicked vacancy's public ID and exact consent wording/version/timestamp in Neon. It then asks Brevo to enable delivery and send the confirmation; Brevo does not receive the preference criteria or consent record. The Neon address becomes active only after Brevo confirms active list delivery. GitHub later reads active, consented preferences from Neon and applies the existing matcher. Brevo supplies suppression status and keeps the existing daily-send marker.

## GitHub Preview read

GitHub Actions needs the Preview-only Neon connection URL as the `ONTAP_EMAIL_PREVIEW_DATABASE_URL` secret in the `ontap-brevo-private-test` GitHub environment. Do not add a Production URL. The Vercel supplies the separate Preview connection to the deployed signup route, but its managed secret is not exported to GitHub Actions.

## Neon readback

After the form reports success, run this query in the Preview database to inspect the linked records:

```sql
SELECT u.id AS user_id, ue.id AS user_email_id, ue.email, ue.alert_status,
       s.id AS subscriber_id, s.status AS subscriber_status,
       p.id AS preference_id, p.criteria, p.signup_job_public_id,
       c.id AS consent_id, c.action, c.wording_version, c.wording_text,
       c.source, c.occurred_at, c.idempotency_key, c.signup_device
FROM ontap_shadow.users u
JOIN ontap_shadow.user_emails ue ON ue.user_id = u.id
JOIN ontap_shadow.subscribers s ON s.user_id = u.id AND s.user_email_id = ue.id
JOIN ontap_shadow.subscriber_preferences p ON p.user_id = u.id AND p.subscriber_id = s.id
JOIN ontap_shadow.consent_history c ON c.subscriber_id = s.id AND c.user_email_id = ue.id
WHERE ue.email_key = lower(trim('jpbt801@gmail.com'))
ORDER BY c.occurred_at DESC
LIMIT 10;
```

Expected: one canonical user, one associated address, the submitted role/location criteria, the clicked job's public ID, active delivery state, and a grant record with the exact displayed consent wording, timestamp, and detected signup device. Repeating the same request must not create another preference or send a duplicate confirmation; the unique signup-attempt key prevents a duplicate consent row for that request.

## Isolation checks

- Production database, production signup and public delivery remain untouched.
- The daily email sender still includes only its existing approved recipient; jnabon stays excluded.
- Do not merge or enable public delivery as part of this private Preview test.

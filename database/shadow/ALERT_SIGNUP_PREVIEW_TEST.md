# Private alert signup Preview test

Status: code prepared on `feat/cpc-alert-neon-signup`; not merged or live. Do not enable public delivery for this test.

## Before the owner submits the form

1. Confirm PR #336's Preview schema migrations `001_initial.sql` through `004_master_cleanup_versions.sql` are already applied to the isolated Neon test database.
2. Run `database/shadow/005_user_identity_for_alerts.sql` once in that same Neon database. It adds stable user IDs, separate email-address IDs, direct user links on preferences and delivery history, and address-linked consent records. It preserves any existing subscriber IDs.
3. Run `database/shadow/006_signup_device.sql` once in the same Neon database. It adds a coarse signup-device category (`mobile`, `laptop`/desktop browser, or `unknown`).
4. Confirm the Vercel Preview branch is `feat/cpc-alert-neon-signup` and has the Preview-only `ONTAP_SHADOW_DATABASE_URL`, Brevo, sender and unsubscribe settings. Do not use `DATABASE_URL` or production variables.
4. Verify `jnabon1108@gmail.com` is still unsubscribed in Brevo before the owner chooses to submit the new form. The earlier unsubscribe test is already complete; do not repeat it.

## Signup test

On the Preview site, open an eligible JobG8 vacancy, submit the new alert form using `jnabon1108@gmail.com`, and tick the explicit consent box. The email is allowed only for the Preview signup path; it is not added to the daily sender's recipient allowlist.

The API saves/updates the Brevo contact, then stores the user, email address, preferences, clicked vacancy's public ID and exact consent wording/version/timestamp in Neon. It marks the Neon address active only after the provider confirms the subscription. The form reports success only after both steps complete.

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
WHERE ue.email_key = lower(trim('jnabon1108@gmail.com'))
ORDER BY c.occurred_at DESC
LIMIT 10;
```

Expected: one canonical user, one associated address, the submitted role/location criteria, the clicked job's public ID, active delivery state, and a grant record with the exact displayed consent wording, timestamp, and detected signup device. A repeat network submission with the same signup attempt must not create a second consent row or preference.

## Isolation checks

- Production database, production signup and public delivery remain untouched.
- The daily email sender still includes only its existing approved recipient; jnabon stays excluded.
- Do not merge or enable public delivery as part of this private Preview test.

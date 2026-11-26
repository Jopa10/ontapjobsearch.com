BEGIN;

CREATE TABLE IF NOT EXISTS ontap_shadow.private_email_send_windows (
    report_date date PRIMARY KEY,
    opened_at timestamptz NOT NULL DEFAULT now(),
    closed_at timestamptz,
    status text NOT NULL DEFAULT 'open'
        CHECK (status IN ('open', 'closed', 'sending', 'sent'))
);

CREATE TABLE IF NOT EXISTS ontap_shadow.private_email_manual_selections (
    report_date date NOT NULL
        REFERENCES ontap_shadow.private_email_send_windows(report_date) ON DELETE CASCADE,
    user_email_id uuid NOT NULL
        REFERENCES ontap_shadow.user_emails(id) ON DELETE CASCADE,
    public_job_id text NOT NULL,
    selected_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (report_date, user_email_id, public_job_id)
);

COMMIT;

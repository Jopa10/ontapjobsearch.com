-- CreateTable
CREATE TABLE "jobs" (
    "id" TEXT NOT NULL,
    "job_title" TEXT NOT NULL,
    "job_location" TEXT NOT NULL,
    "job_description" TEXT NOT NULL,
    "job_category" TEXT NOT NULL,
    "job_type" TEXT NOT NULL,
    "company_name" TEXT NOT NULL,
    "company_url" TEXT,
    "company_logo" TEXT,
    "job_application_url" TEXT NOT NULL,
    "other_details" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "jobs_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "admins" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "role" TEXT NOT NULL DEFAULT 'admin',
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "admins_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "applications" (
    "id" TEXT NOT NULL,
    "job_id" TEXT NOT NULL,
    "tracking_cookie" TEXT NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "applications_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "jobs_job_title_idx" ON "jobs"("job_title");

-- CreateIndex
CREATE INDEX "jobs_job_location_idx" ON "jobs"("job_location");

-- CreateIndex
CREATE INDEX "jobs_job_category_idx" ON "jobs"("job_category");

-- CreateIndex
CREATE INDEX "jobs_job_type_idx" ON "jobs"("job_type");

-- CreateIndex
CREATE INDEX "jobs_company_name_idx" ON "jobs"("company_name");

-- CreateIndex
CREATE INDEX "jobs_created_at_idx" ON "jobs"("created_at");

-- CreateIndex
CREATE UNIQUE INDEX "admins_email_key" ON "admins"("email");

-- CreateIndex
CREATE INDEX "applications_job_id_idx" ON "applications"("job_id");

-- CreateIndex
CREATE INDEX "applications_tracking_cookie_idx" ON "applications"("tracking_cookie");

-- CreateIndex
CREATE INDEX "applications_timestamp_idx" ON "applications"("timestamp");

-- AddForeignKey
ALTER TABLE "applications" ADD CONSTRAINT "applications_job_id_fkey" FOREIGN KEY ("job_id") REFERENCES "jobs"("id") ON DELETE CASCADE ON UPDATE CASCADE;

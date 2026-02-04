# Ontap Job Search Platform

A modern job matching platform built with Next.js, PostgreSQL, and Prisma. Features a comprehensive admin interface for job management and a public-facing job search portal.

## Features

- ✨ **Modern UI** - Clean, responsive design with Tailwind CSS
- 🔐 **Secure Admin Portal** - NextAuth.js authentication with session management
- 📊 **Job Management** - Full CRUD operations for job listings
- 📤 **Bulk Import** - CSV/JSON file upload for batch job creation
- 🔍 **Advanced Search** - Filter jobs by title, location, category, and type
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile
- 🎯 **Application Tracking** - Track user engagement with job listings
- 🚀 **Production Ready** - Docker support with PM2 process management

## Tech Stack

**Frontend:** Next.js 14+, React 19, TypeScript, Tailwind CSS, NextAuth.js

**Backend:** Next.js API Routes, PostgreSQL, Prisma ORM, bcrypt

**Deployment:** Docker, PM2, Vercel-ready

## Quick Start

### Prerequisites

- Node.js 20+ and npm
- PostgreSQL (or use Docker Compose)

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your database connection:
   ``env
   DATABASE_URL="postgresql://ontap_user:ontap_password@localhost:5432/ontap_db"
   NEXTAUTH_SECRET="your-secret-key-min-32-chars"
   ADMIN_PASSWORD="admin123"
   ADMIN_EMAIL="admin@ontap.com"
   ```

3. **Start PostgreSQL with Docker:**
   ```bash
   docker-compose up -d postgres
   ```

4. **Run database migrations and seed:**
   ```bash
   npm run db:migrate
   npm run db:seed
   ```

5. **Start the development server:**
   ```bash
   npm run dev
   ```

6. **Access the application:**
   - **Public site:** http://localhost:3000
   - **Admin login:** http://localhost:3000/admin/login
   - **Default credentials:** Configured in `.env` (default: `admin@ontap.com`)

## Docker Deployment

```bash
# Start everything (database + app)
docker-compose up --build

# Database only (for development)
docker-compose up -d postgres
```

## Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run db:migrate   # Run database migrations
npm run db:seed      # Seed database with default admin
```

## Default Admin Account

After seeding:
- **Email:** Defined in `ADMIN_EMAIL`
- **Password:** Defined in `ADMIN_PASSWORD`

⚠️ **Change these credentials in production!**

## Importing Test Data

1. Navigate to admin panel: http://localhost:3000/admin/jobs
2. Click "Upload CSV/JSON"
3. Select `testdata/csv/jobs.csv` or `testdata/json/jobs.json`
4. Click "Upload Jobs"

## API Endpoints

### Public
- `GET /api/jobs` - List/search jobs
- `GET /api/jobs/[id]` - Get single job
- `GET /api/jobs/similar/[id]` - Get similar jobs
- `POST /api/track` - Track application
- `GET /api/health` - Health check

### Admin (Authenticated)
- `POST /api/jobs` - Create job
- `PUT /api/jobs/[id]` - Update job
- `DELETE /api/jobs/[id]` - Delete job
- `POST /api/jobs/upload` - Bulk upload
- `GET /api/admin/users` - List admins
- `POST /api/admin/users` - Create admin

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection (required) |
| `NEXTAUTH_SECRET` | Auth secret min 32 chars (required) |
| `NEXTAUTH_URL` | App URL (default: http://localhost:3000) |
| `ADMIN_PASSWORD` | Password for default admin user (required for seeding) |
| `ADMIN_EMAIL` | Email for default admin user (default: admin@ontap.com) |

## Troubleshooting

**Database Connection Issues:**
```bash
# Ensure PostgreSQL is running
docker-compose ps

# Check logs
docker-compose logs postgres
```

**Prisma Issues:**
```bash
# Regenerate Prisma Client
npx prisma generate

# Reset database (⚠️ destroys data)
npx prisma migrate reset
Initial Vercel deploy
```

## License

Copyright © 2026 Ontap Job Search. All rights reserved.

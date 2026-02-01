Ontap – Stage 1 Build (Initial Scope)

Purpose of Stage 1
 Prove relevance and unit economics, not platform completeness
 Validate specific geo × role job slices with real users
 Keep cost, scope, and risk deliberately low
 Generate data to justify further build-out or stop early

Stage 1 Traffic Assumption
 Traffic will come from organic LinkedIn referrals only (posts, shares, profile links)
 Pages are designed for referred users, not search traffic
 SEO, automated feeds, and platform automation are intentionally out of scope
 This constraint is deliberate, not a missing feature

Stage 1 – Technical Scope
 Static job landing page template (Next.js or similar)
 Page content rendered from a simple CSV or JSON file
 Manual curation of jobs at this stage
 Page to include:
o H1 showing role and location
o Short context line explaining the job slice
o One primary (“hero”) job
o 8–15 highly similar jobs as backup options
o Clear outbound apply links
 Basic analytics only (page views and outbound clicks)
 Deployed and stable (Vercel is fine)

Explicit Non-Goals (Stage 1)
 No admin interface
 No automated feed ingestion
 No SEO optimisation or crawl strategy
 No dashboards beyond basic analytics

Why This Approach
 Organic LinkedIn traffic provides early signal without paid spend
 High-density job pages test relevance quickly
 Poor-performing slices are cheap to drop
 Successful slices justify automation later
 Code should remain clean and extensible
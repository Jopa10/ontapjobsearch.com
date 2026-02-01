Project Name: Ontap Job Search
 
Who are you? 

I am a senior software engineer with experience in building large-scale web applications. I am working on a new startup that is focused on providing a platform for job seekers to find jobs. The platform will be built using modern web technologies and will be deployed on a cloud platform.

What is the goal of this project?

The startup is currently in the early stages of development and is focused on building a minimum viable product (MVP) that can be used to test the market and validate the business model. The MVP will be built using a modern web development framework and will be deployed on a cloud platform.

Objective:

Build a minimum viable product (MVP) that can be used to test the market and validate the business model.


UX/UI Design:
1. Clean and modern design
2. Responsive design for mobile and desktop
3. Easy to navigate
4. Fast loading
5. Use the following icon for the app: /Users/pablo/Documents/ontap/docs/assets/ontap-icon.svg and /Users/pablo/Documents/ontap/docs/assets/ontap-icon.png
6. Use the following logos for the app: /Users/pablo/Documents/ontap/docs/assets/ontap-logo.png
7. Makse sure colors are consistent accross the app and the admin interface 

Technical Stack:
Backend:
1. Next.js
2. Postgres Database
3. Prisma ORM
4. Docker
5. PM2
6. Auth using NextAuth.js
7. TypeScript
8. ESLint
9. Prettier
10. nodejs
11. Use .env for environment variables
12. Use .env.example for environment variables example

Frontend:
1. ReactJS
2. Use react router for navigation
3. User react nextjs components for layout and navigation
4. Tailwind CSS
5. TypeScript
6. ESLint
7. Prettier
8. nodejs

Deployment:
1. Vercel
2. Docker
3. Make sure to copy all the needded assets to the docker container
4. create all the yaml files needed for the deployment
5. Make sure to use the correct environment variables for the deployment
6. Make sure to use the correct ports for the deployment
7. Make sure to use the correct domain for the deployment
8. Make sure to use the correct paths for the deployment
9. Make sure to use the correct paths for the admin interface
10. Make sure to use the correct paths for the public interface
11. Make sure to use the correct paths for the API
12. Make sure to use the correct paths for the assets
13. Make sure to use the correct paths for the database
14. Make sure to use the correct paths for the logs
15. Make sure to use the correct paths for the cache
16. Make sure to use the correct paths for the sessions
17. Make sure to use the correct paths for the static files
18. Make sure to use the correct paths for the uploaded files

Business Model:
1. Admin interface:
    1. DATA INGESTION:
        1. API Ingestion:
            1. ADD, UPDATE, DELETE job listing via API
        2. CSV Upload AND JSON Upload:
            1. CSV file should have the following columns: jobtitle, joblocation, jobdescription, jobcategory, jobtype, companyname, companyurl, companylogo, jobapplicationurl, otherdetails.
            2. JSON file should have the following structure: { "jobtitle": "Job Title", "joblocation": "Job Location", "jobdescription": "Job Description", "jobcategory": "Job Category", "jobtype": "Job Type", "companyname": "Company Name", "companyurl": "Company URL", "companylogo": "Company Logo", "jobapplicationurl": "Job Application URL", "otherdetails": "Other Details" }.
            3. CSV and JSON files should be uploaded via admin interface.
        3. Manual Entry:
            1. Manual entry should have the following fields: jobtitle, joblocation, jobdescription, jobcategory, jobtype, companyname, companyurl, companylogo, jobapplicationurl, otherdetails.
        Note: Manual Entry and CSV Upload will use API under the hood to add, update, delete job listing.

    2. AUTHENTICATION:
        1. Authentication required for admin interface only
        2. the domain should include /admin in the URL for the admin interface
        3. this is a private admin interface, no public access
        4. Authentication should be implemented using NextAuth.js
        5. Create a simple login page for the admin interface
        6. Create a simple password recovery page for the admin interface
        7. Login will be displayed in /admin/login and password recovery in /admin/recover
        8. No login or auth links in home page, if admins want to login, they should navigate to /admin/login
        9. Make sure to implement a logout functionality
        10. Make sure to implement a session timeout functionality
        11. Make sure to implement a session expiration functionality
        12. Make sure to implement a session refresh functionality
        13. Make sure that back button from browser after logout does not allow access to admin interface
        14. Make sure to implement a session storage functionality
        15. Make sure to implement a session storage expiration functionality
        16. Make sure to implement a session storage refresh functionality
        17. Make sure to implement a session storage cleanup functionality
        18. Make sure to implement a session storage cleanup on logout functionality
        19. Make sure to implement a session storage cleanup on session expiration functionality
        20. Make sure to implement a session storage cleanup on session timeout functionality
        21. Make sure to implement a session storage cleanup on session refresh functionality


    3. INTERFACE:
        1. Add a manage jobs interface (CRUD operations)
            1. the admin interface should have a simple UI to add jobs
            2. the admin interface should have a simple UI to edit jobs
            3. the admin interface should have a simple UI to delete jobs
            4. the admin interface should have a simple UI to view jobs
            5. the admin interface should have a simple UI to search jobs
        2. Each CRUD operation should have its own page with a url param like /admin/jobs/add, /admin/jobs/edit/:jobid, /admin/jobs/delete/:jobid, /admin/jobs/view/:jobid, /admin/jobs/search/:searchterm when the action is performed
        3. Add an interface to manage ADMINISTRATORS (CRUD operations)
            1. the admin interface should have a simple UI to add users
            2. the admin interface should have a simple UI to edit users
            3. the admin interface should have a simple UI to delete users
            4. the admin interface should have a simple UI to view users
            5. the admin interface should have a simple UI to search users
            6. Each CRUD operation should have its own page with a url param like /admin/users/add, /admin/users/edit/:userid, /admin/users/delete/:userid, /admin/users/view/:userid, /admin/users/search/:searchterm when the action is performed
        
2. Public job listing page
    1. This is open, no authentication required
    2. The job listing page should be simple and clean and will render the data from the API endpoint
    3. The job listing page should have a simple UI to apply for the job
    4. each job lisitng should have it own jobid in the url for tracking purposes
    5. each job listing should have a simple UI to apply for the job
    6. the applicant can just click on apply for now, ad the user will be taken to the CTA previously set by the admin
    7. the link will be opened on a new tab
    8. for now mock the CTA to a new page called ACME Company and a simple form, no matter the cta configured for now, redirect to the mock page
    6. This app is not a job board, it is a job matching platform and we make money by matching jobs to applicants and sending them to the CTA configured by the admin, but we do not collect any personal information from the applicant as they are redirected to the CTA configured by the admim, we probably just need to add a cookie as part of the URL to track the applicant and the job listing and the company can pay for the match. All this data should be stored in a database and we should be able to track the performance of the job listing and the company can pay for the match.
    7. The job listing page should have:
        1. H1 showing role and location, logos, company name and url
        2. Short context line explaining the job slice
        3. One primary ("hero") job
        4. 8–15 highly similar jobs as backup options at the bottom of the page
        5. Clear outbound apply links

3. Home Page
    1. By default the home page should show a nice landing page with a search bar to search for jobs, the search bar should be able to search by job title, job location, job category, job type, company name, company url, company logo, job application url, other details.
    2. The home page will have a modern and clean design, with the company name: Ontap Job Research, header and footer, copyright information, privacy policy, terms of service, contact information.
    3. this is what we will render whrn navigating to /
    4. if the user search for a job, we will navigate to /jobs/search/:searchterm, and we will render the search results page
    5. If a user clicks on any results, we will navigate to /jobs/:jobid, and we will render the job listing page
    6. if the user manually navigate to /jobs/:jobid, we will render the job listing page

4. Database:
    1. create the schema needed to accomplish this project, we will use postgres, and we will use prisma as the ORM so use prisma to create the schema and make it scalable, clean and extensible
    2. we will use docker to containerize the database and make it easy to deploy
    3. we will use docker to containerize the database and make it easy to scale
    4. Make sure to provide the scripts to create the database and the user needed to run the database
    5. Migrations should happen at the start of the server to populate the database with the initial data and tables
    6. If the database is not running, the server should not start
    7. if the database is not created, the server should create it and run the migrations
    8. If the database exists, the server should connect to it and run the migrations

5. Server:
    1. create the server needed to accomplish this project, we will use node.js and express
    2. we will use docker to containerize the server and make it easy to deploy
    3. we will use pm2 to run the server and make it easy to scale
    4. we will use docker to containerize the server and make it easy to deploy
    5. Server should have a /health endpoint
    6. Server should have a /heartbeat endpoint


    UI References:

    For the public job listing page, we will use the following reference:
    - /Users/pablo/Documents/ontap/docs/assets/public-listing.png -> create a page using a similar design but with the modern and clean design, same layout for the different sections 

    For the admin interface, we will use the following reference:
    - /Users/pablo/Documents/ontap/docs/assets/admin-listing.png -> Use the same theme BUT make sure to implement all the features mentioned in the previous section, make it modern and clean, and make it responsive as well. 

    For the home page, we will use the following reference:
    - /Users/pablo/Documents/ontap/docs/assets/home.png -> Use the same theme BUT make sure to implement all the features mentioned in the previous section, make it modern and clean, and make it responsive as well.

TEST DATA
1. Generate the CSV file nad JSON templates using the data from the following source: /Users/pablo/Documents/ontap/docs/assets/jobs-placeholder.png -> make sure to generate all the data to use them as import. Create a new folder called testdata and place the files there in 2 folders: csv and json.
2. This data will be used by the admin interface to import the data and use it to create the initial data in the database via UI.

DOCUMENTATION:
1. Use markdown to document the code
2. Use markdown to document the database schema
3. Use markdown to document the API endpoints
4. Use markdown to document the server configuration
5. Use markdown to document the deployment process
6. Use markdown to document the monitoring process
7. Use markdown to document the security process
8. Use markdown to document the testing process
9. Use markdown to document the maintenance process
10. Add a clear README.md to the repository with instructions on how to run the application include the docker commands to run the database and the server, and the environment variables needed to run the application
11. Add an ARCHITECTURE.md to the repository with the architecture of the application
12. Add a DEPLOYMENT.md to the repository with the deployment process
13. Add a MONITORING.md to the repository with the monitoring process



Must follow rules:

    1. DO NOT USE ANY HAYSTACK REFERECE!!
    2. DO NOT REIVENT THE WHEEL!! Use exisitng libraries and packages no hacks and more importan NO FALLBACKS!!
    3. Use SOLID Principles
    4. Use Clean Code Principles
    5. Use Clean Architecture Principles
    6. Use Clean UI Principles
    7. Use Clean Database Principles
    8. Use Clean Security Principles
    9. Use Clean Testing Principles
    10. Use Clean Deployment Principles
    11. Use Clean Monitoring Principles
    12. Use Clean Documentation Principles
    13. Use Clean Infrastructure Principles
    14. Use Clean Operations Principles
    15. Use Clean Maintenance Principles
    16. Use Clean Performance Principles
    17. Use Clean Scalability Principles
    18. Use Clean Resilience Principles

    


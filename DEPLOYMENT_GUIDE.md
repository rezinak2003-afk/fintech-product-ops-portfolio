# Deployment Guide — all three projects

The three applications are static HTML/CSS/JavaScript sites, so GitHub Pages is a simple free-hosting option for a public portfolio repository. GitHub Pages publishes static files; it does not run Python or a server-side database. Official instructions: [Create a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site) and [configure publishing from a branch](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Option A — publish all three under one portfolio URL (recommended)

1. Download and unzip `fintech_product_ops_projects.zip`.
2. Sign in to GitHub and create a **public** repository, for example `fintech-product-ops-portfolio`. Do not add secrets or sensitive data; GitHub Pages sites are public.
3. Upload the **contents** of this package to the repository root (the top-level `index.html` is the portfolio landing page). Alternatively use Git:

   ```bash
   git init
   git add .
   git commit -m "Build fintech product operations portfolio projects"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/fintech-product-ops-portfolio.git
   git push -u origin main
   ```

4. In the repository open **Settings → Pages**.
5. Under **Build and deployment**, select **Deploy from a branch**, choose branch `main` and folder `/(root)`, then Save.
6. Wait for the Pages deployment to finish and copy the exact URL shown in Settings → Pages. The usual format is `https://YOUR-USERNAME.github.io/fintech-product-ops-portfolio/`.
7. Your project pages will be underneath that base URL:
   - `/01-kyc-product-teardown/`
   - `/02-loan-true-cost-calculator/`
   - `/03-funnel-retention-analysis/`
8. Test the main page and all three project links in a private/incognito browser window. Check the calculator on mobile; check the dashboard filters and its `dashboard_data.json` network request.

## Option B — deploy only one project as its own site

For each project you want to separate:
1. Create a new public GitHub repository.
2. Copy the **contents** of that project folder (not the folder itself) into the repository root so `index.html` is at the root.
3. Commit/upload the files.
4. Repeat **Settings → Pages → Deploy from a branch → main → /(root) → Save**.
5. Copy the published URL shown by GitHub; don't guess or hardcode a URL before it exists.

For Project 3, include `dashboard_data.json`, `data/`, `sql/`, and `generate_dashboard_data.py` as well as `index.html`. Only `index.html` and `dashboard_data.json` are needed for the hosted dashboard; the other files make the project reproducible and reviewable.

## Project-specific setup

### 1. KYC teardown
- The prototype works without API keys or a backend.
- Complete genuine usability interviews, enter anonymised notes into `research_log_template.csv`, and update the PRD with evidence before claiming a sample size or top finding.
- To use Figma, follow `01-kyc-product-teardown/Figma_Build_Spec.md`; the package contains the HTML prototype and instructions, not a native Figma file.
- To collect survey responses, create the form from `Google_Forms_Survey.md` and add the public link to the project README once it exists.

### 2. Loan calculator
- Before deployment, open `02-loan-true-cost-calculator/config.js`.
- For no analytics, leave `gaMeasurementId` blank. The calculator still works.
- To use GA4, create a website data stream in your GA4 property, copy the web Measurement ID, set `gaMeasurementId`, and redeploy. Google instructions: [Set up Analytics for a website](https://support.google.com/analytics/answer/14183469?hl=en).
- Analytics is optional and consent-gated; do not add loan values, identifiers or personal data to events. Test with a dedicated property and confirm events in GA4 before writing that tracking is live.
- To connect feedback, create a Google Form using `analytics_and_google_forms.md`, publish it, and paste the responder URL into `feedbackFormUrl` in `config.js`. Google Forms guide: [How to use Google Forms](https://support.google.com/docs/answer/6281888?hl=en-IN).
- Revalidate calculation outputs against an independent calculator or approved formula before presenting any results as financially authoritative. This demo's “effective annual rate” is an educational estimate, not a legal APR disclosure.

### 3. Funnel and retention analysis
- The deployed visual uses `dashboard_data.json`, not a live database. Re-run the packaged generator after changing the CSVs to rebuild the aggregates.
- Locally, from the project folder run `python -m http.server 8000` and open `http://localhost:8000`.
- Run SQL by following `03-funnel-retention-analysis/sql/README.md` and `import_and_run.py` (Python standard library only).
- For a Power BI version, follow `sql/power_bi_measures.md`. A native `.pbix` file is not included; the ready-to-view implementation is the static interactive dashboard plus reproducible SQL and source CSVs.
- Keep the synthetic-data disclaimer visible. If you later replace the synthetic records with approved real data, revise privacy controls, definitions, cut-off dates, and findings before sharing.

## Release checklist
- [ ] Repository contains no secrets, real KYC documents, personal data, or private URLs.
- [ ] Main landing page and every nested page work using relative paths.
- [ ] Project 1 still labels all unconducted research as planned.
- [ ] Project 2 calculations have been cross-checked, consent choice works, and Analytics/Form IDs are blank or correctly configured.
- [ ] Project 3 is prominently labelled synthetic; filters and cohort matrix work.
- [ ] Public URLs copied from GitHub Pages are tested in a private window before adding to your resume.

# Deploy this finished dashboard to your existing GitHub Pages portfolio

The interactive website is already built and comes with populated aggregate data. You do **not** need to run Python or build the web charts before deployment.

## Destination repository

`https://github.com/rezinak2003-afk/fintech-product-ops-portfolio`

## Recommended route: GitHub Desktop

1. Download and extract `Retail_Sales_Customer_Analytics_Deployment_Package.zip`.
2. Open your existing repository's local clone in GitHub Desktop. If you have not cloned it, use **File → Clone repository** and select `rezinak2003-afk/fintech-product-ops-portfolio`.
3. Copy the complete folder named `04-retail-sales-powerbi` into the root of the cloned repository. The new folder should sit next to your existing `index.html` and project folders. Do not replace your existing homepage or any existing project folder.
4. Confirm `04-retail-sales-powerbi/index.html` and `04-retail-sales-powerbi/data/dashboard_data.json` both exist. Keep the entire directory structure intact.
5. In GitHub Desktop, review the changes, enter commit message `Add retail sales and customer analytics dashboard`, click **Commit to main**, then click **Push origin**.
6. GitHub Pages is already enabled in the portfolio. Wait for the latest commit to deploy. You do not need to change the Pages source settings if they currently use `main` and `/(root)`.
7. Open: `https://rezinak2003-afk.github.io/fintech-product-ops-portfolio/04-retail-sales-powerbi/`

## What should load

The new page contains four KPI cards; monthly revenue trend; country revenue mix; top products; monthly return rate; customer RFM segments; first-month cohort retention; and methodology/provenance notes. Switch between the Overview, Customers & retention, and Methodology tabs. The trend period and country filters should respond. No external JavaScript CDN is needed.

## If it does not load

- A 404 usually means the folder was uploaded at the wrong level or not pushed to `main`. Confirm the path is exactly `04-retail-sales-powerbi/index.html`.
- If the page appears but charts are blank, confirm `data/dashboard_data.json` is present beside the dashboard's `data/` folder and got pushed.
- Use a hard refresh (`Ctrl+F5`) after the deploy finishes.

## Native Power BI report

The Excel import pack and CSVs are included. The interactive website is fully built for deployment. A native `.pbix` is not included because it must be saved by Power BI Desktop; the report outline and DAX measures are provided in `powerbi/`.

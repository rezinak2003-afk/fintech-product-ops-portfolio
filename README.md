# Fintech Product & Product Operations Portfolio Projects

Three runnable, independently useful portfolio projects:

1. **Product Teardown & KYC Redesign** — fictional BNPL KYC prototype, PRD, research plan, RICE prioritisation, survey copy and A/B-test design.
2. **Loan True-Cost Calculator** — browser calculator for EMI, fees, net disbursal, total borrowing cost and an effective annual rate estimate; optional GA4 and Google Forms configuration.
3. **Funnel & Retention Analysis** — interactive segmented dashboard, reproducible synthetic CSV data, SQLite analysis queries and Power BI recreation notes.

## Preview locally

From the root folder run:

```bash
python -m http.server 8000
```

Open `http://localhost:8000`. Each project has its own `index.html` and README. Project 3 fetches a JSON file and therefore must be served over HTTP, not opened as a `file://` URL.

## Data / claims integrity
- Project 1 research is planned, not completed; it has no real interviews or measured top finding.
- Project 2 has no actual usage figures or experiment results until deployed and used by real visitors.
- Project 3 data are **synthetic** and do not represent a real BNPL service or real users.
- There is no live Google Analytics property, Google Form, Figma file, Jira project or public hosting URL connected by this package. Configuration and creation instructions are included.

Read `DEPLOYMENT_GUIDE.md` to publish the portfolio on GitHub Pages.

# Loan True-Cost Calculator

A responsive, client-side EMI calculator that includes illustrative processing fees and fee tax, then estimates an effective annual borrowing rate from the amount actually disbursed and the monthly repayment stream.

## Features
- EMI, total interest, total repayment, fees/tax, net disbursed amount and all-in cost breakdown.
- Effective annual rate estimated with a numerical monthly cash-flow IRR calculation.
- Responsive UI and input validation.
- Optional Google Analytics 4 event wiring with explicit opt-in. No principal, term, rate, or other entered values are sent to analytics.
- Optional Google Forms feedback link.
- Test cases, event plan, Jira backlog, and Figma wireframe spec.

## Important limitation
This is an educational calculator, not a lender quote, regulated APR disclosure, or financial advice. Actual APR depends on jurisdiction, cash-flow dates, fee treatment, taxes, insurance, compounding and product-specific rules. Results must be independently validated before any consumer or production use.

## Run locally
Open `index.html` or run `python -m http.server 8000` from this folder, then open `http://localhost:8000`.

## Configure integrations
Edit `config.js`:
- `gaMeasurementId`: enter the GA4 web-stream Measurement ID such as `G-XXXXXXXXXX` only after setting up the property and reviewing consent/privacy requirements.
- `feedbackFormUrl`: enter the published responder URL of your feedback Google Form.

Analytics is disabled until a user opts in via the banner. Do not send application values, financial details or PII as event parameters. Use a dedicated test property initially.

## Deploy
See root `DEPLOYMENT_GUIDE.md`.

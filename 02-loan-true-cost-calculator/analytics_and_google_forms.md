# Analytics & Feedback Integration Plan

## GA4 setup
1. Create or choose a dedicated GA4 property and web data stream for this demo.
2. Copy the web Measurement ID (format `G-XXXXXXXXXX`) and set `gaMeasurementId` in `config.js`.
3. Redeploy the static site and test on the deployed HTTPS URL with GA DebugView/Realtime.
4. Keep consent opt-in enabled; provide a clear privacy notice appropriate to your use and jurisdiction.
5. Verify event counts; do not add loan amount, interest rate, tenure, fees, contact details, application identifiers or other values to analytics parameters.

Events in this build: `calculator_calculated`, `feedback_link_clicked`. These are generic events only; no financial input values are sent. If GA is not configured, no GA script is loaded.

## Google Forms
Create a blank form at https://forms.google.com and use these questions:
1. Was the monthly EMI estimate easy to understand? (1–5)
2. Before using the calculator, did you consider processing fees? (Yes / No / Not sure)
3. Which output was most useful? (EMI / Total interest / Fees and tax / Net amount received / Effective annual rate estimate)
4. What was confusing or missing? (Optional paragraph)
5. Would you use a calculator like this before comparing a loan offer? (Yes / No / Not sure)

Intro note: “This is a student portfolio prototype, not a lender quote. Do not submit personal, banking, application, or financial account identifiers.” Link responses to a restricted Google Sheet, then put the published responder URL in `config.js`.

## Funnel definitions
- **Calculator completion:** `calculator_calculated` event / unique calculator page sessions (define sessionization before reporting).
- **Feedback click-through:** `feedback_link_clicked` / calculator page sessions.
- **Feedback response rate:** valid submitted responses / unique feedback-form visits, only if form visits can be measured consistently.

Do not claim a completion lift or user count until you collect and validate real data. Google Analytics users/events can differ due to consent, blockers and measurement limitations; state the method and date range.

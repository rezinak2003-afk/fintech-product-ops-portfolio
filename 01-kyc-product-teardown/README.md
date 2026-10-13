# Product Teardown & KYC Redesign

**Portfolio case study · BNPL onboarding · HTML prototype + PRD + research pack**

## What's included
- `index.html`: interactive baseline-vs-redesign prototype. The prototype is local and never sends or stores the entered sample details.
- `PRD.md`: problem framing, requirements, user stories and acceptance criteria.
- `RICE_and_AB_Test_Plan.md`: prioritisation, experiment design, metrics and guardrails.
- `Research_Plan_and_Interview_Guide.md`: ten-user moderated research plan, interview script and coding framework.
- `Google_Forms_Survey.md`: copy-ready survey questions and consent wording.
- `research_log_template.csv`: blank log to populate only after real sessions.
- `Figma_Build_Spec.md`: exact frames and components for recreating the redesign in Figma.

## Scope and honesty note
This is a **simulated portfolio exercise** based on a fictional BNPL product, `FlexiPay`. No live provider funnel was instrumented, no participant was interviewed, and no survey was run as part of this package. The drop-off cause is a hypothesis to validate, not a finding. Do not claim `10 users interviewed`, a survey sample size, or a measured lift until you conduct the research and experiment yourself.

## Run locally
Open `index.html` in a browser. It uses only HTML, CSS and JavaScript. To test with a local server, run `python -m http.server 8000` from this folder and open `http://localhost:8000`.

## Suggested execution order
1. Recruit 8–10 eligible participants; obtain consent before recording or taking notes.
2. Use the prototype for usability tasks; record completion, hesitation, errors and verbatim comments.
3. Code the notes in the research log; use observed evidence to update the hypothesis.
4. Revise the PRD, prioritisation and experiment plan based on actual evidence.
5. Recreate the final frames in Figma and link its prototype from the project README once published.

See the root `DEPLOYMENT_GUIDE.md` for GitHub Pages publishing.

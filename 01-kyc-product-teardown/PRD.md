# Product Requirements Document — BNPL KYC Redesign

**Product:** FlexiPay (fictional) · **Version:** 0.1 portfolio draft · **Status:** hypothesis pending research

## 1. Problem statement
Users applying for a hypothetical buy-now-pay-later product may abandon identity verification when requirements, accepted document types, upload limits, and next steps are unclear. The proposed redesign makes requirements visible before upload, explains why information is needed, supports recovery from upload errors, and makes progress clear.

**Problem hypothesis, not a validated finding:** confusing document requirements and weak error recovery contribute to KYC abandonment, particularly on mobile. The first research round must test this rather than assume it.

## 2. Target users and jobs to be done
- **Primary:** a first-time BNPL applicant using a mobile browser who wants to understand eligibility and complete identity verification without repeated attempts.
- **Secondary:** a returning applicant who needs to resume an incomplete application and understand what remains.
- **Job:** “When I apply for pay-later checkout, help me verify my identity with confidence and without avoidable rework.”

## 3. Goals and non-goals
**Goals**
- Set expectations before a user begins document capture.
- Reduce avoidable upload errors and repeated attempts.
- Make progress, privacy purpose, and help options understandable.
- Measure funnel completion and failure reasons without collecting unnecessary personal data.

**Non-goals**
- Real identity verification, credit decisions, lending, or document transmission.
- Collecting real government identifiers or identity documents in this prototype.
- Making claims about any actual lender, regulated entity, or production KYC policy.

## 4. Proposed experience
1. **Eligibility & expectations:** explain time, needed document types, and why verification is required.
2. **Applicant details:** collect only fields required for the hypothetical flow; clearly mark required fields.
3. **Document choice & upload:** explain accepted formats and limits before file selection; give retry and help affordances.
4. **Review & status:** summarise what was provided and explain what happens next.

The prototype’s file upload is intentionally simulated. No file or personal data leaves the browser.

## 5. User stories and acceptance criteria

### US-01 — Know what I need before starting
As an applicant, I want to see the requirements and expected time before I start so that I can decide whether to continue.
- **AC1:** The first screen states the purpose, estimated steps, and document requirement.
- **AC2:** The user can continue or leave without entering details.
- **AC3:** No unverified promise of approval time or credit eligibility is displayed.

### US-02 — Understand required fields
As an applicant, I want required fields to be clearly identified so that I can complete the form without guesswork.
- **AC1:** Required fields have visible labels and programmatic labels.
- **AC2:** Invalid or missing fields receive an inline message adjacent to the field.
- **AC3:** Errors preserve valid entries and explain how to resolve the issue.

### US-03 — Choose and upload an accepted document
As an applicant, I want to know accepted types and limits before choosing a document.
- **AC1:** The screen shows the accepted file formats and size limit before upload.
- **AC2:** Unsupported or oversized files receive a specific corrective message.
- **AC3:** Retry is available without restarting the journey.
- **AC4:** A help route is visible from the upload step.

### US-04 — Review before submitting
As an applicant, I want to review the details and understand next steps before submission.
- **AC1:** A review screen shows a summary before the final action.
- **AC2:** The user can return to an earlier step and edit details.
- **AC3:** The confirmation explains that the prototype did not transmit information.

## 6. Functional requirements
- Four-step redesigned journey with a visible progress indicator.
- Inline validation and back navigation.
- Accepted formats shown before the upload action.
- Upload state is simulated only; no backend, API, or storage is connected.
- Clear privacy-purpose copy and help affordance.
- Keyboard-accessible controls and responsive layout.

## 7. Analytics requirements
Record only non-identifying event names after appropriate consent and after implementing a lawful, transparent production analytics setup. Candidate events: `kyc_intro_viewed`, `kyc_details_completed`, `kyc_document_type_selected`, `kyc_upload_succeeded`, `kyc_upload_failed`, `kyc_review_viewed`, `kyc_flow_completed`, and `kyc_flow_exited`. Do not put names, government IDs, documents, dates of birth, raw form values, or other personal data into analytics events.

## 8. Success metrics and guardrails
- **Primary:** KYC completion rate = completed KYC journeys / journeys started.
- **Secondary:** median time to completion; document upload success rate; retry rate; help-link usage; task success in moderated tests.
- **Guardrails:** error rate, duplicate submissions, complaints, support contact rate, privacy/security incidents, accessibility task failures, and abandonment shifted to later steps.
- **Segmentation:** device and acquisition channel only when sample sizes and privacy policies support it.

## 9. Dependencies and risks
- Legal/compliance approval of document requirements and consent language.
- KYC provider capabilities, accepted formats, file-size limits, and accessibility support.
- Privacy/security review before real document collection or analytics.
- Selection bias in convenience-sample usability testing; small studies diagnose usability, not population prevalence.

## 10. Open questions
- Which documents and markets are actually in scope?
- What are the real provider file constraints and error codes?
- Can an applicant save and resume safely?
- Which support route is staffed and what response expectations are approved?
- What baseline completion rate and minimum detectable effect are available?

# Prioritisation & A/B Test Plan

**All scores below are initial analyst estimates for planning, not research findings. Re-score after interviews and engineering estimates.**

## RICE prioritisation
RICE score = (Reach × Impact × Confidence) / Effort. Reach is expressed as affected applicants per quarter; impact uses a 0.25–3 scale; confidence is 0–1; effort is person-weeks. Placeholder reach estimates are intentionally marked as assumptions.

| Improvement | Reach assumption / qtr | Impact | Confidence | Effort (person-weeks) | RICE | Why prioritise |
|---|---:|---:|---:|---:|---:|---|
| Show accepted formats and size limits before selection | 1,000* | 2.0 | 0.70 | 1.0 | 1,400 | Low effort; prevents avoidable retries |
| Add specific upload failure and retry states | 1,000* | 2.0 | 0.65 | 1.5 | 867 | Helps users recover instead of restarting |
| Add progress indicator and step estimate | 1,000* | 1.0 | 0.70 | 1.0 | 700 | Sets expectations across the journey |
| Add plain-language purpose/privacy explanation | 1,000* | 1.0 | 0.60 | 1.0 | 600 | Supports trust and informed decisions |
| Save-and-resume for incomplete applications | 350* | 2.0 | 0.35 | 4.0 | 61 | Potential benefit, but security and backend complexity |

`*` Reach values are illustrative planning assumptions, not product traffic. Change them to actual eligible funnel volume before using the ranking for roadmap decisions.

## Experiment question
Does a redesigned document-upload step, which exposes format/size requirements earlier and provides actionable recovery messages, increase successful KYC completion versus the existing experience without increasing security, error, or support issues?

## Design
- **Control:** current approved production flow, instrumented consistently.
- **Variant:** redesigned document-upload step; do not change other screens during the first test unless required for safety/accessibility.
- **Randomisation:** persistent user/applicant-level assignment; avoid assigning one person to both variants.
- **Eligibility:** eligible new applicants reaching KYC; define exclusions in advance.
- **Primary metric:** KYC completion within a pre-defined window after KYC start.
- **Secondary metrics:** upload success on first attempt, upload retries per applicant, median time from KYC start to submission, help usage.
- **Guardrails:** validation failures, duplicate applications, support contacts, suspicious activity, privacy/security events, accessibility defects, and downstream approval quality where appropriate.
- **Duration:** run until the pre-calculated sample size and minimum duration are reached; do not stop early based on daily fluctuations.

## Sample size and analysis plan
1. Pull a recent baseline conversion rate from the real funnel.
2. Agree the minimum detectable absolute or relative improvement with Product, Analytics and Risk.
3. Set a two-sided significance level (commonly 5%) and power (commonly 80%); use a validated sample-size calculator or statistical package for a two-proportion test.
4. Account for exclusions, missing events and clustering if assignment is not independent.
5. Pre-register the primary metric, guardrails, exclusion rules and analysis window.
6. Report absolute percentage-point change, relative change, confidence interval, sample sizes and guardrail deltas. A statistically significant result is not automatically a meaningful business result.

## Decision rules
- **Ship:** primary metric improves by the pre-agreed practical threshold and no guardrail breaches occur.
- **Iterate:** positive but inconclusive effect, or qualitative sessions identify a fixable usability issue.
- **Do not ship:** meaningful decline or guardrail breach.

## Before launch checklist
- [ ] Events fire once and have defined numerator/denominator.
- [ ] Consent/privacy notice and retention are approved.
- [ ] Experiment assignment is stable and sample ratio is checked.
- [ ] KYC/vendor, Risk, Compliance, Support and Accessibility sign off.
- [ ] The team has an incident/rollback plan.
- [ ] All hypotheses, metrics and thresholds are timestamped before reading results.

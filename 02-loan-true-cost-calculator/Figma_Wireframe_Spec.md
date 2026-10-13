# Figma Wireframe Spec — Loan True-Cost Calculator

Create a Figma file with desktop (1440 × 1000) and mobile (390 × 844) frames.

## Desktop layout
- Top nav with “Fintech product prototype” label and Reset button.
- Heading/subhead and visible “Educational estimate only” notice.
- Two-column area: assumptions form (principal, nominal interest, tenure, processing fee %, fixed fee, tax on fees) on the left; EMI result, effective annual rate estimate and fee/interest breakdown on the right.
- Bottom privacy note and optional analytics preference card.

## Components/variants
- Text input: default, focused, invalid, disabled.
- Primary button: default, hover, disabled/loading.
- Fee row: label + tabular currency amount.
- Result tile: EMI and effective annual rate estimate.
- Notice: caution/validation/help.
- Consent prompt: opted in / declined / undecided.

## Interaction notes
- Calculate updates EMI, interest, net proceeds, repayment total, all-in cost and effective annual rate estimate.
- Invalid values show inline errors and do not show misleading results.
- User can reject analytics; no numeric loan assumptions are analytics parameters.
- If fees equal or exceed principal, display that net proceeds are non-positive and the rate estimate is not meaningful.

This is a spec to recreate an editable Figma file; the deliverable contains a working HTML implementation rather than a native `.fig` file.

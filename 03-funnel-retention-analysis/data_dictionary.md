# Data Dictionary

## `users.csv` — one row per synthetic visitor ID
| Field | Type | Meaning |
|---|---|---|
| `user_id` | string | Synthetic ID; does not identify a real person |
| `first_seen_date` | ISO date | First simulated landing date |
| `signup_date` | ISO date / blank | Simulated signup date when sign-up succeeded |
| `signup_week` | ISO Monday date / blank | Week commencing for signup; blank for non-signups |
| `device` | category | Android, iOS, or Desktop (synthetic assignment) |
| `region` | category | North, South, West, East, or Central (synthetic assignment) |
| `acquisition_channel` | category | Organic Search, Paid Social, Referral, Affiliate |

## `events.csv` — one row per synthetic event
| Field | Type | Meaning |
|---|---|---|
| `event_id` | string | Synthetic unique event key |
| `user_id` | string | Links to users table |
| `event_name` | category | Funnel event or `app_active` |
| `event_ts` | timestamp | Simulated event timestamp |
| `week_since_signup` | integer / blank | Simulated activity week index for `app_active`; blank for funnel events |

## Funnel definition
`landing_view` → `signup_started` → `kyc_started` → `kyc_submitted` → `kyc_approved` → `loan_offer_viewed` → `calculator_completed` → `application_submitted` → `loan_approved`.

Each stage conversion displayed by the dashboard uses unique users at the stage divided by unique landing visitors (not the prior stage). The dashboard also calculates the percentage-point drop between consecutive stage rates. Clearly state your denominator when presenting a funnel.

## Synthetic data caveat
The generator assigns conversion probabilities for demonstration. The labels are intentionally generic and the `device`/`region` effects are programmed into generation logic. Never describe this file as production, anonymised customer, or third-party provider data.

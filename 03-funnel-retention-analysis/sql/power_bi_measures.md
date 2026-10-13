# Rebuild in Power BI Desktop

The deployed HTML dashboard is the ready-to-view artifact. To demonstrate the same analysis in Power BI, load `data/users.csv` and `data/events.csv` as tables and create a one-to-many relationship from `users[user_id]` to `events[user_id]`.

## Useful measures (DAX)

```DAX
Visitors = DISTINCTCOUNT(users[user_id])
Landing Visitors = CALCULATE(DISTINCTCOUNT(events[user_id]), events[event_name] = "landing_view")
Signup Started = CALCULATE(DISTINCTCOUNT(events[user_id]), events[event_name] = "signup_started")
KYC Started = CALCULATE(DISTINCTCOUNT(events[user_id]), events[event_name] = "kyc_started")
KYC Submitted = CALCULATE(DISTINCTCOUNT(events[user_id]), events[event_name] = "kyc_submitted")
KYC Approved = CALCULATE(DISTINCTCOUNT(events[user_id]), events[event_name] = "kyc_approved")
Calculator Completed = CALCULATE(DISTINCTCOUNT(events[user_id]), events[event_name] = "calculator_completed")
Application Submitted = CALCULATE(DISTINCTCOUNT(events[user_id]), events[event_name] = "application_submitted")
Loan Approved = CALCULATE(DISTINCTCOUNT(events[user_id]), events[event_name] = "loan_approved")
Signup Conversion % = DIVIDE([Signup Started], [Landing Visitors])
KYC Submission % = DIVIDE([KYC Submitted], [Landing Visitors])
Loan Approval % = DIVIDE([Loan Approved], [Landing Visitors])
Active Users = CALCULATE(DISTINCTCOUNT(events[user_id]), events[event_name] = "app_active")
```

## Suggested visuals
- Funnel visual: stage name and unique user count, with denominator and event definition documented.
- Matrix: device × region with KYC submission %, application submission %, loan approval %.
- Weekly cohort matrix: rows `users[signup_week]`, columns week offset (from a generated activity-week column), values active users / eligible cohort size.
- Slicers: device, region, acquisition channel.
- Cards: dataset window, visitors, signed-up users, generated event count, and a visible “synthetic data” label.

For the cohort matrix, add a calculated `week_offset` to events using the date difference between event date and signup date, exclude `week_offset` rows whose full seven-day observation window exceeds the dataset cutoff, and divide active distinct users by the original cohort size. Do not compare censored cohorts to fully observed cohorts without making the observability rule explicit.

**Important:** measures are intended for a portfolio exercise and should be validated against the SQL results. Relationships and filter context can affect distinct-count measures; test each with the same denominator.

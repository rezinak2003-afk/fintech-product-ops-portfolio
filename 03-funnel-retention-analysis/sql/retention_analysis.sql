-- Weekly cohort retention (SQLite).
-- signup_week is the Monday date that starts a user's signup week.
-- For each cohort and week offset, an active user is a signed-up user with >=1 app_active event that week.
-- Exclude partially observed future weeks by requiring the full 7-day window to be within 2026-09-30.
WITH cohort_sizes AS (
  SELECT signup_week, COUNT(DISTINCT user_id) AS cohort_size, MIN(signup_date) AS earliest_signup
  FROM users WHERE signup_date IS NOT NULL AND signup_week IS NOT NULL
  GROUP BY signup_week
), active AS (
  SELECT u.signup_week,
         CAST((julianday(date(e.event_ts))-julianday(date(u.signup_date)))/7 AS INTEGER) AS week_offset,
         COUNT(DISTINCT u.user_id) AS active_users
  FROM users u JOIN events e ON e.user_id=u.user_id
  WHERE u.signup_date IS NOT NULL AND e.event_name='app_active'
  GROUP BY u.signup_week, week_offset
), observed AS (
  SELECT c.signup_week, c.cohort_size, a.week_offset,
         COALESCE(a.active_users,0) AS active_users
  FROM cohort_sizes c JOIN active a ON a.signup_week=c.signup_week
  WHERE date(c.earliest_signup, '+' || (a.week_offset*7+6) || ' days') <= '2026-09-30'
)
SELECT signup_week, cohort_size, week_offset, active_users,
       ROUND(100.0*active_users/NULLIF(cohort_size,0),1) AS retention_pct
FROM observed
ORDER BY signup_week, week_offset;

-- Aggregate retention curve by week offset. Denominator is only users whose full week window is observable.
WITH signed_up AS (
  SELECT user_id, signup_date FROM users WHERE signup_date IS NOT NULL
), offsets AS (
  SELECT 0 AS week_offset UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
  UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
  UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13
), eligible AS (
  SELECT o.week_offset, s.user_id FROM offsets o JOIN signed_up s
    ON date(s.signup_date, '+' || (o.week_offset*7+6) || ' days') <= '2026-09-30'
), active AS (
  SELECT e.user_id,
         CAST((julianday(date(e.event_ts))-julianday(date(u.signup_date)))/7 AS INTEGER) AS week_offset
  FROM events e JOIN users u ON u.user_id=e.user_id
  WHERE e.event_name='app_active'
  GROUP BY e.user_id, week_offset
)
SELECT el.week_offset, COUNT(DISTINCT el.user_id) AS eligible_users,
       COUNT(DISTINCT ac.user_id) AS active_users,
       ROUND(100.0*COUNT(DISTINCT ac.user_id)/NULLIF(COUNT(DISTINCT el.user_id),0),1) AS retention_pct
FROM eligible el LEFT JOIN active ac ON ac.user_id=el.user_id AND ac.week_offset=el.week_offset
GROUP BY el.week_offset ORDER BY el.week_offset;

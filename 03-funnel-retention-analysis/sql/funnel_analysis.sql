-- Funnel conversion by device and region.
-- Stage rates below use all unique landing visitors as the denominator.
WITH stage_counts AS (
  SELECT
    u.device,
    u.region,
    COUNT(DISTINCT u.user_id) AS visitors,
    COUNT(DISTINCT CASE WHEN e.event_name='signup_started' THEN u.user_id END) AS signup_started,
    COUNT(DISTINCT CASE WHEN e.event_name='kyc_started' THEN u.user_id END) AS kyc_started,
    COUNT(DISTINCT CASE WHEN e.event_name='kyc_submitted' THEN u.user_id END) AS kyc_submitted,
    COUNT(DISTINCT CASE WHEN e.event_name='kyc_approved' THEN u.user_id END) AS kyc_approved,
    COUNT(DISTINCT CASE WHEN e.event_name='loan_offer_viewed' THEN u.user_id END) AS loan_offer_viewed,
    COUNT(DISTINCT CASE WHEN e.event_name='calculator_completed' THEN u.user_id END) AS calculator_completed,
    COUNT(DISTINCT CASE WHEN e.event_name='application_submitted' THEN u.user_id END) AS application_submitted,
    COUNT(DISTINCT CASE WHEN e.event_name='loan_approved' THEN u.user_id END) AS loan_approved
  FROM users u
  LEFT JOIN events e ON e.user_id=u.user_id
  GROUP BY u.device, u.region
)
SELECT device, region, visitors,
  ROUND(100.0*signup_started/NULLIF(visitors,0),1) AS signup_started_pct,
  ROUND(100.0*kyc_started/NULLIF(visitors,0),1) AS kyc_started_pct,
  ROUND(100.0*kyc_submitted/NULLIF(visitors,0),1) AS kyc_submitted_pct,
  ROUND(100.0*kyc_approved/NULLIF(visitors,0),1) AS kyc_approved_pct,
  ROUND(100.0*loan_offer_viewed/NULLIF(visitors,0),1) AS offer_viewed_pct,
  ROUND(100.0*calculator_completed/NULLIF(visitors,0),1) AS calculator_completed_pct,
  ROUND(100.0*application_submitted/NULLIF(visitors,0),1) AS application_submitted_pct,
  ROUND(100.0*loan_approved/NULLIF(visitors,0),1) AS loan_approved_pct
FROM stage_counts
ORDER BY device, region;

-- Overall funnel and percentage-point drop between consecutive stages.
WITH stage AS (
 SELECT 'Landing views' AS stage, 1 AS ord, COUNT(DISTINCT user_id) AS n FROM events WHERE event_name='landing_view'
 UNION ALL SELECT 'Signup started',2,COUNT(DISTINCT user_id) FROM events WHERE event_name='signup_started'
 UNION ALL SELECT 'KYC started',3,COUNT(DISTINCT user_id) FROM events WHERE event_name='kyc_started'
 UNION ALL SELECT 'KYC submitted',4,COUNT(DISTINCT user_id) FROM events WHERE event_name='kyc_submitted'
 UNION ALL SELECT 'KYC approved',5,COUNT(DISTINCT user_id) FROM events WHERE event_name='kyc_approved'
 UNION ALL SELECT 'Offer viewed',6,COUNT(DISTINCT user_id) FROM events WHERE event_name='loan_offer_viewed'
 UNION ALL SELECT 'Calculator completed',7,COUNT(DISTINCT user_id) FROM events WHERE event_name='calculator_completed'
 UNION ALL SELECT 'Application submitted',8,COUNT(DISTINCT user_id) FROM events WHERE event_name='application_submitted'
 UNION ALL SELECT 'Loan approved',9,COUNT(DISTINCT user_id) FROM events WHERE event_name='loan_approved'
), rates AS (
 SELECT stage,ord,n,100.0*n/NULLIF((SELECT n FROM stage WHERE ord=1),0) AS visitor_conversion_pct FROM stage
)
SELECT stage,n,ROUND(visitor_conversion_pct,1) AS visitor_conversion_pct,
 ROUND(LAG(visitor_conversion_pct) OVER(ORDER BY ord)-visitor_conversion_pct,1) AS drop_vs_previous_stage_pp
FROM rates ORDER BY ord;

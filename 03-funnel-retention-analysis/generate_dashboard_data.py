"""Rebuild dashboard aggregates from the packaged synthetic CSVs."""
from pathlib import Path
import csv, json, datetime
ROOT=Path(__file__).resolve().parent
with (ROOT/'data'/'users.csv').open(newline='',encoding='utf-8') as f: users=list(csv.DictReader(f))
with (ROOT/'data'/'events.csv').open(newline='',encoding='utf-8') as f: events=list(csv.DictReader(f))
labels=['Landing views','Sign-up started','KYC started','KYC submitted','KYC approved','Loan offer viewed','Calculator completed','Application submitted','Loan approved']
funnel=['landing_view','signup_started','kyc_started','kyc_submitted','kyc_approved','loan_offer_viewed','calculator_completed','application_submitted','loan_approved']
end=datetime.date(2026,9,30); user_by={u['user_id']:u for u in users}
stage_users={name:set(e['user_id'] for e in events if e['event_name']==name) for name in funnel}
active={}
for e in events:
    if e['event_name']=='app_active':active.setdefault(e['user_id'],set()).add(int(e['week_since_signup']))
def agg(dev='All',reg='All'):
    us=[u for u in users if (dev=='All' or u['device']==dev) and (reg=='All' or u['region']==reg)]
    ids={u['user_id'] for u in us};counts=[len(ids&s) for s in [stage_users[e] for e in funnel]]
    su=[u for u in us if u['signup_date']]
    ret=[]
    for wk in range(14):
        eligible=[u for u in su if datetime.date.fromisoformat(u['signup_date'])+datetime.timedelta(days=wk*7+6)<=end]
        cnt=sum(wk in active.get(u['user_id'],set()) for u in eligible)
        ret.append({'week':wk,'eligible_signups':len(eligible),'active_users':cnt,'rate':round(100*cnt/len(eligible),1) if eligible else None})
    return {'device':dev,'region':reg,'visitors':len(us),'stageCounts':counts,'stages':[round(100*x/len(us),1) if us else 0 for x in counts],'signups':len(su),'retention':ret}
segments=[agg(d,r) for d in ['Android','iOS','Desktop'] for r in ['North','South','West','East','Central']]
overall=agg();rates=overall['stages'];drop=max(range(1,len(rates)),key=lambda i:rates[i-1]-rates[i])
cohorts={}
for week in sorted(set(u['signup_week'] for u in users if u['signup_week'])):
    su=[u for u in users if u['signup_week']==week and u['signup_date']]; row={'signup_week':week,'cohort_size':len(su),'retention':[]}
    for wk in range(13):
        eligible=[u for u in su if datetime.date.fromisoformat(u['signup_date'])+datetime.timedelta(days=wk*7+6)<=end]
        cnt=sum(wk in active.get(u['user_id'],set()) for u in eligible)
        row['retention'].append(round(100*cnt/len(eligible),1) if eligible else None)
    cohorts[week]=row
out={'datasetName':'BNPL Funnel & Retention Synthetic Dataset v1','synthetic':True,'generatedFor':'Portfolio demonstration only','period':'2026-01-01 to 2026-09-30','visitorCount':len(users),'eventCount':len(events),'signups':overall['signups'],'devices':['All','Android','iOS','Desktop'],'regions':['All','North','South','West','East','Central'],'funnelEvents':funnel,'funnelLabels':labels,'overall':overall,'segments':segments,'cohorts':cohorts,'largestDrop':{'from':labels[drop-1],'to':labels[drop],'drop_pp':round(rates[drop-1]-rates[drop],1),'from_rate':rates[drop-1],'to_rate':rates[drop]},'methodNote':'All records are synthetic and generated with programmed conversion and retention probabilities. They are not real customer activity or findings about an actual BNPL product.'}
(ROOT/'dashboard_data.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(f"Wrote dashboard_data.json for {len(users)} visitors and {len(events)} events")

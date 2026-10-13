from pathlib import Path
import csv, sqlite3
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent
DB=HERE/'funnel_retention.db'
if DB.exists(): DB.unlink()
con=sqlite3.connect(DB)
con.executescript((HERE/'schema.sql').read_text(encoding='utf-8'))
for name, cols in [('users',['user_id','first_seen_date','signup_date','signup_week','device','region','acquisition_channel']),('events',['event_id','user_id','event_name','event_ts','week_since_signup'])]:
    source=PROJECT/'data'/f'{name}.csv'
    with source.open(newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f); rows=[]
        for r in reader:
            vals=[r[c] if r[c] != '' else None for c in cols]
            if name=='events' and vals[-1] is not None: vals[-1]=int(vals[-1])
            rows.append(tuple(vals))
    placeholders=','.join('?' for _ in cols)
    con.executemany(f"INSERT INTO {name} ({','.join(cols)}) VALUES ({placeholders})",rows)
con.commit()
import re
for query_file in ['funnel_analysis.sql','retention_analysis.sql']:
    sql=(HERE/query_file).read_text(encoding='utf-8')
    print('\n##',query_file)
    # Strip full-line SQL comments before splitting; queries may begin with comments.
    sql=re.sub(r'(?m)^\s*--.*$', '', sql)
    for statement in [part.strip() for part in sql.split(';') if part.strip()]:
        if statement.upper().startswith(('SELECT','WITH')):
            try:
                cur=con.execute(statement)
                if cur.description:
                    print([d[0] for d in cur.description])
                    for row in cur.fetchmany(10): print(row)
            except sqlite3.Error as ex:
                print('SQL error:',ex)
print('\nDatabase created at',DB)
con.close()

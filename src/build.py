"""Build BGG 'US Power Outage Burden by State' from raw EIA-861 and DOE-417 files in raw/."""
import pandas as pd, numpy as np, re, glob, os, json, warnings
warnings.filterwarnings('ignore')
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R=B+'/raw'
STATES={'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas','CA':'California','CO':'Colorado','CT':'Connecticut','DE':'Delaware','DC':'District of Columbia','FL':'Florida','GA':'Georgia','HI':'Hawaii','ID':'Idaho','IL':'Illinois','IN':'Indiana','IA':'Iowa','KS':'Kansas','KY':'Kentucky','LA':'Louisiana','ME':'Maine','MD':'Maryland','MA':'Massachusetts','MI':'Michigan','MN':'Minnesota','MS':'Mississippi','MO':'Missouri','MT':'Montana','NE':'Nebraska','NV':'Nevada','NH':'New Hampshire','NJ':'New Jersey','NM':'New Mexico','NY':'New York','NC':'North Carolina','ND':'North Dakota','OH':'Ohio','OK':'Oklahoma','OR':'Oregon','PA':'Pennsylvania','RI':'Rhode Island','SC':'South Carolina','SD':'South Dakota','TN':'Tennessee','TX':'Texas','UT':'Utah','VT':'Vermont','VA':'Virginia','WA':'Washington','WV':'West Virginia','WI':'Wisconsin','WY':'Wyoming','PR':'Puerto Rico'}
def num(v):
    if v is None or (isinstance(v,float) and np.isnan(v)): return np.nan
    s=str(v).replace(',','').strip()
    try: return float(s)
    except: return np.nan
# ---------- EIA-861 reliability ----------
util=[]
for f in sorted(glob.glob(R+'/rel/Reliability_*.xlsx')):
    y=int(re.search(r'(\d{4})',f).group(1))
    d=pd.read_excel(f,sheet_name='Reliability_States',header=None)
    off=1 if d.shape[1]==29 else 0
    hdr=d.iloc[:4].astype(str)
    assert hdr[5+off].str.contains('SAIDI').any() and hdr[17+off].str.contains('SAIDI').any() and hdr[14+off].str.contains('Customers').any() and hdr[23+off].str.contains('Customers').any(), y
    d=d[pd.to_numeric(d[0],errors='coerce')==y]
    d=pd.concat([d.iloc[:,:5],d.iloc[:,5+off:].set_axis(range(5,d.shape[1]-off),axis=1)],axis=1)
    for _,r in d.iterrows():
        util.append(dict(year=y,utility_id=r[1],utility_name=r[2],state=r[3],ownership=r[4],
          ieee_saidi_med=num(r[5]),ieee_saifi_med=num(r[6]),ieee_saidi_nomed=num(r[8]),ieee_saifi_nomed=num(r[9]),ieee_customers=num(r[14]),
          oth_saidi_med=num(r[17]),oth_saifi_med=num(r[18]),oth_saidi_nomed=num(r[20]),oth_saifi_nomed=num(r[21]),oth_customers=num(r[23])))
U=pd.DataFrame(util)
# choose standard per utility-state-year: IEEE 1366 if IEEE customers & SAIDI-with-MED reported, else Other
ie=U.ieee_customers.gt(0)&U.ieee_saidi_med.notna()
ot=~ie&U.oth_customers.gt(0)&U.oth_saidi_med.notna()
U['standard_used']=np.where(ie,'IEEE',np.where(ot,'Other',''))
for m in ['saidi_med','saifi_med','saidi_nomed','saifi_nomed','customers']:
    U[m]=np.where(ie,U['ieee_'+m],np.where(ot,U['oth_'+m],np.nan))
U.to_csv(B+'/eia861-utility-reliability-2013-2025.csv',index=False,
  columns=['year','state','utility_id','utility_name','ownership','standard_used','customers','saidi_med','saifi_med','saidi_nomed','saifi_nomed','ieee_customers','ieee_saidi_med','ieee_saifi_med','ieee_saidi_nomed','ieee_saifi_nomed','oth_customers','oth_saidi_med','oth_saifi_med','oth_saidi_nomed','oth_saifi_nomed'])
rows=[]
for (y,s),g in U[U.standard_used!=''].groupby(['year','state']):
    o=dict(year=y,state=s,state_name=STATES.get(s,''),utilities_reporting=len(g),utilities_ieee=int((g.standard_used=='IEEE').sum()),customers_covered=int(g.customers.sum()))
    for m in ['saidi_med','saifi_med','saidi_nomed','saifi_nomed']:
        k=g[g[m].notna()]
        o[m]=round(float((k[m]*k.customers).sum()/k.customers.sum()),3) if len(k) and k.customers.sum()>0 else np.nan
        o['customers_'+m]=int(k.customers.sum())
    b=g[g.saidi_med.notna()&g.saidi_nomed.notna()]
    wm=(b.saidi_med*b.customers).sum()/b.customers.sum() if b.customers.sum()>0 else np.nan
    wn=(b.saidi_nomed*b.customers).sum()/b.customers.sum() if b.customers.sum()>0 else np.nan
    o['med_share_of_saidi_pct']=round(100*(wm-wn)/wm,1) if wm and wm>0 else np.nan
    o['saidi_med_hours']=round(o['saidi_med']/60,2)
    rows.append(o)
S=pd.DataFrame(rows)
S['rank_saidi_med_in_year']=S.groupby('year').saidi_med.rank(ascending=False,method='min').astype(int)
S['source']='EIA Form 861 Reliability file, '+S.year.astype(str)
S.to_csv(B+'/state-reliability-saidi-saifi-2013-2025.csv',index=False)
# national
N=[]
for y,g in U[U.standard_used!=''].groupby('year'):
    o=dict(year=y,utilities_reporting=len(g),customers_covered=int(g.customers.sum()))
    for m in ['saidi_med','saifi_med','saidi_nomed','saifi_nomed']:
        k=g[g[m].notna()]; o[m]=round(float((k[m]*k.customers).sum()/k.customers.sum()),3)
    N.append(o)
pd.DataFrame(N).to_csv(B+'/national-reliability-2013-2025.csv',index=False)
# validation vs EIA State Totals (any standard) where file has it
val=[]
for f in sorted(glob.glob(R+'/rel/Reliability_*.xlsx')):
    y=int(re.search(r'(\d{4})',f).group(1))
    try: t=pd.read_excel(f,sheet_name='State Totals',header=None)
    except Exception: continue
    t=t[pd.to_numeric(t[0],errors='coerce')==y]
    for _,r in t.iterrows():
        m=S[(S.year==y)&(S.state==r[1])]
        if len(m): val.append(dict(year=y,state=r[1],eia_any_customers=num(r[12]),our_customers=m.customers_covered.iloc[0],eia_any_saidi_med=num(r[13]),our_saidi_med=m.saidi_med.iloc[0],eia_any_saidi_nomed=num(r[16]),our_saidi_nomed=m.saidi_nomed.iloc[0]))
pd.DataFrame(val).to_csv(B+'/validation-vs-eia-state-totals.csv',index=False)
# ---------- DOE-417 ----------
KEYS=sorted([('connecicut','CT')]+[(re.sub(r'[^a-z]','',v.lower()),k) for k,v in STATES.items()],key=lambda x:-len(x[0]))
def states_in(t):
    s=re.sub(r'[^a-z]','',str(t).lower()); found=[]
    for nm,ab in KEYS:
        if nm in s: found.append(ab); s=s.replace(nm,'|')
    return sorted(set(found))
ev=[];unmatched=[]
for f in sorted(glob.glob(R+'/oe417/*')):
    y=int(os.path.basename(f)[:4])
    d=pd.read_excel(f,header=None)
    hdr=d.index[d.apply(lambda r: r.astype(str).str.contains('Area Affected').any(),axis=1)][0]
    cols=[str(c).strip() for c in d.loc[hdr]]
    d=d.loc[hdr+1:]; d.columns=cols
    ac=[c for c in cols if 'Area Affected' in c][0]
    tc=[c for c in cols if c=='Event Type'][0]
    cc=[c for c in cols if 'Customers' in c][0]
    mc=[c for c in cols if 'Demand Loss' in c][0]
    dc=[c for c in cols if 'Date' in c and 'Began' in c][0]
    d=d[d[ac].notna()]
    for _,r in d.iterrows():
        st=states_in(r[ac])
        if not st: unmatched.append(dict(year=y,area_affected=r[ac],event_type=r[tc]))
        ev.append(dict(year=y,date_began=str(r[dc])[:10],area_affected=str(r[ac]).strip(),states=';'.join(st),n_states=len(st),event_type=str(r[tc]).strip(),demand_loss_mw=num(r[mc]),customers_affected=num(r[cc]),customers_affected_raw=r[cc],source_file=os.path.basename(f)))
E=pd.DataFrame(ev)
E.to_csv(B+'/doe417-events-2013-2025.csv',index=False)
pd.DataFrame(unmatched).to_csv(B+'/doe417-unmatched-areas.csv',index=False)
W=E.event_type.str.contains('weather|storm|hurricane|tornado|natural disaster|wildfire|fire|ice|heat|wind|flood|earthquake',case=False)
E['weather']=W
rows=[]
for y in sorted(E.year.unique()):
    for ab in STATES:
        g=E[(E.year==y)&E.states.str.split(';').apply(lambda l: ab in l)]
        one=g[g.n_states==1]
        rows.append(dict(year=y,state=ab,state_name=STATES[ab],events_total=len(g),events_weather=int(g.weather.sum()),events_single_state=len(one),events_multi_state=len(g)-len(one),
          events_customers_reported=int(one.customers_affected.notna().sum()),customers_affected_single_state_sum=int(one.customers_affected.sum()) if one.customers_affected.notna().any() else 0,
          max_customers_single_event=float(g.customers_affected.max()) if g.customers_affected.notna().any() else np.nan))
pd.DataFrame(rows).to_csv(B+'/state-doe417-event-summary-2013-2025.csv',index=False)
print(len(U),len(S),len(E),len(unmatched),len(rows))

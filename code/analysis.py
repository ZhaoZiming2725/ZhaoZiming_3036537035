"""Card-Krueger replication. Definitions follow the author public codebook/check.sas."""
from pathlib import Path
import json
import hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from scipy import stats

ROOT=Path(__file__).resolve().parents[1]
TAB=ROOT/'outputs/tables'; FIG=ROOT/'outputs/figures'
for d in [TAB,FIG,ROOT/'data/processed']: d.mkdir(parents=True,exist_ok=True)

def load():
    d=pd.read_csv(ROOT/'data/raw/public.csv')
    assert len(d)==410 and d.groupby('STATE').size().to_dict()=={0:79,1:331}
    assert not d.duplicated(['STATE','SHEET']).any() # SHEET alone repeats across states.
    d['store_id']=d.STATE.astype(str)+'_'+d.SHEET.astype(str)
    d['fte1']=d.EMPFT+.5*d.EMPPT+d.NMGRS
    d['fte2']=d.EMPFT2+.5*d.EMPPT2+d.NMGRS2
    d.loc[d.STATUS2==3,'fte2']=0 # Six permanent closures only.
    d.loc[d.STATUS2.isin([0,2,4,5]),'fte2']=np.nan
    d['dfte']=d.fte2-d.fte1
    d['gap']=np.where(d.STATE==0,0,((5.05-d.WAGE_ST)/d.WAGE_ST).clip(lower=0))
    d['regression_sample']=d.dfte.notna() & ((d.STATUS2==3)|(d.WAGE_ST.notna()&d.WAGE_ST2.notna()))
    assert d.dfte.notna().sum()==384 and d.regression_sample.sum()==357
    return d

def dataset():
    d=load();d[['store_id','STATE','CHAIN','CO_OWNED','STATUS2','fte1','fte2','dfte','gap','regression_sample']].to_csv(ROOT/'data/processed/analysis_all.csv',index=False)
    d.loc[d.dfte.notna(),['store_id','STATE','CHAIN','CO_OWNED','STATUS2','fte1','fte2','dfte','gap','regression_sample']].to_csv(ROOT/'data/processed/analysis_panel.csv',index=False)
    audit={'raw_stores':len(d),'NJ':331,'PA':79,'permanent_closures':int((d.STATUS2==3).sum()),'temporary_closures':int(d.STATUS2.isin([2,4,5]).sum()),'refusals':int((d.STATUS2==0).sum()),'missing_fte1':int(d.fte1.isna().sum()),'missing_fte2':int(d.fte2.isna().sum()),'balanced':int(d.dfte.notna().sum()),'table4':int(d.regression_sample.sum()),'raw_sha256':hashlib.sha256((ROOT/'data/raw/public.csv').read_bytes()).hexdigest()}
    (ROOT/'outputs/validation.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(audit)

def mean_se(s):
    s=s.dropna();return s.mean(),s.std(ddof=1)/np.sqrt(len(s)),len(s)

def table2():
    d=load();variables=[]
    for chain,name in [(1,'Burger King (%)'),(2,'KFC (%)'),(3,'Roy Rogers (%)'),(4,"Wendy's (%)")]: variables.append(('Store types',name,100*(d.CHAIN==chain)))
    variables.append(('Store types','Company-owned (%)',100*d.CO_OWNED))
    for wave,suffix in [(1,''),(2,'2')]:
        fte=d[f'fte{wave}'];w=d['WAGE_ST'+suffix]
        pct=100*d['EMPFT'+suffix]/fte.where(fte>0)
        meal=d['PSODA'+suffix]+d['PFRY'+suffix]+d['PENTREE'+suffix]
        v=[('FTE employment',fte),('Full-time employees (%)',pct),('Starting wage ($/hour)',w),('Wage = $4.25 (%)',100*w.eq(4.25))]
        if wave==2:v.append(('Wage = $5.05 (%)',100*w.eq(5.05)))
        v += [('Full meal price ($)',meal),('Hours open (weekday)',d['HRSOPEN'+suffix]),('Recruiting program (%)',100*d['BONUS' if wave==1 else 'SPECIAL2'])]
        variables.extend([(f'Wave {wave}',label,s) for label,s in v])
    rows=[]
    for section,label,s in variables:
        nj,njse,nnj=mean_se(s[d.STATE==1]);pa,pase,npa=mean_se(s[d.STATE==0]);t=(nj-pa)/np.hypot(njse,pase)
        rows.append(dict(Section=section,Variable=label,NJ=nj,NJ_SE=njse,NJ_n=nnj,PA=pa,PA_SE=pase,PA_n=npa,t_NJ_PA=t))
    out=pd.DataFrame(rows)
    out.to_csv(TAB/'table2_means_all_variables.csv',index=False)
    # Published Table 2 point estimates, in row order. Kept separately from calculations.
    paper_nj=[41.1,20.5,24.8,13.6,34.1,20.4,32.8,4.61,30.5,3.35,14.4,23.6,21.0,35.9,5.08,0.0,85.2,3.41,14.4,20.3]
    paper_pa=[44.3,15.2,21.5,19.0,35.4,23.3,35.0,4.63,32.9,3.04,14.5,29.1,21.2,30.4,4.62,25.3,1.3,3.03,14.7,23.4]
    out['Paper_NJ']=paper_nj;out['Paper_PA']=paper_pa
    out['Difference_NJ']=out.NJ-out.Paper_NJ;out['Difference_PA']=out.PA-out.Paper_PA
    out.to_csv(TAB/'table2_comparison.csv',index=False)

def table3():
    d=load();groups={'PA':d.STATE==0,'NJ':d.STATE==1,'NJ low ($4.25)':(d.STATE==1)&d.WAGE_ST.eq(4.25),'NJ middle ($4.26-$4.99)':(d.STATE==1)&d.WAGE_ST.gt(4.25)&d.WAGE_ST.lt(5),'NJ high (>= $5)':(d.STATE==1)&d.WAGE_ST.ge(5)}
    temp=d.fte2.copy();temp.loc[d.STATUS2.isin([2,4,5])]=0
    measures={'1. Before (all available)':d.fte1,'2. After (all available)':d.fte2,'4. Change (balanced)':d.dfte,'5. Change (temporary closures=0)':temp-d.fte1}
    rows=[]
    for label,s in measures.items():
        vals={}
        for name,mask in groups.items():
            m,se,n=mean_se(s[mask]);vals[name]=(m,se,n);rows.append(dict(Row=label,Group=name,Estimate=m,SE=se,n=n))
        for name,a,b in [('NJ-PA','NJ','PA'),('NJ low-high','NJ low ($4.25)','NJ high (>= $5)'),('NJ middle-high','NJ middle ($4.26-$4.99)','NJ high (>= $5)')]:
            rows.append(dict(Row=label,Group=name,Estimate=vals[a][0]-vals[b][0],SE=np.hypot(vals[a][1],vals[b][1]),n=np.nan))
    # Row 3 has different wave samples. Do not reuse the paired-change SE.
    for name in [*groups,'NJ-PA','NJ low-high','NJ middle-high']:
        before=next(r for r in rows if r['Row'].startswith('1.') and r['Group']==name)
        after=next(r for r in rows if r['Row'].startswith('2.') and r['Group']==name)
        paired=next(r for r in rows if r['Row'].startswith('4.') and r['Group']==name)
        rows.append(dict(Row='3. Difference of available means',Group=name,Estimate=after['Estimate']-before['Estimate'],SE=np.nan,n=np.nan))
    out=pd.DataFrame(rows).sort_values(['Row','Group']);out.to_csv(TAB/'table3_means.csv',index=False)
    assert abs(out.query("Row == '4. Change (balanced)' and Group == 'NJ-PA'").Estimate.iloc[0]-2.75)<1e-9
    assert abs(out.query("Row == '5. Change (temporary closures=0)' and Group == 'NJ-PA'").Estimate.iloc[0]-2.51)<.01
    # Published targets transcribed from Table 3, AER p.780.
    benchmarks={'PA':[23.33,21.17,-2.16,-2.28,-2.28],'NJ':[20.44,21.03,.59,.47,.23],'NJ-PA':[-2.89,-.14,2.76,2.75,2.51],'NJ low ($4.25)':[19.56,20.88,1.32,1.21,.90],'NJ middle ($4.26-$4.99)':[20.08,20.96,.87,.71,.49],'NJ high (>= $5)':[22.25,20.21,-2.04,-2.16,-2.39],'NJ low-high':[-2.69,.67,3.36,3.36,3.29],'NJ middle-high':[-2.17,.75,2.91,2.87,2.88]}
    comp=[]
    for row in out.to_dict('records'):
        target=benchmarks[row['Group']][int(row['Row'][0])-1]
        comp.append({**row,'Paper':target,'Difference':row['Estimate']-target})
    pd.DataFrame(comp).to_csv(TAB/'table3_comparison.csv',index=False)

def table4():
    d=load();q=d[d.regression_sample].copy()
    controls='C(CHAIN)+CO_OWNED'
    # Column v follows author check.sas: ownership excluded despite printed table label.
    specs=[('i','dfte~STATE','STATE',2.33,1.19),('ii',f'dfte~STATE+{controls}','STATE',2.30,1.20),('iii','dfte~gap','gap',15.65,6.08),('iv',f'dfte~gap+{controls}','gap',14.92,6.21),('v','dfte~gap+C(CHAIN)+CENTRALJ+SOUTHJ+PA1+PA2','gap',11.91,7.39)]
    rows=[]
    for label,formula,key,ref,refse in specs:
        m=smf.ols(formula,q).fit();assert np.linalg.matrix_rank(m.model.exog)==m.model.exog.shape[1]
        hc=m.get_robustcov_results(cov_type='HC3');j=m.model.exog_names.index(key)
        nuisance=[n for n in m.params.index if n not in ['Intercept',key]]
        fp=float(m.f_test(', '.join(n+'=0' for n in nuisance)).pvalue) if nuisance else np.nan
        rows.append(dict(Model=label,Regressor=key,Estimate=m.params[key],OLS_SE=m.bse[key],HC3_SE=hc.bse[j],Paper=ref,Paper_SE=refse,n=int(m.nobs),Residual_SE=np.sqrt(m.mse_resid),Controls_F_p=fp,Formula=formula))
        assert abs(m.params[key]-ref)<.006 and abs(m.bse[key]-refse)<.006
    pd.DataFrame(rows).to_csv(TAB/'table4_did_regression.csv',index=False)
    # Transparent sensitivity to printed-table ownership label.
    m=smf.ols('dfte~gap+C(CHAIN)+CO_OWNED+CENTRALJ+SOUTHJ+PA1+PA2',q).fit()
    pd.DataFrame([dict(Specification='v plus ownership (printed-table label)',Estimate=m.params['gap'],SE=m.bse['gap'],n=int(m.nobs))]).to_csv(TAB/'table4_ownership_sensitivity.csv',index=False)

def figure1():
    d=load();fig,axes=plt.subplots(2,1,figsize=(10,8));rows=[]
    # Paper-style upper-bound labels: 4.25, 4.35, ..., 5.55; final bin absorbs upper tail.
    bounds=np.round(np.arange(4.25,5.56,.1),2);labels=[f'{b:.2f}' for b in bounds];labels[-1]='5.55+'
    for wave,ax in enumerate(axes,1):
        for state,name,color,shift in [(1,'New Jersey','#245777',-.19),(0,'Pennsylvania','#aab9c6',.19)]:
            w=d.loc[d.STATE==state,'WAGE_ST'+('' if wave==1 else '2')].dropna()
            bins=np.minimum(np.searchsorted(bounds,w.to_numpy()-1e-8,side='left'),len(bounds)-1)
            counts=np.bincount(bins,minlength=len(bounds));pct=counts/len(w)*100
            assert abs(pct.sum()-100)<1e-8
            ax.bar(np.arange(len(bounds))+shift,pct,.38,label=f'{name} (n={len(w)})',color=color)
            rows.extend([dict(Wave=wave,State=name,Bin=label,Percent=p,Count=int(c),n=len(w)) for label,p,c in zip(labels,pct,counts)])
        ax.set(title='Before: February-March 1992' if wave==1 else 'After: November-December 1992',ylabel='Percent of stores',xticks=np.arange(len(bounds)),xticklabels=labels);ax.legend();ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    axes[-1].set_xlabel('Starting wage ($/hour); bins end at label, final bin includes upper tail')
    fig.suptitle('Figure 1 replication: Distribution of starting wage rates');fig.tight_layout();fig.savefig(FIG/'figure1_wage_distribution.png',dpi=180);plt.close(fig)
    pd.DataFrame(rows).to_csv(TAB/'figure1_wage_bins.csv',index=False)

def extension():
    """New question: does ownership moderate the state employment contrast?"""
    d=load();q=d[d.regression_sample].copy()
    m=smf.ols('dfte~STATE*CO_OWNED+C(CHAIN)',q).fit(cov_type='HC3',use_t=True)
    assert np.linalg.matrix_rank(m.model.exog)==m.model.exog.shape[1]
    rows=[]
    for label,contrast in [('Franchise NJ-PA','STATE'),('Company-owned NJ-PA','STATE+STATE:CO_OWNED'),('Ownership difference in DID','STATE:CO_OWNED')]:
        t=m.t_test(contrast);ci=t.conf_int()[0]
        rows.append(dict(Contrast=label,Estimate=float(np.asarray(t.effect).item()),HC3_SE=float(np.asarray(t.sd).item()),CI_low=ci[0],CI_high=ci[1],p=float(t.pvalue),n=int(m.nobs)))
    out=pd.DataFrame(rows);out.to_csv(TAB/'table_extension_ownership.csv',index=False)
    q.groupby(['STATE','CO_OWNED']).dfte.agg(['mean','count','std']).to_csv(TAB/'extension_group_audit.csv')
    # Sensitivity to the wider employment-only sample (no wage-data restriction needed).
    wide=d[d.dfte.notna()].copy();w=smf.ols('dfte~STATE*CO_OWNED+C(CHAIN)',wide).fit(cov_type='HC3',use_t=True)
    ci=w.conf_int().loc['STATE:CO_OWNED'];pd.DataFrame([dict(Contrast='Ownership interaction, employment-only sample',Estimate=w.params['STATE:CO_OWNED'],HC3_SE=w.bse['STATE:CO_OWNED'],CI_low=ci[0],CI_high=ci[1],p=w.pvalues['STATE:CO_OWNED'],n=int(w.nobs))]).to_csv(TAB/'extension_sample_sensitivity.csv',index=False)
    fig,ax=plt.subplots(figsize=(8,4));ax.errorbar(out.Estimate,np.arange(3),xerr=[out.Estimate-out.CI_low,out.CI_high-out.Estimate],fmt='o',color='#245777',capsize=5);ax.set_yticks(np.arange(3),out.Contrast);ax.axvline(0,color='gray',linestyle='--');ax.set_xlabel('FTE change contrast; 95% HC3 confidence interval');ax.set_title('Extension: Employment contrasts by ownership');fig.tight_layout();fig.savefig(FIG/'fig_extension_ownership.png',dpi=180);plt.close(fig)
    print(out.to_string(index=False))

if __name__=='__main__':
    dataset();table2();table3();table4();figure1();extension()

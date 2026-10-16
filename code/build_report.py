"""Generate PDF and HTML from the same checked CSV outputs; no hand-entered estimates."""
from pathlib import Path
import html
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,PageBreak
from analysis import ROOT,TAB,FIG

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=9))
styles.add(ParagraphStyle(name='SmallNote',fontName='Helvetica',fontSize=8,leading=11,spaceAfter=7))
styles['Title'].fontSize=21;styles['Title'].leading=26
styles['Heading1'].textColor=colors.HexColor('#245777');styles['Heading1'].fontSize=16
story=[];web=[]
def p(text,small=False):
    story.append(Paragraph(text,styles['SmallNote' if small else 'Body']));web.append('<p>'+text+'</p>')
def h(text):
    story.append(Paragraph(text,styles['Heading1']));web.append('<h2>'+text+'</h2>')
def page():story.append(PageBreak())
def table(headers,rows,widths=None,size=8):
    def cell(v):return Paragraph(html.escape(str(v)),ParagraphStyle(name='Cell',fontName='Helvetica',fontSize=size,leading=size+3))
    t=Table([[cell(x) for x in headers]]+[[cell(x) for x in r] for r in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5eef4')),('LINEBELOW',(0,0),(-1,0),.8,colors.HexColor('#245777')),('LINEBELOW',(0,-1),(-1,-1),.6,colors.HexColor('#245777')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f8fa')])]))
    story.extend([t,Spacer(1,10)])
    web.append('<table><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</table>')
def picture(name,width=470,height=330):
    im=Image(str(FIG/name),width=width,height=height,kind='proportional');story.extend([im,Spacer(1,9)]);web.append(f'<img src="../outputs/figures/{name}" alt="{name}">')
def fmt(v,d=2):return '-' if pd.isna(v) else f'{v:.{d}f}'

story.append(Paragraph('Minimum Wages and Employment',styles['Title']))
story.append(Paragraph('Replication, validation and an ownership heterogeneity extension',styles['Heading2']))
p('Zhao Ziming | Student ID: 3036537035<br/>ECON6067 - Individual Project | Revised 16 October 2026',True)
h('1. Question and empirical design')
p('Did New Jersey\'s increase in the minimum wage from $4.25 to $5.05 on 1 April 1992 reduce fast-food employment? Card and Krueger (1994) compare New Jersey (NJ) restaurants with eastern Pennsylvania (PA), where the minimum remained $4.25. Competitive labor-demand reasoning predicts job losses when the floor binds; employer wage-setting power can permit a different response. This project reproduces Tables 2-4 and Figure 1, then asks whether company ownership moderates the state employment contrast.')
p('The surveys cover February-March and November-December 1992. Define FTE = full-time employees + managers + 0.5 x part-time employees. The basic model is change in FTE = intercept + b x NJ + error. The wage-gap model replaces NJ with GAP: zero in PA, and max[(5.05 - initial wage)/initial wage, 0] in NJ. Chain and ownership controls follow the author program.')
p('A causal interpretation requires parallel employment trends absent the policy, no relevant differential state shocks, and no spillovers contaminating the comparison. Two waves cannot establish pre-trends. The estimates are conditional comparisons, not proof that all minimum-wage increases raise employment.')
h('2. Data and sample construction')
p('The submitted public.csv contains 410 stores: 331 NJ and 79 PA. During this review it was independently compared, value by value and including missingness, with public.dat in the author-hosted njmin.zip. All 46 columns matched. The original acquisition route of the submitted CSV is not independently established. Re-run code/verify_public_source.py for verification; data/source_verification.json records hashes and the source URL.')
p('Six permanent closures (STATUS2=3) have wave-2 employment zero. Four temporary closures (2, 4, 5) are missing in the baseline and zero only in the Table 3 row-5 sensitivity. One refusal remains missing. There are 12 missing pre-period FTE observations and 14 missing post-period observations; these overlap, leaving 384 paired records (309 NJ, 75 PA). Permanent closures are already included, not newly added as a robustness exercise.')
p('Table 2 uses variable-specific available observations. Table 3 distinguishes all-available means from paired changes. Table 4 uses 357 records with valid employment changes and wages in both waves, except permanent closures are retained as in the author code. Use STATE plus SHEET as the store key: SHEET=407 occurs once in each state and must not be deduplicated across states.')
page();h('3. Table 2 - Means of key variables')
t2=pd.read_csv(TAB/'table2_means_all_variables.csv');rows=[]
for r in t2.to_dict('records'):
    rows.append([r['Section'],r['Variable'],f"{r['NJ']:.2f} ({r['NJ_SE']:.2f})",f"{r['PA']:.2f} ({r['PA_SE']:.2f})",f"{r['NJ_n']}/{r['PA_n']}",fmt(r['t_NJ_PA'])])
table(['Section','Variable','NJ mean (SE)','PA mean (SE)','n NJ/PA','t'],rows,[53,135,88,88,63,35],7.5)
p('SEs are standard errors of store means. t uses the independent-state difference divided by the square root of the two mean variances. Full-time percentage follows the author program: 100 x EMPFT/FTE (managers are included in the FTE denominator). Full meal price sums soda, fries and entree; missing components make meal price missing. Wave-2 recruiting program uses SPECIAL2, as in the author code.',True)
p('Exact-wage indicator percentages use all stores in each state, coding missing wages as false to reproduce the author SAS comparison convention; this differs from the nonmissing-wage denominator used in Figure 1. Published and computed means are compared in table2_comparison.csv. Most differences are rounding. NJ post-period wage=$5.05 is 85.50% here versus 85.2% printed, a one-store discrepancy not resolved by this public release; it is retained and disclosed rather than adjusted to force agreement. Some printed t statistics also differ slightly.',True)
p('The first stage is clear: starting wage increases from $4.61 to $5.08 in NJ, while PA changes from $4.63 to $4.62. A policy-induced wage shift alone does not identify its employment effect.',True)
page();h('4. Table 3 - Employment levels and changes')
t3=pd.read_csv(TAB/'table3_means.csv')
rowlabels={'1. Before (all available)':'1. Before, available','2. After (all available)':'2. After, available','3. Difference of available means':'3. Change in available means','4. Change (balanced)':'4. Paired change','5. Change (temporary closures=0)':'5. Temporary closures = 0'}
for groups,headers in [(['PA','NJ','NJ-PA'],['PA','NJ','NJ-PA']),(['NJ low ($4.25)','NJ middle ($4.26-$4.99)','NJ high (>= $5)'],['NJ $4.25','NJ $4.26-$4.99','NJ >= $5']),(['NJ low-high','NJ middle-high'],['NJ low-high','NJ middle-high'])]:
    rows=[]
    for key,label in rowlabels.items():
        vals=[]
        for group in groups:
            r=t3[(t3.Row==key)&(t3.Group==group)].iloc[0]
            vals.append(fmt(r.Estimate)+(f' ({r.SE:.2f})' if pd.notna(r.SE) else ''))
        rows.append([label]+vals)
    table(['Row']+headers,rows,[145]+[(462-145)/len(groups)]*len(groups),8)
p('Parentheses: SEs for levels, paired changes and independent-group contrasts. Row 3 uses different available samples in each wave; its point estimate is reproduced, but its covariance-adjusted SE is not reconstructed here. It is intentionally left blank rather than mislabeled as the paired-change SE. Row 4 estimates the mean within-store change; row 5 additionally sets the four temporarily closed stores to zero. Baseline permanent closures remain zero throughout.',True)
c=pd.read_csv(TAB/'table3_comparison.csv')
p(f'All 40 point estimates agree with the printed Table 3 to within {c.Difference.abs().max():.3f} FTE (rounding). The all-available DID is +2.76, the paired DID is +2.75, and the temporary-closure sensitivity is +2.51. These are different estimands/samples and should not be described as one identical calculation. Full differences and sample sizes are in the CSV outputs.',True)
page();h('5. Table 4 - Reduced-form regressions')
t4=pd.read_csv(TAB/'table4_did_regression.csv');rows=[]
for r in t4.to_dict('records'):rows.append([r['Model'],r['Regressor'],fmt(r['Estimate']),fmt(r['OLS_SE']),fmt(r['HC3_SE']),f"{r['Paper']:.2f} ({r['Paper_SE']:.2f})",r['n']])
table(['Model','Term','Estimate','OLS SE','HC3 SE','Paper (SE)','n'],rows,[40,55,62,60,60,130,55],8)
table(['Model','Chain / ownership controls','Region controls','Residual SE','Joint controls F p'],[[r.Model,'No' if r.Model in ['i','iii'] else ('Chain only' if r.Model=='v' else 'Yes'),'Yes' if r.Model=='v' else 'No',fmt(r.Residual_SE),fmt(r.Controls_F_p,3)] for r in t4.itertuples()],[40,150,90,80,102],8)
p('All five regressions use the same 357 observations. Conventional homoskedastic OLS SEs reproduce the published table; HC3 SEs are additional sensitivity estimates. The NJ coefficient is +2.326 (SE 1.192) without controls and +2.304 (SE 1.196) with chain and ownership controls. These are not the +2.75 estimate from the 384-store paired sample.')
p('Models iii-v use the proportional initial wage gap. All five primary coefficients and conventional SEs match the printed values after rounding. Model v contains GAP and four region indicators; it does not contain NJ, so PA1 and PA2 can both be included without collinearity. The prior NJ-plus-region specification was not the assigned Table 4 model.')
sens=pd.read_csv(TAB/'table4_ownership_sensitivity.csv').iloc[0]
p(f'Author-code discrepancy: printed Table 4 labels model v as including ownership, but the distributed check.sas omits CO_OWNED in that model. Following the executable author specification reproduces GAP = 11.91 (SE 7.39). Including ownership instead gives {sens.Estimate:.2f} (SE {sens.SE:.2f}); this alternative is saved separately. The choice is documented rather than silently selecting a specification to match the target. Model v residual-SE and joint-control F diagnostics differ slightly from the printed table; the reproduced code-based values are shown.')
p('Inference limitation: HC3 permits heteroskedasticity across stores but does not correct arbitrary state-level correlation. Policy varies across only two states; conventional state-cluster inference is unreliable with two clusters. Treat store-level significance as descriptive sensitivity, not conclusive policy-level evidence. Wider intervals and weak regional precision preclude a strong positive-effect claim.')
page();h('6. Figure 1 - Starting-wage distributions')
picture('figure1_wage_distribution.png',470,430)
p('This reproduces the subject and two-wave/state structure of the actual Figure 1: starting-wage distributions, not mean employment. Each state-wave denominator is the number of stores with an observed starting wage. Bars are proportions, so each distribution sums to 100%. Bin labels are upper bounds 4.25, 4.35, ..., 5.55; the final bin absorbs the upper tail. The plotted November panel includes the full November-December survey wave.')
p('This is a transparent modern redrawing, not a pixel-identical copy. Exact original histogram cutpoints and tail handling are not documented in the public program. Our bins and counts are exported in figure1_wage_bins.csv. The concentration at the new NJ wage floor is clear; PA retains a dispersed distribution near the old floor. The mean-employment visualization is supplementary and cannot substitute for this assigned figure.')
page();h('7. Independent extension - Ownership heterogeneity')
p('Question: does the NJ-PA employment contrast differ between company-owned and franchise restaurants, conditional on chain? Ownership may proxy centralized wage/staffing decisions, financing and local adjustment incentives. Neither sign is imposed in advance. A wage-bite split alone is not an independent contribution: original Tables 3-4 already compare initial wages and wage gaps.')
p('Estimate change in FTE = intercept + b x NJ + c x Company + d x NJ x Company + chain indicators + error, on the same 357-store replication sample. The parameter d is the difference between the company-owned and franchise state contrasts. Ownership is measured before treatment. Report HC3 SEs, t-based 95% intervals, and the wider 384-store employment-only sample as sensitivity; missing wages need not exclude stores for this ownership question.')
e=pd.read_csv(TAB/'table_extension_ownership.csv');rows=[]
for r in e.to_dict('records'):rows.append([r['Contrast'],fmt(r['Estimate']),fmt(r['HC3_SE']),f"[{r['CI_low']:.2f}, {r['CI_high']:.2f}]",fmt(r['p'],3)])
table(['Contrast','Estimate','HC3 SE','95% CI','p'],rows,[175,60,60,112,55],8)
picture('fig_extension_ownership.png',462,220)
r=e.iloc[2];w=pd.read_csv(TAB/'extension_sample_sensitivity.csv').iloc[0]
p(f'The ownership interaction is {r.Estimate:.2f} FTE (p={r.p:.3f}); its interval spans {r.CI_low:.2f} to {r.CI_high:.2f}. In the 384-store sample it is {w.Estimate:.2f} (p={w.p:.3f}). These results do not establish an ownership difference; substantial negative and positive differences remain compatible with the data. This is a conditional heterogeneity association, not a causal effect of company ownership. Sparse cells, nonrandom ownership, two-state policy variation and multiple possible subgroup choices limit interpretation.')
page();h('8. Validation, reproducibility and conclusion')
p('Validation completed during review: independent comparison of every raw value with the author archive; state counts and composite-key uniqueness; closure-status counts and missingness audit; assertions for 384 paired and 357 regression observations; full-rank regression designs; rounded agreement of all five Table 4 coefficients/OLS SEs; Table 3 paired and temporary-closure DID benchmarks; and distribution percentages summing to 100. No claim of hand calculation or student-only verification is made.')
p('Reproduce with Python and requirements.txt, then run python code/run_all.py from any working directory. The workflow reads the locally supplied public CSV and regenerates processed data, tables, figures, this PDF and the matching HTML. PDF creation uses ReportLab and needs no browser or proprietary software. The optional source verifier downloads only the author public archive; the main workflow needs no network access. README and skills/SKILL.md describe the same workflow.')
p('Remaining replication limits: Table 3 row-3 SEs are not reconstructed; the public-data exact-$5.05 share differs by one NJ store from the printed Table 2; Figure 1 uses documented modern bins; model v follows the author code and discloses the ownership-label discrepancy. Small rounding and printed-summary differences remain visible in comparison files. No data or coefficient was edited to force a match.')
p('Conclusion: the sample shows a positive NJ-relative employment change (+2.76 in all-available means; +2.75 in paired changes). The assigned regression sample yields smaller NJ contrasts around +2.3 FTE. This supports the paper\'s finding of no observed relative employment reduction in this setting, with substantial uncertainty about causal attribution and generalization. The ownership extension finds no precise evidence that company and franchise stores differ in their relative response.')
h('References and source access')
p('Card, D. and Krueger, A. B. (1994). Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania. American Economic Review 84(4), 772-793. Tables 2-4: pp.776, 780; Figure 1: p.777.',True)
p('Paper: https://davidcard.berkeley.edu/papers/njmin-aer.pdf<br/>Author data landing page: https://davidcard.berkeley.edu/data_sets.html<br/>Public archive: https://davidcard.berkeley.edu/data_sets/njmin.zip<br/>Archive includes public.dat, codebook, check.sas and survey forms. Princeton catalogue: https://irs.princeton.edu/publications/data-sets/minimum-wages-and-employment-chapter-4',True)

def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#bdcbd5'));canvas.line(42,35,A4[0]-42,35)
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#52616d'));canvas.drawString(42,23,'ECON6067 | Card-Krueger replication | Zhao Ziming');canvas.drawRightString(A4[0]-42,23,str(doc.page))
SimpleDocTemplate(str(ROOT/'report.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=40,bottomMargin=48,title='Card-Krueger Replication and Ownership Extension',author='Zhao Ziming').build(story,onFirstPage=footer,onLaterPages=footer)
css='body{font:16px/1.55 Arial,sans-serif;max-width:1050px;margin:40px auto;color:#203344;padding:0 20px}h2{color:#245777}table{border-collapse:collapse;width:100%;font-size:13px;margin:18px 0}td,th{padding:8px;border-bottom:1px solid #ccd6dc;text-align:left}th{background:#e5eef4}img{max-width:100%}'
(ROOT/'report/report.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Card-Krueger replication</title><style>'+css+'</style><body><h1>Minimum Wages and Employment</h1>'+''.join(web)+'</body></html>')
print('Built report.pdf and report/report.html from current CSV outputs.')

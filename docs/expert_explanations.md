# Why does the NYC subway cost so much to run? What experts say, and how it fits our data

*Literature review, 26 November 2026. Scope: operating cost only (running trains, maintenance, administration). Construction and capital costs are out of scope.*

> **How to read this document.** Each claim cites a source by its `source_id` in [`sources/sources.csv`](../sources/sources.csv). The documents were read through a web tool that converts pages and PDFs to text. Quotes and page numbers come from that reading. Items marked ✔ were opened a second time and the quote and page were confirmed; the rest stay **unverified** under rule 2 of [`AGENTS.md`](../AGENTS.md) until someone checks them. No number from this document has been added to `data/observations.csv`. Section 4.1 computes new ratios from existing rows and from figures transcribed in Appendix A; they are **derived** values that are not yet in the dataset. "Our data" means the findings in [`report/report.md`](../report/report.md).

---

## Summary

1. **Nobody runs a "Transit Costs Project for operations".** The Transit Costs Project at NYU studies construction. It has one operations paper, on train crew size. The serious work on NYC operating cost comes from four places: the econometric studies of the Imperial College metro benchmarking group (CoMET), the Citizens Budget Commission (CBC), the New York State Comptroller, and the MTA's own benchmarking reports. Alon Levy's blog is the main source of international comparison with named cities.
2. **The experts agree on the main point, and so does our data: maintenance of track, stations, signals and structures is where NYC is out of line.** The MTA's own 2019 report says that without maintenance NYC's cost per car-mile is about average, and that only one CoMET metro spends more on maintenance. CBC says matching the US peer median for subway facility maintenance would save about $981M and 6,185 jobs a year. Our data finds 46% of NYC operating staff in facility maintenance.
3. **The main explanations offered are poor track access, too many staff, high benefit costs, and two-person crews.** Track work stops every time a train passes, because the system runs 24 hours a day and flagging rules are strict. Two-person crews are real but small: every estimate ($221M to $442M a year) is a minority of the gap.
4. **The MTA's "labour price" view and our "headcount" view are both right (updated 26 November 2026).** The MTA's 2023 report says NYC wages are 51% above the international average and non-wage labour costs 91% above, and that at international labour prices NYC would be 16% *cheaper* per mile than its peers. Our data shows NYC uses 1.35 to 1.7 times as many of its own staff per car-km as Tokyo and Hong Kong. A total-compensation comparison (section 4.1) shows both hold at once. Each NYC subway employee costs about **$181,000** a year in wages and benefits, against about **$108,000 to $110,000** at Tokyo Metro, Toei and Hong Kong's MTR at PPP: **1.65 to 1.7 times as much**. Benefits are the biggest part of the difference: NYC's fringe benefits equal 70% of wages, against about 30% at Tokyo Metro. So NYC's labour cost per car-km is 2.5 to 2.8 times the peers'. NYC's total cost gap is smaller (1.3 to 1.8 times) because the peers spend about twice as much per car-km on everything else, much of it contracted-out maintenance labour that does not appear in their staff counts. **If NYC paid its own staff Tokyo-level compensation, it would cost about the same per car-km as Tokyo Metro and Toei, and about 20% more than Hong Kong.** Pay and benefits, not headcount, explain most of the gap with Tokyo. This revises the report's §5 and §11.5 statement that the problem is "mainly about how many people it takes ... not about how much each is paid".
5. **Two expert findings go beyond our data.** First, the Imperial econometrics find that the age of a metro has almost no effect on cost once other factors are controlled, but frequent train failures and in-house (not contracted) maintenance do raise cost. Second, overtime and claims costs are growing much faster than inflation.

---

## 1. Who studies this seriously

| Group | Who | What data | Rigor | Main sources |
| --- | --- | --- | --- | --- |
| Imperial College Transport Strategy Centre | Daniel Graham, Richard Anderson, Ramon Brage-Ardao, Anupriya; transport econometrics | Confidential panel data for 20 to 40 metros in the CoMET and Nova benchmarking groups, which include NYC. Translog cost functions, panel methods. | **Strong** (peer reviewed). But the metros are anonymous, so no paper names NYC. | `anupriya_2020_rail_opex`, `brage_ardao_2015_train_service_costs`, `brage_ardao_2016_rolling_stock_maintenance`, `brage_ardao_2015_etc_benchmarking`, `brage_ardao_2017_thesis` |
| Citizens Budget Commission (CBC) | Business-funded fiscal watchdog in New York. Lead author Alex Armlovich (economist). | National Transit Database (NTD) benchmarks against US peer medians, job by job. | **Medium to strong.** Transparent method; advocacy for cost cuts. | `cbc_2021_track_to_fiscal_stability`, `cbc_2023_stabilized_for_now`, `cbc_2025_fix_mta_deficit` |
| NY State Comptroller (Office of the State Comptroller, OSC) | Statutory fiscal monitor of the MTA | MTA financial plans and audits | **Strong** on facts. Does not benchmark against other systems. | `osc_2018_mta_financial_outlook`, `osc_2025_mta_financial_outlook`, `osc_2026_mta_financial_outlook`, `osc_2025_audit_mta_transformation`, `osc_2025_subway_delays`, `osc_2022_existential_questions` |
| MTA's own reviews | MTA (statutory performance report), its lawyers, its Inspector General | NTD, anonymous CoMET peers, internal payroll | **Medium to strong** on data; it is a self-assessment. | `mta_2021_performance_metrics_cy2019`, `mta_2025_performance_metrics_cy2023`, `mofo_2019_mta_overtime`, `mta_oig_2021_overtime_monitoring`, `mta_2026_operating_efficiencies` |
| Transit Costs Project (NYU Marron Institute) | Eric Goldwyn, Alon Levy, Marco Chitti and others | Census of crew size on 400+ lines in 36 cities | **Medium.** Descriptive; no cost model. | `tcp_2025_train_operations` |
| Alon Levy (Pedestrian Observations blog) | Mathematician, co-lead of the Transit Costs Project | Public data from many named countries | **Medium.** Expert blog, back-of-envelope numbers, no formal model. | `levy_2019_overnight_transit`, `levy_2022_bad_benchmarking_report`, `levy_2022_systemic_investments`, `levy_2015_labor_efficiency`, `levy_2018_base_vs_peak` |
| Manhattan Institute | Connor Harris, Nicole Gelinas | NTD and MTA budgets | **Medium** (briefs) to **weak** (op-eds) | `harris_2020_five_cheap_ways`, `gelinas_2019_seven_ways` |
| US transit economics | MIT (Sarriera, Salvucci, Zhao); Scholl; Odolinski and Smith (Sweden) | NTD bus panel; contracting studies; Swedish track-maintenance tenders | **Strong**, but bus or mainline rail, not metro, and not NYC | `sarriera_2018_baumol`, `scholl_2006_contracting`, `odolinski_smith_2016_tendering` |

**Not found.** No public McKinsey report for the MTA. The 2019 AlixPartners "Transformation Plan" and the 2018 "Fast Forward" plan were not opened as primary documents; this review uses the Comptroller's audit of them instead. This search found no operating-cost analysis from the Permanent Citizens Advisory Committee (PCAC), the Regional Plan Association or the Eno Center for Transportation; the Regional Plan Association appears only as a member of the coalition that backed one-person crews.

---

## 2. Their explanations

### 2.1 Maintenance of fixed assets is the outlier (strong agreement)

- The MTA's 2019 report: compared with US peers, NYC's total cost per car-mile is "just above average", and excluding maintenance NYC is "among the most efficient". Maintenance is 57% of operating cost, against about 30% to 40% at US peers. "Only one COMET member spends more than NYCT on maintenance activities." (`mta_2021_performance_metrics_cy2019`, pp. 3–4, 9)
- The MTA's 2023 report: facility maintenance per vehicle-mile is 25% above US peers; vehicle maintenance is 11% *below* (`mta_2025_performance_metrics_cy2023`, pp. 10–11). Maintenance as a whole "is 43% of overall operating costs" (p. 9 ✔).
- CBC: subway facility maintenance is "far less productive than other transit systems". Bringing it to the US peer median would save **$981M and 6,185 positions a year by 2024** (`cbc_2021_track_to_fiscal_stability`, p. 4 and Table 1 on p. 2 ✔). CBC's productivity measure is vehicle revenue hours of service per facility-maintenance hour worked; NYC is compared with a peer median of 1.36 (p. 4, Table 2 ✔). A later CBC piece puts productivity at "44% lower than the national median" (`cbc_2025_fix_mta_deficit`).
- Manhattan Institute: NYC spends about $1.9B a year on track maintenance, "four times as much per track-mile as any heavy rail system in the U.S. outside of New York" (`harris_2020_five_cheap_ways`, p. 4).
- Levy accepts the MTA's finding that cost outside maintenance is average and that maintenance is the problem (`levy_2022_bad_benchmarking_report`).

### 2.2 Poor track access: 24/7 service and flagging rules (agreement on the fact, disagreement on how much it explains)

- The MTA says maintenance must be done "within 20-minute windows between late night trains", while peers get about 4 hours of continuous access (`mta_2021_performance_metrics_cy2019`, pp. 4, 10; repeated in `mta_2025_performance_metrics_cy2023`, p. 11).
- CBC splits the cause. Part is real: "more wear and tear than other systems because of NYCT's high-frequency and 24-hour service". Part is rules: "since a 2007 rule change, 'flaggers' are needed" even for work on inactive tracks next to an active track, and trackworkers on active overnight tracks "must cease activity at least every 20 minutes to let a train pass" (`cbc_2021_track_to_fiscal_stability`, p. 4; Appendix I, p. 10 ✔).
- Levy in 2019 blamed "the constant interruptions" of 24/7 service and flagging rules that have grown more generous over 20 years (`levy_2019_overnight_transit`). In 2022 he changed his view: Boston closes at night yet has "nearly identical maintenance cost per car-km", so 24/7 service is mainly "an excuse" (`levy_2022_bad_benchmarking_report`).
- Weekend track outages are staffed largely on overtime (`mofo_2019_mta_overtime`, p. 19).

### 2.3 Too many staff for the output (agreement among outside critics; the MTA disagrees)

- Levy: "Staffing levels in New York are very high." NYC train drivers spend "around 550 hours a year driving a revenue train", against about 900 in Berlin, because off-peak trains are infrequent. "Track maintenance productivity is extremely low" because work stops for passing trains (`levy_2022_systemic_investments`).
- The Imperial models show that, across metros, total staff hours raise cost per car-km (+4.0% for +10% staff hours) and driver productivity lowers train-service cost (−4.7% for +10%) (`brage_ardao_2015_etc_benchmarking`, slides 15 and 21).
- The MIT bus study finds near-zero labour productivity growth in US transit from 1997 to 2014, so real unit cost rises with real wages (a "Baumol" effect, but worse) (`sarriera_2018_baumol`, pp. 4, 16).

### 2.4 Two-person crews (agreement that it is real and small)

- The Transit Costs Project: "New York is almost globally unique in maintaining" two-person crews; "fewer than 6.25%" of 400+ lines surveyed use them (`tcp_2025_train_operations`, p. 1).
- CBC: a 50% cut in conductors by 2024 "would save half of total projected subway conductor spending ($221 million of $442 million)" (`cbc_2021_track_to_fiscal_stability`, p. 7 ✔). A later CBC piece says one-person operation "expansion systemwide would save $442 million annually" (`cbc_2023_stabilized_for_now` ✔). This is the primary source of the $442M figure our report quotes through Reason. Note that $442M is *total* conductor spending in the 2021 report, so the systemwide saving assumes every conductor job goes; it is an upper bound.
- The union's case is safety in tunnel emergencies, crime and "subway surfing"; it gives no cost or safety data (`news12_2025_twu_two_person`). Governor Hochul's December 2025 veto message says one-person operation "is safe" (`streetsblog_2025_12_19_opto_veto`).

### 2.5 High price of labour, especially benefits (MTA's main explanation)

- MTA 2023, which states that "all international values have been adjusted for purchasing power parity" (p. 6 ✔): "NYCT wages are 51% higher than the international average" ✔; "non-wage labor costs—such as healthcare, pensions, and social security—are 91% higher than international benchmarks" (`mta_2025_performance_metrics_cy2023`, p. 6). Unadjusted, NYC is "23% more expensive than average" per mile; after adjusting for labour prices it "would actually be 16% cheaper than the average international peer on a per-mile basis" (p. 9 ✔). The international comparison uses CoMET data for 2022 (p. 6 ✔).
- The Comptroller: "nearly two-thirds" of the MTA operating budget is personnel cost (`osc_2018_mta_financial_outlook`, p. 9). Health and welfare cost grew about 5% a year from 2016 to 2025, to $2.7B (`osc_2026_mta_financial_outlook`, p. 17).
- CBC: "MTA retirees do not contribute to their health care premiums"; represented staff pay 2% of salary. Cost-sharing and plan redesign would save $663M a year (`cbc_2021_track_to_fiscal_stability`, p. 9).

### 2.6 Overtime, vacancies and weak time-keeping

- Overtime "has become the rule rather than the exception". MTA overtime rose from $849M (2014) to $1.324B (2018), +56%, against +24% for regular pay. NYCT overtime was $899M in 2018, about 18% of wages. Causes named: vacancies, low staff availability, track outages, a 1988-era time-keeping system and "antiquated work rules" (mainly at the commuter railroads) (`mofo_2019_mta_overtime`, pp. 1, 7, 13, 17, 19).
- About 3,240 train-crew members are "not required to swipe" in and out under labour agreements (`mta_oig_2021_overtime_monitoring`, p. 8).
- The Comptroller reports record non-reimbursable overtime of about $1.2B in 2023, driven by vacancies (`osc_2026_mta_financial_outlook`, p. 15). Overtime is partly a substitute for unfilled straight-time jobs, so it is a symptom of staffing problems more than a separate cost.

### 2.7 Density and utilisation (academic finding)

- The Imperial econometrics find that "metro systems with a high density of usage are the most cost-efficient" (`anupriya_2020_rail_opex`, abstract), with strong returns to density in train service and stations (`brage_ardao_2015_train_service_costs`, abstract; `brage_ardao_2015_etc_benchmarking`, slides 18 and 21: +10% output lowers cost per unit by about 9%).
- Levy notes that NYC cars run about 86,000 km a year against about 127,000 km on the London Underground, so fixed costs are spread over less service (`levy_2018_base_vs_peak`).

### 2.8 Train failures, not age, drive rolling-stock cost (academic finding)

- In the Imperial models, more rolling-stock failures and higher required fleet availability raise maintenance cost; **fleet age and system age have almost no effect** once other factors are controlled (`brage_ardao_2016_rolling_stock_maintenance`, abstract; `brage_ardao_2015_etc_benchmarking`, slides 12, 15 and 21). Older metros do have higher *station* costs (slide 18).
- Contracting out maintenance hours lowers rolling-stock maintenance cost (−5.7% for +10% contracted hours; slide 12). Tendering Swedish track maintenance cut its cost by about 11% with no loss of quality (`odolinski_smith_2016_tendering`, abstract). Evidence from US bus contracting is mixed: savings range from none to 16% (`scholl_2006_contracting`, pp. 148–152; `sarriera_2018_baumol`, Table 2).

### 2.9 Claims and other costs the MTA does not control

- On an accrual basis, MTA claims costs "have nearly tripled from $394 million in 2023 to more than $1 billion in each of 2024 and 2025" (`osc_2026_mta_financial_outlook`, p. 18 ✔). The MTA itself names tort costs rising about 7% a year (`mta_2026_operating_efficiencies`).

### 2.10 Reform programmes that did not reform

- The Comptroller's audit of the 2019 Transformation Plan found the MTA "did not have a working plan for Transformation". Savings came mainly from removing jobs left vacant by the 2018 hiring freeze, and claimed efficiency gains were not documented (`osc_2025_audit_mta_transformation`).

---

## 3. Their recommendations

In order of how many independent sources make them:

1. **Fix track access and maintenance productivity.** Regular planned line closures (CBC's "FASTRACK-style" closures; Manhattan Institute's nightly closures with replacement buses), revised flagging rules, and barriers between tracks so crews can work next to running trains (Levy). Benchmark staffing to peer medians (CBC). Sources: `cbc_2021_track_to_fiscal_stability`, `harris_2020_five_cheap_ways`, `levy_2019_overnight_transit`, `levy_2022_systemic_investments`.
2. **Move to one-person train operation through attrition**, so no current conductor is laid off. Sources: `cbc_2021_track_to_fiscal_stability`, `cbc_2023_stabilized_for_now`, `tcp_2025_train_operations`, `levy_2022_systemic_investments`.
3. **Health-benefit cost-sharing and plan redesign.** Sources: `cbc_2021_track_to_fiscal_stability`, `gelinas_2019_seven_ways`, `osc_2026_mta_financial_outlook`.
4. **Control overtime**: modern time-keeping, fill vacancies, measure overtime cost. Sources: `mofo_2019_mta_overtime`, `mta_oig_2021_overtime_monitoring`.
5. **Run more off-peak trains** so that drivers spend more of their paid hours driving (Levy). Source: `levy_2022_systemic_investments`, `levy_2015_labor_efficiency`.
6. **Publish named benchmarks**, and report mean distance between failures and slow orders. Source: `levy_2022_bad_benchmarking_report`.
7. **Contract out or competitively tender some maintenance**, keeping some in-house work as a benchmark. Sources: Imperial models and Swedish evidence above; `sarriera_2018_baumol`.
8. **Share productivity gains with labour** in the contract, since every reform above needs collective bargaining. Sources: `cbc_2021_track_to_fiscal_stability` (p. 10), `osc_2026_mta_financial_outlook` (p. 4), `gelinas_2019_seven_ways`.

---

## 4. How the expert explanations compare with our data

| Expert explanation | Our data | Verdict |
| --- | --- | --- |
| Facility maintenance is the outlier (MTA, CBC, Manhattan Institute, Levy) | 46% of NYC operating staff are in facility maintenance; 208 facility-maintenance staff per million train-km against 44 to 142 at US peers (report §7) | **Agrees.** Strongest point of agreement. Our foreign data has no split by function, so this is still a US-only comparison. |
| Non-maintenance cost is about average (MTA 2019) | Vehicle-operations staff per train-km are within the US range (report §7) | **Agrees** for US peers. |
| 24/7 service is the cause (MTA) | Consistent with maintenance-heavy staffing; PATH also runs 24/7 and is more expensive (report §11.2) | **Agrees in direction, not tested.** Levy's Boston point and our PATH point both say 24/7 service alone is not enough. The flagging rule (CBC) is a more specific cause that our data cannot see. |
| Two-person crews cost $221M–$442M (CBC) | $442M is 24% to 28% of the gap with London and Tokyo (report §11.1) | **Agrees.** We now have the primary CBC source for $442M. Since $442M is CBC's figure for *all* conductor spending, our "at most about a quarter" is the right reading: it is an upper bound. |
| Too many staff (Levy, CBC) | 1.3× to 1.7× the staff per car-km of Tokyo, London and Hong Kong (report §5) | **Agrees**, and our data adds the international comparison that CBC lacks (CBC uses US peers only). |
| Labour *price* explains the gap; adjusted for wages NYC is 16% cheaper per mile (MTA 2023) ✔ | Total compensation per employee is 1.65× to 1.7× the peers' at PPP; at peer compensation NYC's cost per car-km would be 0.92× Tokyo Metro, 1.00× Toei and 1.22× Hong Kong (section 4.1) | **Agrees, after a total-compensation check.** The first version of this document called this a conflict, because NYC's *total cost* per employee is about the same as the peers'. That turns out to hide two offsetting differences: NYC pays each employee about 1.7 times as much, and spends about half as much per car-km on non-labour items, mainly because the peers contract out work. See section 4.1. |
| Density drives cost per unit (Imperial) | Most of NYC's per-passenger-km gap with Tokyo (about 86% EST) comes from fuller cars (report §4) | **Agrees**, and our decomposition puts a number on it for named systems. |
| Asset age has little effect; failures do (Imperial) | Age is a weak explanation on its own (report §11.4); NYC trains fail 24 to 41 times as often per car-km as Hong Kong and Singapore (report §10) | **Agrees.** The Imperial result is the econometric version of our §11.4 verdict, and gives a mechanism linking our reliability and cost findings. |
| Claims costs tripled (Comptroller) | Casualty and liability cost rose from $167M to $578M in 2024 and drove the jump in general administration (report §8) | **Agrees.** Different scope: the Comptroller's figure is MTA-wide accrued claims; ours is NYC subway only from the NTD. |
| Overtime is a large and growing cost (Morrison & Foerster, Comptroller, Empire Center) | Not measured | **Goes beyond our data.** |
| Funding mix and hard budgets | Weak as an explanation (report §11.7) | None of the sources reviewed makes this argument for operating cost. |

### 4.1 Pay versus headcount: a total-compensation comparison (added 26 November 2026)

**The question.** Hrishi asked whether the MTA's wage finding reflects total compensation (benefits, pensions, retiree health) rather than base pay, and whether our cost-per-employee figures miss it. This section rebuilds the comparison with labour cost split out.

**What the MTA measures.** The MTA report gives indices, not dollar values ("absolute values for these metrics are not reported", p. 6 ✔). It compares wages and non-wage labour costs separately: "NYCT wages are 51% higher than the international average" and "Non-wage labor costs—such as healthcare, pensions, and social security—are 91% higher than international benchmarks"; "Nearly one-third of NYCT's labor costs fall into this non-wage category, with healthcare being the largest driver" (p. 6 ✔). Chart 2 is titled "Labor cost per hour by cost type", so the comparison is probably per hour worked, but the text does not say so. Matching international wages would cut NYC's 2023 operating cost by about 19% and matching non-wage costs by about 13%; together about 32%, which puts NYC 16% below the international average per mile (pp. 6, 9). The report gives no measure of labour quantity (hours or staff per mile). It notes only that "Labor productivity explains some of the apparent NYCT cost premium", naming two-person crews (p. 8). So the MTA's adjustment holds NYC's own labour hours fixed and reprices them. Our check of that arithmetic, using NYC's NTD cost shares, gives 16% + 15% = 31%, close to the MTA's 32%.

**What our NYC figures already include.** NTD operating expense includes fringe benefits. In 2023 the NYC subway spent $2.80B on wages and paid absences and $1.95B on fringe benefits (`nyc_subway_2023_opex_type_*_ntd`), so fringe benefits equal 70% of wages, and labour is 78% of operating cost. The audited NYC Transit statements (subway and buses together) book pensions and retiree health (OPEB) on an accrual basis under GASB 68 and 75, and give the same ratio: benefits are 68% of wages in 2023. Of that, active-employee health and welfare is 24% of wages, pensions 20% and retiree health 24% (`nycta_fs_2023`, statement of revenues, expenses and changes in net position, p. 26: salaries and wages $4,484M, health and welfare $1,096M, pensions $881M, OPEB $1,087M). **So lifetime benefit costs are in our cost data, on an accrual basis.** What the report did not do was compare the *price* of labour across systems.

**Peer compensation.**

- *Tokyo Metro and Toei.* MLIT's FY2023 yardstick table splits each cost category into personnel cost (人件費) and other expense (経費) (Appendix A). Personnel cost is ¥94.6B for Tokyo Metro and ¥36.0B for Toei, 43% and 40% of the operating cost we use. Tokyo Metro's average salary was ¥7.62M for 9,551 parent-company employees (`tokyometro_yuho_fye2024`, 第1【企業の概況】5【従業員の状況】(2)). Personnel cost per employee (¥9.91M) is 1.30 times salary, so on-costs (employer social insurance, retirement benefits, welfare) add about 30%. Tokyo Metro contracts rolling-stock, track, electrical and station-facility maintenance to four group subsidiaries (same section, 4【関係会社の状況】); that labour is in "other expense", not personnel cost.
- *Hong Kong.* MTR reports "Staff costs and related expenses" of HK$6.92B for its Hong Kong transport operations in 2023, 49% of their operating expense, for 11,728 staff (`hong_kong_mtr_2023_opex_staff_costs_mtrall`, `hong_kong_mtr_2023_employees_fte_mtrall`). The staff count excludes corporate-support staff that the cost may include, so cost per employee may be slightly overstated.
- *London.* TfL's staff-cost note could not be read. London Underground staff are in a final-salary pension scheme with an employer rate of 27.3% of pensionable pay (`tfl_pension_fund_review_2023`, p. 12), on top of employer National Insurance. No per-employee figure is computed.

**Results, 2023, 2024 US dollars at PPP.** All values are **derived** from the rows named. NYC: NTD, 26,884 operating employees, 553.3M car-km. Peers: inputs above; PPP conversion as for the existing rows.

| | NYC subway | Tokyo Metro | Toei | Hong Kong MTR |
| --- | --- | --- | --- | --- |
| Wages and benefits per employee | $180,900 | $108,300 | $109,700 | $109,400 |
| NYC ÷ peer | | 1.67× | 1.65× | 1.65× |
| Labour share of operating cost | 78% | 43% | 40% | 49% |
| Total operating cost per employee | $230,700 | $253,000 | $272,800 | $224,100 |
| Labour cost per car-km | $8.79 | $3.57 | $3.11 | $3.10 EST |
| Non-labour cost per car-km | $2.42 | $4.77 | $4.62 | $3.26 EST |
| Own staff per million car-km | 48.6 | 33.0 | 28.3 | 28.4 EST |
| Total cost per car-km | $11.21 | $8.34 | $7.72 | $6.36 EST |
| **NYC cost per car-km at this peer's compensation** | | **$7.68 (0.92×)** | **$7.75 (1.00×)** | **$7.73 (1.22×) EST** |

EST: Hong Kong's per-car-km values use the existing estimated heavy-rail cost (`hong_kong_mtr_2023_opex_per_car_km_est`) and apply the whole-business labour share to it. Tokyo Metro uses the 9,551 parent-company employees that match the salary disclosure; with the 10,435 transport-segment employees used in the report, compensation per employee is $99,100 and the NYC ratio 1.83×.

Formulas: compensation per employee = labour cost ÷ employees. NYC labour cost = wages + paid absences + fringe benefits (NTD object classes). NYC at peer compensation = NYC labour cost per car-km ÷ (NYC ÷ peer compensation ratio) + NYC non-labour cost per car-km. This holds NYC's own staff numbers fixed, as the MTA's adjustment does.

**What this shows.**

1. **Both views hold.** NYC has more of its own staff per car-km (1.5× Tokyo Metro, 1.7× Toei and Hong Kong) *and* pays each of them about 1.65 to 1.7 times as much. Its labour cost per car-km is therefore 2.5 to 2.8 times the peers'.
2. **Peers buy labour that does not show in their staff counts.** NYC spends about half as much as Tokyo per car-km on non-labour items. Tokyo Metro contracts out most maintenance to its subsidiaries. The report's staff-per-car-km comparison therefore overstates NYC's *labour-quantity* gap against Tokyo, and the earlier "cost per employee is the same" check was hiding the pay gap.
3. **Compensation explains all of the gap with Tokyo, and about 70% of the gap with Hong Kong.** At Tokyo-level pay, NYC's cost per car-km would be about equal to Tokyo Metro's and Toei's. This agrees with the MTA's adjustment, and Hrishi's view that the MTA report should carry weight is supported.
4. **Benefits are the bigger part.** NYC's fringe benefits are 70% of wages; Tokyo Metro's on-costs are about 30%. Per employee, NYC wages (including paid absences) are $106,600 against Tokyo Metro's average salary of $83,300 at PPP (1.28×), and NYC benefits are $74,300 against about $25,000 (about 3×). Of the $72,600 compensation gap per employee with Tokyo Metro, about $49,000 (two-thirds) is benefits. The MTA names active-employee health care as the largest non-wage item. Retiree health care (24% of wages) has no counterpart at Tokyo, where health care is funded through social insurance, which is inside the 30%.
5. **High compensation is not all an MTA choice.** Some of the gap reflects the US labour market and the US system of employer-paid health care, which any US employer faces. The MTA says its wages "align with other U.S. transit agencies" (p. 6). Separating MTA-specific generosity from US-wide price levels needs a comparison with average local pay, which this document does not yet have.

**Limits.** NYC is calendar 2023; Tokyo is April 2023 to March 2024. Tokyo Metro's 人件費 is assumed to include bonuses, retirement-benefit cost and statutory welfare; no document defining it was opened. NYC staff are NTD head counts of operating employees (full- and part-time). The Tokyo personnel-cost lines were read once through a text-extraction tool; they add up exactly to the category totals already in `data/raw/asia/mlit_yardstick_tokyo.csv`, which is a strong check, but they remain unverified.

**Two numbers to reconcile.**

- *Farebox recovery.* The Comptroller gives NYCT a 52.8% farebox operating ratio for 2019 (`osc_2022_existential_questions`), against our 70% for the subway alone from the NTD. The Comptroller's figure covers all of NYCT (including buses) under the MTA's own definition. They are not in conflict, but the report should say so if it quotes either.
- *Overtime.* Totals differ by basis: about $1.2B non-reimbursable (Comptroller, 2023), about $1.4B total (Comptroller 2025 report, 2023), $1.46B from payroll records (Empire Center, 2025). Do not mix them.

---

## 5. Gaps our data could fill

1. **Foreign cost by function.** Every expert analysis of the maintenance problem compares NYC with US systems, or with anonymous CoMET peers. A named split of foreign metro cost or staff into operations, vehicle maintenance and facility maintenance would test the central claim internationally. Candidates: Tokyo Metro and Toei financial statements (by expense type), TfL's London Underground segment accounts, MTR's annual report.
2. **Wages and benefits at PPP.** Section 4.1 does this for Tokyo Metro, Toei and Hong Kong. Still open: London (TfL's staff-cost note), a 2019 comparison, adding the personnel-cost rows to `data/observations.csv`, and a comparison of each system's pay with average pay in its own country, which would separate MTA-specific generosity from US-wide labour costs.
3. **Track access hours.** A sourced table of nightly closure hours and planned weekend closures per peer would let us test the 24/7 argument directly, and Boston (nightly closures, high maintenance cost) is a useful US control.
4. **Driver productivity.** Revenue hours per driver per year (Levy's 550 vs 900) can be computed from NTD train-hours and operator counts for NYC; peers publish driver counts.
5. **Overtime as a share of NYC labour cost**, as a time series from MTA financial plans and the Comptroller's reports. The NTD does not report overtime separately.
6. **Within-NYC tests**: cost and failures on the CBTC lines (L, 7) and on one-person-operated lines (shuttles, parts of the A, G, M and 5) against other lines, which the report already names as the best causal test.

---

## 6. Caveats

- The Imperial papers (`anupriya_2020_rail_opex`, `brage_ardao_2015_train_service_costs`, `brage_ardao_2016_rolling_stock_maintenance`, `odolinski_smith_2016_tendering`) were read as abstracts only; the full texts are paywalled. The elasticities quoted come from the open conference slides (`brage_ardao_2015_etc_benchmarking`).
- `osc_2025_audit_mta_transformation` was read from its landing page, not the PDF. `osc_2025_subway_delays` was read from the press release.
- Union and advocacy sources are included to show the other side, not as evidence.
- Several sources (CBC, Manhattan Institute) argue for cost cuts. Their numbers are transparent and cite NTD, but the framing is not neutral.

---

## Appendix A. Tokyo personnel cost by category, FY2023

Source: `mlit_yardstick_fy2023`, table 地下鉄事業者, columns 東京地下鉄 (Tokyo Metro) and 東京都 (Toei); ¥ thousand; 人件費 = personnel cost, 経費 = other expense. Each row's personnel cost plus other expense equals the category total, and the totals match `data/raw/asia/mlit_yardstick_tokyo.csv` (Tokyo Metro 207,545,218; Toei 89,512,580). Unverified (read once).

| Category | Tokyo Metro 人件費 | Tokyo Metro 経費 | Toei 人件費 | Toei 経費 |
| --- | --- | --- | --- | --- |
| 線路保存費 (track maintenance) | 3,317,454 | 20,896,231 | 3,581,543 | 10,455,161 |
| 電路保存費 (electrical maintenance) | 6,281,957 | 9,773,771 | 4,043,197 | 5,587,593 |
| 車両保存費 (vehicle maintenance) | 8,682,449 | 9,903,415 | 3,420,731 | 6,116,907 |
| 運転費 (train operation) | 30,035,023 | 13,317,756 | 10,777,070 | 6,309,077 |
| 運輸費 (stations and traffic) | 31,242,908 | 35,260,769 | 11,420,771 | 19,395,239 |
| 保守管理費 (maintenance management) | 3,760,897 | 6,237,257 | 0 | 0 |
| 輸送管理費 (transport management) | 3,305,959 | 5,122,361 | 930,037 | 2,918,264 |
| 案内宣伝費 (publicity) | 0 | 922,571 | 0 | 0 |
| 厚生福利施設費 (welfare facilities) | 961,716 | 3,602,914 | 192,540 | 31,342 |
| 一般管理費 (general administration) | 7,029,017 | 7,890,793 | 1,643,696 | 2,689,412 |
| **Total** | **94,617,380** | **112,927,838** | **36,009,585** | **53,502,995** |

Track maintenance is the clearest case of contracting: at Tokyo Metro only 14% of its cost is personnel cost.

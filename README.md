# Do Behavioral Nudges Increase Clinical Trial Enrollment?
### A/B Testing with Bayesian Analysis on Real-World ClinicalTrials.gov Data

Rigorous A/B testing framework applied to 18,644 completed clinical trials, 
investigating whether behavioral nudge interventions — reminders, outreach, 
navigators, incentives — increase patient enrollment rates compared to standard 
recruitment approaches.

Combines frequentist and Bayesian methods to answer a question with direct 
implications for clinical research efficiency: **can a simple nudge meaningfully 
move the needle on trial enrollment?**

## Research Question

80% of clinical trials fail to meet enrollment targets on time, causing delays, 
cost overruns, and in some cases trial termination. Behavioral nudges — low-cost 
interventions drawn from behavioral economics — have shown promise in other 
healthcare contexts. This project tests their impact on enrollment at scale 
using observational data from ClinicalTrials.gov.

## Dataset

**Source:** [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api)  
**Trials:** 18,644 completed interventional trials with actual enrollment data  
**Treatment:** Trials with behavioral nudge interventions (n=494)  
**Control:** Standard recruitment trials (n=18,150)  
No PHI involved — all data publicly available.

## Analyses

### Notebook 1 — EDA & Power Analysis (`notebooks/01_eda.ipynb`)
- Enrollment rate distributions by phase, sponsor class, condition
- Nudge vs control baseline characteristics
- Power analysis: minimum detectable effect size

### Notebook 2 — Frequentist A/B Test (`notebooks/02_frequentist.ipynb`)
- Chi-square and t-tests for enrollment rate differences
- Multiple testing correction (Bonferroni, Benjamini-Hochberg FDR)
- Subgroup analysis: oncology vs non-oncology, phase, sponsor type

### Notebook 3 — Bayesian A/B Test (`notebooks/03_bayesian.ipynb`)
- Beta-Binomial conjugate model
- Posterior distributions and credible intervals
- Probability that nudge > control
- Comparison of frequentist vs Bayesian conclusions

### Notebook 4 — Predictive Modeling (`notebooks/04_predictive.ipynb`)
- What trial features predict meeting enrollment goals?
- Gradient boosting + SHAP feature importance
- Enrollment goal achievement as binary outcome

## Stack

- **Python, pandas** — data ingestion and processing
- **scipy, statsmodels** — frequentist hypothesis testing
- **PyMC, ArviZ** — Bayesian modeling
- **scikit-learn, SHAP** — predictive modeling
- **Matplotlib, seaborn, plotly** — visualizations
- **JupyterLab** — documented analysis notebooks

## Project Structure
```
clinical-trial-nudges/
├── data/
│   ├── raw/          # ClinicalTrials.gov JSON (not tracked in git)
│   └── processed/    # cleaned dataset (not tracked in git)
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_frequentist.ipynb
│   ├── 03_bayesian.ipynb
│   └── 04_predictive.ipynb
├── figures/          # saved plots
├── src/
│   └── ingest.py     # data ingestion pipeline
├── requirements.txt
├── .gitignore
└── README.md
```
## Setup

```bash
git clone https://github.com/KelyNorel/clinical-trial-nudges.git
cd clinical-trial-nudges
pyenv virtualenv 3.11 trial-nudges
pyenv local trial-nudges
pip install -r requirements.txt
python src/ingest.py
```

---

**Author:** Raquel (Kely) Norel, PhD  
**Domain:** Clinical Research / Behavioral Economics / A/B Testing  
**Status:** 🔄 In progress


# Analytical Specification & Business Problem

**Project:** IT Hardware Reliability Analytics  
**Role Scope:** Data Analyst / BI Analyst  

---

## 1. Primary Business Questions
1. **Model Reliability:** Which drive models and manufacturers demonstrate statistically significant higher failure rates under operational workloads?
2. **Predictive Degradation Signals:** Which S.M.A.R.T. raw attributes (e.g., Reallocated Sectors `SMART 5`, Pending Sectors `SMART 197`) serve as reliable early-warning indicators before drive failure occurs?
3. **Maintenance SLA Optimization:** How can IT infrastructure teams transition from reactive drive replacement to proactive maintenance scheduling based on empirical survival probabilities?

---

## 2. Key Analytical Hypotheses
* **H1 (Capacity Effect):** Larger capacity drives (>=14TB) exhibit higher annualized failure rates than mid-capacity enterprise drives (8-12TB) due to higher areal density.
* **H2 (SMART Warning Threshold):** A non-zero `SMART 5` (Reallocated Sectors) or `SMART 197` (Pending Sectors) count increases 30-day failure probability by >5x.
* **H3 (Age vs Exposure):** Operational exposure (power-on hours) is a stronger predictor of failure than calendar age.

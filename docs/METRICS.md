# Metric Definitions & Formula Contract

**Project:** IT Hardware Reliability Analytics  

---

## 1. Primary Reliability Metrics

### A. Operational Exposure (Drive-Days)
$$\text{Total Exposure} = \sum_{i=1}^{N} \text{Days Active}_i$$
* **Definition:** The cumulative sum of active operational days across all monitored drives within the evaluation window.

---

### B. Annualized Failure Rate (AFR)
$$\text{AFR (\%)} = \left( \frac{\text{Total Failure Events}}{\text{Total Exposure (Drive-Days)}} \right) \times 365 \times 100$$
* **Definition:** Standardized industry benchmark normalizing failures per year across heterogeneous fleet sizes.

---

### C. Failure Rate per 10,000 Drive-Days
$$\text{Failure Rate}_{10k} = \left( \frac{\text{Total Failure Events}}{\text{Total Exposure (Drive-Days)}} \right) \times 10,000$$
* **Definition:** Granular metric measuring short-term reliability per 10,000 active operational days.

---

### D. S.M.A.R.T. Anomaly Prevalence
$$\text{Anomaly Prevalence (\%)} = \left( \frac{\text{Drives with } \text{SMART}_x > 0}{\text{Total Active Drives}} \right) \times 100$$
* **Definition:** Percentage of operational fleet exhibiting early hardware degradation signals.

---

## 2. Business Decision Thresholds
* **Critical Risk Level:** $\text{AFR} > 2.5\%$ $\rightarrow$ Immediate Procurement Freeze & Targeted Replacement.
* **Warning Risk Level:** $1.5\% \le \text{AFR} \le 2.5\%$ $\rightarrow$ Standard Inspection & Priority Backup.
* **Healthy Level:** $\text{AFR} < 1.5\%$ $\rightarrow$ Normal Operations.

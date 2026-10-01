-- ====================================================================
-- SQL Script 03: Model-Level Reliability Benchmarking
-- Description: Groups drive reliability metrics by model and capacity.
--              Filters out models with < 1,000 drive-days exposure.
-- ====================================================================

SELECT 
    model,
    ROUND(MAX(capacity_bytes) / 1073741824.0 / 1024.0, 0) AS capacity_tb,
    COUNT(DISTINCT serial_number) AS active_drives,
    COUNT(*) AS drive_days_exposure,
    SUM(failure) AS failure_count,
    ROUND(((CAST(SUM(failure) AS FLOAT) / COUNT(*)) * 365) * 100, 2) AS annualized_failure_rate_pct,
    CASE 
        WHEN ((CAST(SUM(failure) AS FLOAT) / COUNT(*)) * 365) * 100 > 2.5 THEN 'CRITICAL_RISK'
        WHEN ((CAST(SUM(failure) AS FLOAT) / COUNT(*)) * 365) * 100 >= 1.5 THEN 'MODERATE_RISK'
        ELSE 'LOW_RISK'
    END AS reliability_tier
FROM backblaze_drive_stats
GROUP BY model
HAVING COUNT(*) >= 1000
ORDER BY annualized_failure_rate_pct DESC, drive_days_exposure DESC;

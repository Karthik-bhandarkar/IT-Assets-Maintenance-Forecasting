-- ====================================================================
-- SQL Script 02: Fleet Exposure & Failure Summary Query
-- Description: Aggregates total operational drive-days, failure counts,
--              and calculates fleet-wide Annualized Failure Rate (AFR).
-- ====================================================================

WITH FleetSummary AS (
    SELECT 
        COUNT(DISTINCT serial_number) AS total_unique_drives,
        COUNT(*) AS total_drive_days_exposure,
        SUM(failure) AS total_failures,
        ROUND(AVG(capacity_bytes / 1073741824.0 / 1024.0), 2) AS avg_capacity_tb
    FROM backblaze_drive_stats
)
SELECT 
    total_unique_drives,
    total_drive_days_exposure,
    total_failures,
    avg_capacity_tb,
    ROUND((CAST(total_failures AS FLOAT) / total_drive_days_exposure) * 10000, 4) AS failures_per_10k_days,
    ROUND(((CAST(total_failures AS FLOAT) / total_drive_days_exposure) * 365) * 100, 2) AS annualized_failure_rate_pct
FROM FleetSummary;

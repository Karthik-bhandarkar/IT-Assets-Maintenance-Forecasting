-- ====================================================================
-- SQL Script 04: S.M.A.R.T. Degradation Signal Correlation Query
-- Description: Analyzes failure rates of drives exhibiting elevated 
--              reallocated sectors (SMART 5) vs clean drives.
-- ====================================================================

WITH SmartBuckets AS (
    SELECT 
        serial_number,
        model,
        failure,
        CASE 
            WHEN smart_5_raw > 0 OR smart_197_raw > 0 THEN 'Elevated SMART Anomaly (SMART 5/197 > 0)'
            ELSE 'Healthy SMART Profile (SMART 5 & 197 = 0)'
        END AS smart_health_status
    FROM backblaze_drive_stats
)
SELECT 
    smart_health_status,
    COUNT(DISTINCT serial_number) AS total_drives,
    COUNT(*) AS total_drive_days,
    SUM(failure) AS total_failures,
    ROUND(((CAST(SUM(failure) AS FLOAT) / COUNT(*)) * 365) * 100, 2) AS annualized_failure_rate_pct
FROM SmartBuckets
GROUP BY smart_health_status
ORDER BY annualized_failure_rate_pct DESC;

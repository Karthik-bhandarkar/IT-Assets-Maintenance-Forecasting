-- ====================================================================
-- SQL Script 01: Schema Definition & Ingestion Table Setup
-- Description: Defines the analytical schema for Backblaze drive stats.
-- ====================================================================

CREATE TABLE IF NOT EXISTS backblaze_drive_stats (
    date DATE NOT NULL,
    serial_number VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    capacity_bytes BIGINT NOT NULL,
    failure INTEGER NOT NULL DEFAULT 0,
    smart_5_raw INTEGER,
    smart_9_raw INTEGER,
    smart_187_raw INTEGER,
    smart_197_raw INTEGER,
    smart_198_raw INTEGER,
    PRIMARY KEY (date, serial_number)
);

CREATE INDEX IF NOT EXISTS idx_model ON backblaze_drive_stats(model);
CREATE INDEX IF NOT EXISTS idx_failure ON backblaze_drive_stats(failure);
CREATE INDEX IF NOT EXISTS idx_date ON backblaze_drive_stats(date);

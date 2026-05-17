-- =============================================================================
-- SEO AUTOMATION DATABASE SCHEMA
-- PostgreSQL 15
-- =============================================================================

-- ---------------------------------------------------------------------------
-- RAW DATA (extracted from APIs)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS raw_gsc_queries (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    query TEXT NOT NULL,
    page TEXT NOT NULL,
    clicks INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    ctr DECIMAL(5,4) DEFAULT 0,
    position DECIMAL(5,2) DEFAULT 0,
    site TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, query, page, site)
);

CREATE INDEX idx_raw_gsc_date ON raw_gsc_queries(date);
CREATE INDEX idx_raw_gsc_page ON raw_gsc_queries(page);
CREATE INDEX idx_raw_gsc_query ON raw_gsc_queries(query);

CREATE TABLE IF NOT EXISTS raw_ga4_sessions (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    page TEXT NOT NULL,
    sessions INTEGER DEFAULT 0,
    users INTEGER DEFAULT 0,
    revenue DECIMAL(12,2) DEFAULT 0,
    source_medium TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, page, source_medium)
);

CREATE INDEX idx_raw_ga4_date ON raw_ga4_sessions(date);
CREATE INDEX idx_raw_ga4_page ON raw_ga4_sessions(page);

CREATE TABLE IF NOT EXISTS raw_ym_traffic (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    page TEXT NOT NULL,
    visits INTEGER DEFAULT 0,
    users INTEGER DEFAULT 0,
    bounce_rate DECIMAL(5,2) DEFAULT 0,
    source TEXT,
    search_phrase TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, page, source, search_phrase)
);

CREATE INDEX idx_raw_ym_date ON raw_ym_traffic(date);
CREATE INDEX idx_raw_ym_page ON raw_ym_traffic(page);

CREATE TABLE IF NOT EXISTS raw_yw_problems (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    host_id TEXT NOT NULL,
    problem_type TEXT NOT NULL,
    url TEXT,
    severity TEXT CHECK (severity IN ('critical', 'warning', 'info')),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_raw_yw_date ON raw_yw_problems(date);
CREATE INDEX idx_raw_yw_severity ON raw_yw_problems(severity);

-- ---------------------------------------------------------------------------
-- REFERENCE DATA
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS clusters (
    id SERIAL PRIMARY KEY,
    page TEXT NOT NULL UNIQUE,
    cluster_name TEXT NOT NULL,
    category TEXT,
    subcategory TEXT,
    priority TEXT CHECK (priority IN ('High', 'Medium', 'Low')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_clusters_name ON clusters(cluster_name);
CREATE INDEX idx_clusters_category ON clusters(category);

-- ---------------------------------------------------------------------------
-- PROCESSED DATA
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS processed_traffic (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    page TEXT NOT NULL,
    cluster_name TEXT,
    category TEXT,
    sessions INTEGER DEFAULT 0,
    users INTEGER DEFAULT 0,
    revenue DECIMAL(12,2) DEFAULT 0,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, page, source)
);

CREATE INDEX idx_proc_traffic_date ON processed_traffic(date);
CREATE INDEX idx_proc_traffic_cluster ON processed_traffic(cluster_name);

CREATE TABLE IF NOT EXISTS processed_positions (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    query TEXT NOT NULL,
    page TEXT NOT NULL,
    cluster_name TEXT,
    position DECIMAL(5,2) DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    ctr DECIMAL(5,4) DEFAULT 0,
    search_engine TEXT CHECK (search_engine IN ('google', 'yandex')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, query, page, search_engine)
);

CREATE INDEX idx_proc_pos_date ON processed_positions(date);
CREATE INDEX idx_proc_pos_cluster ON processed_positions(cluster_name);
CREATE INDEX idx_proc_pos_query ON processed_positions(query);

CREATE TABLE IF NOT EXISTS processed_visibility (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    cluster_name TEXT,
    category TEXT,
    visibility_score DECIMAL(10,4) DEFAULT 0,
    search_engine TEXT CHECK (search_engine IN ('google', 'yandex')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, cluster_name, category, search_engine)
);

CREATE INDEX idx_proc_vis_date ON processed_visibility(date);

-- ---------------------------------------------------------------------------
-- ANALYTICS
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    alert_date DATE NOT NULL,
    alert_type TEXT NOT NULL CHECK (alert_type IN (
        'traffic_drop', 'position_drop', 'ctr_drop', 
        'crawl_error', 'indexing_error', 'backlink_spike'
    )),
    severity TEXT CHECK (severity IN ('critical', 'warning', 'info')),
    message TEXT NOT NULL,
    metric_value DECIMAL(12,2),
    threshold DECIMAL(12,2),
    page TEXT,
    query TEXT,
    cluster_name TEXT,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'resolved', 'ignored'))
);

CREATE INDEX idx_alerts_date ON alerts(alert_date);
CREATE INDEX idx_alerts_type ON alerts(alert_type);
CREATE INDEX idx_alerts_status ON alerts(status);

CREATE TABLE IF NOT EXISTS weekly_tops (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    category TEXT,
    page TEXT,
    cluster_name TEXT,
    metric_name TEXT NOT NULL,
    metric_value DECIMAL(12,2),
    rank INTEGER,
    trend TEXT CHECK (trend IN ('up', 'down', 'stable')),
    change_value DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tops_date ON weekly_tops(date);

-- ---------------------------------------------------------------------------
-- EXECUTION LOG
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS execution_log (
    id SERIAL PRIMARY KEY,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP,
    status TEXT CHECK (status IN ('running', 'success', 'failed')),
    stage TEXT,
    message TEXT,
    records_processed INTEGER DEFAULT 0
);

CREATE INDEX idx_exec_date ON execution_log(started_at);

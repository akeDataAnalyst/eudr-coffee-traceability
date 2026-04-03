USE romina_coffee_db;

CREATE TABLE IF NOT EXISTS eudr_compliance_audit (
    -- Unique ID for the database
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Traceability identifiers
    farmer_id VARCHAR(50) NOT NULL UNIQUE,
    region VARCHAR(100),
    woreda VARCHAR(100),
    
    -- Geospatial Data (Precision: 8 decimal places for GPS)
    latitude DECIMAL(11, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    altitude_masl INT,
    
    -- Plot Characteristics
    plot_size_ha DECIMAL(10, 2),
    coffee_variety VARCHAR(100),
    
    -- EUDR Parameters
    eudr_readiness_score DECIMAL(5, 2),
    is_non_compliant BOOLEAN DEFAULT FALSE,
    risk_category VARCHAR(20), -- e.g., 'Low', 'Medium', 'High'
    
    -- Metadata for auditing
    sync_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

DESCRIBE eudr_compliance_audit;
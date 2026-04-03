CREATE DATABASE romina_coffee_db;
USE romina_coffee_db;

CREATE TABLE coffee_plots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id VARCHAR(50) UNIQUE,
    region VARCHAR(100),
    woreda VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    altitude_masl INT,
    plot_size_ha DECIMAL(5, 2),
    eudr_readiness_score INT,
    is_non_compliant BOOLEAN,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
SELECT 
    region, 
    COUNT(farmer_id) AS total_farmers, 
    ROUND(SUM(plot_size_ha), 2) AS total_hectares, 
    ROUND(AVG(eudr_readiness_score), 1) AS avg_compliance_score
FROM eudr_compliance_audit
GROUP BY region
ORDER BY avg_compliance_score DESC;
SELECT 
    farmer_id, 
    region,
    woreda, 
    plot_size_ha, 
    eudr_readiness_score
FROM eudr_compliance_audit
WHERE plot_size_ha > 2.0 
  AND eudr_readiness_score < 80
ORDER BY plot_size_ha DESC;
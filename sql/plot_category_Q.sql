SELECT 
    CASE 
        WHEN plot_size_ha <= 2.0 THEN 'Small (0-2ha)'
        WHEN plot_size_ha <= 4.0 THEN 'Medium (2-4ha)'
        ELSE 'Large (>4ha)'
    END AS plot_category,
    COUNT(*) AS total_plots,
    ROUND(AVG(eudr_readiness_score), 2) AS avg_score
FROM eudr_compliance_audit
GROUP BY plot_category;
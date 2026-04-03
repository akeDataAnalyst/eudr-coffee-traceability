SELECT 
    woreda, 
    COUNT(*) AS non_compliant_count,
    ROUND(AVG(altitude_masl), 0) AS avg_altitude
FROM eudr_compliance_audit
WHERE is_non_compliant = 1
GROUP BY woreda
HAVING non_compliant_count > 5
ORDER BY non_compliant_count DESC;
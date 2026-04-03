CREATE VIEW v_ready_for_export AS
SELECT farmer_id, region, woreda, plot_size_ha, sync_date
FROM eudr_compliance_audit
WHERE is_non_compliant = 0 
  AND eudr_readiness_score >= 90;
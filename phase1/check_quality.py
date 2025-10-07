"""
Phase 1 - Step 4: Check Data Quality
Analyzes data completeness, missing values, and potential issues
"""

import logging


def check_quality_step(dataset_state):
    """
    Step 4: Check data quality (missing values, data types, outliers)
    
    Args:
        dataset_state: Dictionary containing loaded dataset and metadata
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    logger.info("\n" + "-"*70)
    logger.info("[STEP 4/4] CHECK DATA QUALITY")
    logger.info("-"*70)
    
    dataset = dataset_state.get('dataset')
    if dataset is None:
        logger.error("✗ Dataset not loaded!")
        return False
    
    try:
        primary_split = dataset_state['metadata']['primary_split']
        split_data = dataset[primary_split]
        total_records = len(split_data)
        
        # Sample size for quality check
        sample_size = min(1000, total_records)
        logger.info(f"Checking data quality on sample of {sample_size:,} records")
        logger.info(f"(Total dataset: {total_records:,} records)")
        logger.info("")
        
        # Get field names
        first_record = split_data[0]
        field_names = list(first_record.keys())
        
        logger.info("--- MISSING/NULL VALUE ANALYSIS ---")
        
        quality_report = {}
        
        for field_name in field_names:
            null_count = 0
            empty_count = 0
            
            # Check sample records
            for i in range(sample_size):
                value = split_data[i][field_name]
                
                # Check for null/None
                if value is None:
                    null_count += 1
                # Check for empty strings
                elif isinstance(value, str) and value.strip() == "":
                    empty_count += 1
                # Check for empty lists
                elif isinstance(value, list) and len(value) == 0:
                    empty_count += 1
            
            total_missing = null_count + empty_count
            missing_pct = (total_missing / sample_size) * 100
            
            quality_report[field_name] = {
                'null_count': null_count,
                'empty_count': empty_count,
                'total_missing': total_missing,
                'missing_pct': missing_pct
            }
            
            # Only log fields with missing data
            if total_missing > 0:
                logger.info(f"  {field_name}:")
                logger.info(f"    Null values: {null_count}/{sample_size} ({null_count/sample_size*100:.1f}%)")
                if empty_count > 0:
                    logger.info(f"    Empty values: {empty_count}/{sample_size} ({empty_count/sample_size*100:.1f}%)")
                logger.info(f"    Total missing: {total_missing}/{sample_size} ({missing_pct:.1f}%)")
                logger.info("")
        
        # Check if metrics fields have good quality
        metrics_fields = dataset_state['metadata'].get('metrics_fields', {})
        logger.info("--- METRICS FIELDS QUALITY CHECK ---")
        
        all_metrics = (metrics_fields.get('additions', []) + 
                      metrics_fields.get('deletions', []) + 
                      metrics_fields.get('files', []))
        
        if all_metrics:
            for metric_field in all_metrics:
                if metric_field in quality_report:
                    report = quality_report[metric_field]
                    logger.info(f"  {metric_field}:")
                    logger.info(f"    Missing: {report['missing_pct']:.1f}%")
                    
                    if report['missing_pct'] < 5:
                        logger.info(f"    Status: ✓ GOOD (< 5% missing)")
                    elif report['missing_pct'] < 20:
                        logger.info(f"    Status: ⚠ ACCEPTABLE (< 20% missing)")
                    else:
                        logger.info(f"    Status: ✗ CONCERNING (> 20% missing)")
                    logger.info("")
        else:
            logger.warning("  No metrics fields identified yet")
        
        # Store quality report
        dataset_state['metadata']['quality_report'] = quality_report
        
        # Summary
        fields_with_issues = sum(1 for r in quality_report.values() if r['total_missing'] > 0)
        logger.info("--- QUALITY SUMMARY ---")
        logger.info(f"  Total fields checked: {len(field_names)}")
        logger.info(f"  Fields with missing data: {fields_with_issues}")
        logger.info(f"  Sample size: {sample_size:,} records")
        
        logger.info(f"\n✓ Step 4 Complete - Data quality check done")
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed quality check: {e}")
        logger.error(f"  Error type: {type(e).__name__}")
        return False

"""
Phase 1 - Step 2: Understand Dataset Schema
Analyzes the structure and fields of the dataset
"""

import logging


def understand_schema_step(dataset_state):
    """
    Step 2: Understand the dataset schema (fields, types, structure)
    
    Args:
        dataset_state: Dictionary containing loaded dataset
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    logger.info("\n" + "-"*70)
    logger.info("[STEP 2/4] UNDERSTAND DATASET SCHEMA")
    logger.info("-"*70)
    
    dataset = dataset_state.get('dataset')
    if dataset is None:
        logger.error("✗ Dataset not loaded! Cannot analyze schema.")
        return False
    
    try:
        # Get the primary split (first one available)
        splits = list(dataset.keys())
        primary_split = splits[0]
        split_data = dataset[primary_split]
        
        logger.info(f"Analyzing primary split: '{primary_split}'")
        logger.info(f"Number of records: {len(split_data):,}")
        
        # Store primary split info
        dataset_state['metadata']['primary_split'] = primary_split
        
        # Get column names and types
        logger.info("\n--- DATASET FEATURES (COLUMNS) ---")
        
        fields_info = {}
        if hasattr(split_data, 'features'):
            for feature_name, feature_type in split_data.features.items():
                logger.info(f"  • {feature_name}")
                logger.info(f"      Type: {feature_type}")
                fields_info[feature_name] = str(feature_type)
        else:
            # Fallback: get from first record
            first_record = split_data[0]
            for key, value in first_record.items():
                value_type = type(value).__name__
                logger.info(f"  • {key}")
                logger.info(f"      Type: {value_type}")
                fields_info[key] = value_type
        
        # Store fields info
        dataset_state['metadata']['fields'] = fields_info
        dataset_state['metadata']['num_fields'] = len(fields_info)
        
        # Show a sample record
        logger.info("\n--- SAMPLE RECORD (First Entry) ---")
        first_record = split_data[0]
        
        for key, value in first_record.items():
            # Truncate long values for readability
            value_str = str(value)
            if len(value_str) > 150:
                value_str = value_str[:150] + "... [truncated]"
            
            # Format based on type
            if isinstance(value, (int, float)):
                logger.info(f"  {key}: {value}")
            elif isinstance(value, bool):
                logger.info(f"  {key}: {value}")
            elif isinstance(value, list):
                logger.info(f"  {key}: [list with {len(value)} items]")
                if len(value) > 0:
                    logger.info(f"      First item: {str(value[0])[:100]}")
            elif isinstance(value, dict):
                logger.info(f"  {key}: [dict with {len(value)} keys]")
                logger.info(f"      Keys: {list(value.keys())[:5]}")
            else:
                logger.info(f"  {key}: {value_str}")
        
        logger.info(f"\n✓ Step 2 Complete - Analyzed {len(fields_info)} fields")
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to analyze schema: {e}")
        logger.error(f"  Error type: {type(e).__name__}")
        return False

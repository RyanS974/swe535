"""
Phase 4 - Step 3: Identify Comment Fields
Finds fields containing comment text for classification
"""

import logging


def identify_comment_fields_step(dataset_state):
    """
    Step 3: Identify fields containing comment text
    
    Args:
        dataset_state: Dictionary containing loaded dataset and metadata
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    logger.info("\n" + "-"*70)
    logger.info("[STEP 3/4] IDENTIFY COMMENT FIELDS")
    logger.info("-"*70)
    
    dataset = dataset_state.get('dataset')
    if dataset is None:
        logger.error("✗ Dataset not loaded!")
        return False
    
    try:
        primary_split = dataset_state['metadata']['primary_split']
        split_data = dataset[primary_split]
        first_record = split_data[0]
        current_config = dataset_state['metadata'].get('config_name', 'unknown')
        
        # Keywords to search for in field names
        comment_keywords = ['body', 'text', 'comment', 'message', 'content']
        
        logger.info(f"Analyzing config: '{current_config}'")
        logger.info("Searching for comment text fields...")
        logger.info(f"Target: fields containing review comment text")
        logger.info("")
        
        found_fields = []
        
        # Search through all fields
        for field_name in first_record.keys():
            field_name_lower = field_name.lower()
            
            # Check if field name matches comment keywords
            if any(kw in field_name_lower for kw in comment_keywords):
                # Verify it's a string field
                value = first_record[field_name]
                if isinstance(value, str):
                    found_fields.append(field_name)
                    logger.info(f"✓ Found comment field: '{field_name}'")
                    
                    # Show sample (truncated)
                    sample = value[:200] if value else "[empty]"
                    logger.info(f"    Sample: {sample}...")
                    logger.info(f"    Type: string")
                    logger.info("")
        
        # Store found fields
        dataset_state['metadata']['comment_fields'] = found_fields
        
        # Summary
        logger.info("--- COMMENT FIELDS SUMMARY ---")
        logger.info(f"  Config analyzed: '{current_config}'")
        logger.info(f"  Comment fields found: {found_fields}")
        logger.info("")
        
        # Check if we found what we need
        if not found_fields:
            logger.warning("="*70)
            logger.warning("⚠ NOTICE: No comment text fields found in this config")
            logger.warning("="*70)
            logger.info("")
            logger.info(f"The '{current_config}' config may not contain comment text.")
            logger.info("Available fields in this config:")
            for field_name in first_record.keys():
                logger.info(f"  - {field_name}")
            logger.info("")
        else:
            # We found comment fields!
            logger.info("="*70)
            logger.info("✓ SUCCESS: Found comment text fields!")
            logger.info("="*70)
            logger.info("")
            logger.info(f"  ✓ Comment text fields: {found_fields}")
            logger.info("")
            logger.info("This config contains the comment data needed for analysis.")
            logger.info("")
        
        logger.info(f"✓ Step 3 Complete - Comment field identification done")
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to identify comment fields: {e}")
        logger.error(f"  Error type: {type(e).__name__}")
        return False

"""
Phase 1 - Step 3: Identify PR Metrics Fields
Finds fields related to additions, deletions, and files touched
"""

import logging


def identify_metrics_step(dataset_state):
    """
    Step 3: Identify fields containing PR metrics (additions, deletions, files)
    
    Args:
        dataset_state: Dictionary containing loaded dataset and metadata
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    logger.info("\n" + "-"*70)
    logger.info("[STEP 3/4] IDENTIFY PR METRICS FIELDS")
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
        target_keywords = {
            'additions': ['addition', 'add', 'insert', 'lines_added'],
            'deletions': ['deletion', 'delete', 'remove', 'lines_deleted'],
            'files': ['file', 'changed_files', 'touched', 'modified'],
            'changes': ['change', 'diff', 'patch', 'modification'],
        }
        
        logger.info(f"Analyzing config: '{current_config}'")
        logger.info("Searching for PR metrics fields...")
        logger.info(f"Target metrics: additions, deletions, files touched")
        logger.info("")
        
        found_metrics = {
            'additions': [],
            'deletions': [],
            'files': [],
            'other_relevant': []
        }
        
        # Search through all fields
        for field_name in first_record.keys():
            field_name_lower = field_name.lower()
            
            # Check for additions
            if any(kw in field_name_lower for kw in target_keywords['additions']):
                found_metrics['additions'].append(field_name)
                logger.info(f"✓ Found ADDITIONS field: '{field_name}'")
                sample_value = first_record[field_name]
                logger.info(f"    Sample value: {sample_value}")
                logger.info(f"    Type: {type(sample_value).__name__}")
                logger.info("")
            
            # Check for deletions
            elif any(kw in field_name_lower for kw in target_keywords['deletions']):
                found_metrics['deletions'].append(field_name)
                logger.info(f"✓ Found DELETIONS field: '{field_name}'")
                sample_value = first_record[field_name]
                logger.info(f"    Sample value: {sample_value}")
                logger.info(f"    Type: {type(sample_value).__name__}")
                logger.info("")
            
            # Check for files
            elif any(kw in field_name_lower for kw in target_keywords['files']):
                found_metrics['files'].append(field_name)
                logger.info(f"✓ Found FILES field: '{field_name}'")
                sample_value = first_record[field_name]
                
                # Handle different types
                if isinstance(sample_value, (int, float)):
                    logger.info(f"    Sample value: {sample_value}")
                elif isinstance(sample_value, list):
                    logger.info(f"    Sample value: [list with {len(sample_value)} items]")
                    if len(sample_value) > 0:
                        logger.info(f"    First item: {str(sample_value[0])[:100]}")
                else:
                    preview = str(sample_value)[:150]
                    logger.info(f"    Sample value: {preview}...")
                
                logger.info(f"    Type: {type(sample_value).__name__}")
                logger.info("")
            
            # Check for other change-related fields
            elif any(kw in field_name_lower for kw in target_keywords['changes']):
                found_metrics['other_relevant'].append(field_name)
                logger.info(f"  Found related field: '{field_name}'")
                sample_value = first_record[field_name]
                if isinstance(sample_value, (int, float, bool)):
                    logger.info(f"    Sample value: {sample_value}")
                logger.info("")
        
        # Store found metrics
        dataset_state['metadata']['metrics_fields'] = found_metrics
        
        # Summary
        logger.info("--- METRICS FIELDS SUMMARY ---")
        logger.info(f"  Config analyzed: '{current_config}'")
        logger.info(f"  Additions fields: {found_metrics['additions']}")
        logger.info(f"  Deletions fields: {found_metrics['deletions']}")
        logger.info(f"  Files fields: {found_metrics['files']}")
        logger.info(f"  Other relevant: {found_metrics['other_relevant']}")
        logger.info("")
        
        # Check if we found what we need
        has_additions = len(found_metrics['additions']) > 0
        has_deletions = len(found_metrics['deletions']) > 0
        has_files = len(found_metrics['files']) > 0
        
        if not (has_additions or has_deletions or has_files):
            logger.warning("="*70)
            logger.warning("⚠ NOTICE: No PR metrics fields found in this config")
            logger.warning("="*70)
            logger.info("")
            logger.info(f"The '{current_config}' config contains PR metadata only:")
            logger.info("  - PR identification (id, number, title)")
            logger.info("  - User/agent information")
            logger.info("  - Timestamps (created, closed, merged)")
            logger.info("  - Links (html_url, repo_url)")
            logger.info("")
            logger.info("This is expected for the 'pull_request' config.")
            logger.info("Metrics will be extracted from 'pr_commit_details' in Phase 2.")
            logger.info("")
            
            # List all available fields for reference
            logger.info("Available fields in this config:")
            for field_name in first_record.keys():
                logger.info(f"  - {field_name}")
            logger.info("")
        else:
            # We found some metrics!
            logger.info("="*70)
            logger.info("✓ SUCCESS: Found PR metrics fields!")
            logger.info("="*70)
            logger.info("")
            if has_additions:
                logger.info(f"  ✓ Additions data: {found_metrics['additions']}")
            if has_deletions:
                logger.info(f"  ✓ Deletions data: {found_metrics['deletions']}")
            if has_files:
                logger.info(f"  ✓ Files data: {found_metrics['files']}")
            logger.info("")
            logger.info("This config contains the metrics data needed for analysis.")
            logger.info("")
        
        logger.info(f"✓ Step 3 Complete - Metrics field identification done")
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to identify metrics: {e}")
        logger.error(f"  Error type: {type(e).__name__}")
        return False

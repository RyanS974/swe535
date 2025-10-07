"""
Phase 1: Dataset Exploration
Orchestrates the 4 steps of dataset exploration
"""

import logging
from .load_dataset import load_dataset_step
from .understand_schema import understand_schema_step
from .identify_metrics import identify_metrics_step
from .check_quality import check_quality_step


def run_phase1(dataset_state, config_name='pull_request', current_phase='Phase 1'):
    """
    Run all Phase 1 steps: Dataset Exploration
    
    Args:
        dataset_state: Dictionary to store dataset and metadata
                      Should contain: {'configs': {}, 'metadata': {}}
        config_name: Dataset configuration to load (default: 'pull_request')
        current_phase: Phase name for logging (default: 'Phase 1')
    
    Returns:
        bool: True if all steps completed successfully, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    logger.info("="*70)
    logger.info(f"{current_phase.upper()}: DATASET EXPLORATION")
    logger.info("="*70)
    logger.info("This phase will:")
    logger.info("  1. Load dataset from HuggingFace (or cache)")
    logger.info("  2. Understand the dataset schema")
    logger.info("  3. Identify PR metrics fields (additions/deletions/files)")
    logger.info("  4. Check data quality")
    logger.info("")
    
    # Step 1: Load Dataset
    success = load_dataset_step(dataset_state, config_name=config_name, current_phase=current_phase)
    if not success:
        logger.error(f"{current_phase} failed at Step 1: Load Dataset")
        return False
    
    # Step 2: Understand Schema
    success = understand_schema_step(dataset_state)
    if not success:
        logger.error(f"{current_phase} failed at Step 2: Understand Schema")
        return False
    
    # Step 3: Identify Metrics Fields
    success = identify_metrics_step(dataset_state)
    if not success:
        logger.error(f"{current_phase} failed at Step 3: Identify Metrics")
        return False
    
    # Step 4: Check Data Quality
    success = check_quality_step(dataset_state)
    if not success:
        logger.error(f"{current_phase} failed at Step 4: Check Quality")
        return False
    
    # All steps completed - determine if this is partial or complete
    # Check if we have all required configs for Question 1
    required_configs = ['pull_request', 'pr_commit_details']
    loaded_configs = list(dataset_state.get('configs', {}).keys())
    
    all_required_loaded = all(config in loaded_configs for config in required_configs)
    
    logger.info("\n" + "="*70)
    if all_required_loaded:
        logger.info(f"✓ {current_phase.upper()} COMPLETE - Dataset ready for extraction")
    else:
        logger.info(f"✓ {current_phase.upper()} for '{config_name}' COMPLETE - Dataset partially ready")
    logger.info("="*70)
    logger.info(f"Dataset loaded: {dataset_state['metadata'].get('total_records', 0)} records")
    logger.info(f"Configuration: {dataset_state['metadata'].get('config_name', 'unknown')}")
    logger.info(f"Primary split: {dataset_state['metadata'].get('primary_split', 'unknown')}")
    logger.info(f"Cache status: {dataset_state['metadata'].get('cache_status', 'unknown')}")
    
    return True


# Export the main function
__all__ = ['run_phase1']

"""
Phase 4: Dataset Exploration (Question 2)
Orchestrates the 4 steps of dataset exploration for review comments
"""

import logging
import sys
import os

# Add parent directory to path to import phase1 modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phase1.load_dataset import load_dataset_step
from phase1.understand_schema import understand_schema_step
from .identify_comment_fields import identify_comment_fields_step
from phase1.check_quality import check_quality_step


def run_phase4(dataset_state, config_name='pr_review_comments', current_phase='Phase 4'):
    """
    Run all Phase 4 steps: Dataset Exploration for Question 2
    
    Args:
        dataset_state: Dictionary to store dataset and metadata
                      Should contain: {'configs': {}, 'metadata': {}}
        config_name: Dataset configuration to load (default: 'pr_review_comments')
        current_phase: Phase name for logging (default: 'Phase 4')
    
    Returns:
        bool: True if all steps completed successfully, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    logger.info("="*70)
    logger.info(f"{current_phase.upper()}: DATASET EXPLORATION (Question 2)")
    logger.info("="*70)
    logger.info("This phase will:")
    logger.info("  1. Load dataset from HuggingFace (or cache)")
    logger.info("  2. Understand the dataset schema")
    logger.info("  3. Identify comment text fields")
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
    
    # Step 3: Identify Comment Fields (NEW for Phase 4)
    success = identify_comment_fields_step(dataset_state)
    if not success:
        logger.error(f"{current_phase} failed at Step 3: Identify Comment Fields")
        return False
    
    # Step 4: Check Data Quality
    success = check_quality_step(dataset_state)
    if not success:
        logger.error(f"{current_phase} failed at Step 4: Check Quality")
        return False
    
    # All steps completed
    logger.info("\n" + "="*70)
    logger.info(f"✓ {current_phase.upper()} for '{config_name}' COMPLETE")
    logger.info("="*70)
    logger.info(f"Dataset loaded: {dataset_state['metadata'].get('total_records', 0)} records")
    logger.info(f"Configuration: {dataset_state['metadata'].get('config_name', 'unknown')}")
    logger.info(f"Primary split: {dataset_state['metadata'].get('primary_split', 'unknown')}")
    logger.info(f"Cache status: {dataset_state['metadata'].get('cache_status', 'unknown')}")
    logger.info(f"Comment fields: {dataset_state['metadata'].get('comment_fields', [])}")
    
    return True


# Export the main function
__all__ = ['run_phase4']

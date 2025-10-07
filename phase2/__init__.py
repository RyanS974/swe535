"""
Phase 2: Data Extraction
Extracts per-PR metrics by aggregating commit-level data
"""

import logging
from .extract_metrics import extract_pr_metrics


def run_phase2(dataset_state):
    """
    Run Phase 2: Extract per-PR metrics
    
    Args:
        dataset_state: Dictionary containing loaded datasets
    
    Returns:
        tuple: (success: bool, metrics_df: DataFrame or None)
    """
    logger = logging.getLogger(__name__)
    
    logger.info("="*70)
    logger.info("PHASE 2: DATA EXTRACTION")
    logger.info("="*70)
    logger.info("Goal: Extract per-PR metrics (additions, deletions, files)")
    logger.info("")
    
    # Extract metrics
    success, metrics_df = extract_pr_metrics(dataset_state)
    
    if success:
        logger.info("\n" + "="*70)
        logger.info("✓ PHASE 2 COMPLETE - Per-PR metrics extracted")
        logger.info("="*70)
        logger.info(f"Total PRs processed: {len(metrics_df):,}")
        logger.info(f"Output file: pr_metrics.csv")
        return True, metrics_df
    else:
        logger.error("✗ PHASE 2 FAILED")
        return False, None


# Export the main function
__all__ = ['run_phase2']

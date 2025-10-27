"""
Phase 5: Data Extraction (Question 2)
Extracts per-PR review metrics by aggregating and categorizing comments
"""

import logging
from .extract_review_metrics import extract_review_metrics


def run_phase5(dataset_state):
    """
    Run Phase 5: Extract per-PR review metrics
    
    Args:
        dataset_state: Dictionary containing loaded datasets
    
    Returns:
        tuple: (success: bool, metrics_df: DataFrame or None)
    """
    logger = logging.getLogger(__name__)
    
    logger.info("="*70)
    logger.info("PHASE 5: DATA EXTRACTION (Question 2)")
    logger.info("="*70)
    logger.info("Goal: Extract and categorize review comments per PR")
    logger.info("Categories: correctness, style, security, testing, other")
    logger.info("")
    
    # Extract metrics
    success, metrics_df = extract_review_metrics(dataset_state)
    
    if success:
        logger.info("\n" + "="*70)
        logger.info("✓ PHASE 5 COMPLETE - Per-PR review metrics extracted")
        logger.info("="*70)
        logger.info(f"Total PRs processed: {len(metrics_df):,}")
        prs_with_comments = len(metrics_df[metrics_df['total_comments'] > 0])
        logger.info(f"PRs with review comments: {prs_with_comments:,}")
        logger.info(f"Output file: review_metrics.csv")
        return True, metrics_df
    else:
        logger.error("✗ PHASE 5 FAILED")
        return False, None


# Export the main function
__all__ = ['run_phase5']

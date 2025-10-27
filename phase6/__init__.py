"""
Phase 6: Analysis & Visualization (Question 2)
Generates visualizations and statistical summaries of review patterns
"""

import logging
from .statistical_analysis import perform_statistical_analysis
from .generate_visualizations import generate_all_visualizations


def run_phase6(review_metrics_df):
    """
    Run Phase 6: Analyze and visualize per-PR review metrics
    
    Args:
        review_metrics_df: DataFrame with extracted PR review metrics
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    logger.info("="*70)
    logger.info("PHASE 6: ANALYSIS & VISUALIZATION (Question 2)")
    logger.info("="*70)
    logger.info("Goal: Analyze and visualize review attention patterns")
    logger.info("")
    
    # Step 1: Statistical Analysis
    logger.info("Step 1: Performing statistical analysis...")
    analysis_success = perform_statistical_analysis(review_metrics_df)
    
    if not analysis_success:
        logger.error("✗ Statistical analysis failed")
        return False
    
    # Step 2: Generate Visualizations
    logger.info("\nStep 2: Generating visualizations...")
    viz_success = generate_all_visualizations(review_metrics_df)
    
    if not viz_success:
        logger.error("✗ Visualization generation failed")
        return False
    
    # Complete
    logger.info("\n" + "="*70)
    logger.info("✓ PHASE 6 COMPLETE")
    logger.info("="*70)
    logger.info("Analysis outputs saved to:")
    logger.info("  - figures/ (5 PNG visualizations)")
    logger.info("  - review_analysis.txt (text report)")
    
    return True


# Export the main function
__all__ = ['run_phase6']

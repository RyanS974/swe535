"""
Phase 3: Analysis & Visualization
Generates visualizations and statistical summaries of PR metrics
"""

import logging
from .generate_visualizations import generate_all_visualizations
from .statistical_analysis import perform_statistical_analysis


def run_phase3(pr_metrics_df):
    """
    Run Phase 3: Analyze and visualize per-PR metrics
    
    Args:
        pr_metrics_df: DataFrame with extracted PR metrics
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    logger.info("="*70)
    logger.info("PHASE 3: ANALYSIS & VISUALIZATION")
    logger.info("="*70)
    logger.info("Goal: Analyze and visualize PR change patterns")
    logger.info("")
    
    # Step 1: Statistical Analysis
    logger.info("Step 1: Performing statistical analysis...")
    analysis_success = perform_statistical_analysis(pr_metrics_df)
    
    if not analysis_success:
        logger.error("✗ Statistical analysis failed")
        return False
    
    # Step 2: Generate Visualizations
    logger.info("\nStep 2: Generating visualizations...")
    viz_success = generate_all_visualizations(pr_metrics_df)
    
    if not viz_success:
        logger.error("✗ Visualization generation failed")
        return False
    
    # Complete
    logger.info("\n" + "="*70)
    logger.info("✓ PHASE 3 COMPLETE")
    logger.info("="*70)
    logger.info("Analysis outputs saved to:")
    logger.info("  - figures/ (5 PNG visualizations)")
    logger.info("  - analysis_summary.txt (text report)")
    
    return True


# Export the main function
__all__ = ['run_phase3']

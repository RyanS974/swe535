"""
Phase 3: Statistical Analysis
Computes summary statistics for additions, deletions, and files touched
"""

import logging
import pandas as pd


def perform_statistical_analysis(df):
    """
    Perform statistical analysis of PR metrics
    
    Args:
        df: DataFrame with PR metrics
    
    Returns:
        bool: True if successful
    """
    logger = logging.getLogger(__name__)
    
    logger.info("\n" + "-"*70)
    logger.info("STATISTICAL ANALYSIS")
    logger.info("-"*70)
    
    # Open output file
    output_file = "analysis_summary.txt"
    with open(output_file, 'w') as f:
        
        # Write header
        f.write("="*70 + "\n")
        f.write("MSR 2026 - Question 1: How do Agentic-PRs change code?\n")
        f.write("Statistical Analysis Report\n")
        f.write("="*70 + "\n\n")
        
        # ----------------------------------------------------------------
        # DATASET TOTALS
        # ----------------------------------------------------------------
        
        f.write("-"*70 + "\n")
        f.write("DATASET TOTALS (Across All PRs)\n")
        f.write("-"*70 + "\n\n")
        
        total_additions = df['total_additions'].sum()
        total_deletions = df['total_deletions'].sum()
        total_files = df['files_touched'].sum()
        total_prs = len(df)
        
        f.write(f"Total PRs analyzed: {total_prs:,}\n")
        f.write(f"Total additions: {total_additions:,} lines\n")
        f.write(f"Total deletions: {total_deletions:,} lines\n")
        f.write(f"Total files touched: {total_files:,} files\n")
        f.write("\n")
        
        logger.info(f"Dataset totals: {total_prs:,} PRs, {total_additions:,} additions, {total_deletions:,} deletions, {total_files:,} files")
        
        # ----------------------------------------------------------------
        # PER-PR STATISTICS: Additions
        # ----------------------------------------------------------------
        
        f.write("-"*70 + "\n")
        f.write("PER-PR STATISTICS: ADDITIONS\n")
        f.write("-"*70 + "\n\n")
        
        additions = df['total_additions']
        f.write(f"Mean: {additions.mean():.1f} lines\n")
        f.write(f"Median: {additions.median():.1f} lines\n")
        f.write(f"Std Dev: {additions.std():.1f}\n")
        f.write(f"Min: {additions.min():,} lines\n")
        f.write(f"Max: {additions.max():,} lines\n")
        f.write(f"\nPercentiles:\n")
        f.write(f"  25th: {additions.quantile(0.25):.1f} lines\n")
        f.write(f"  50th: {additions.quantile(0.50):.1f} lines\n")
        f.write(f"  75th: {additions.quantile(0.75):.1f} lines\n")
        f.write(f"  90th: {additions.quantile(0.90):.1f} lines\n")
        f.write(f"  95th: {additions.quantile(0.95):.1f} lines\n")
        f.write("\n")
        
        logger.info(f"  Additions - Mean: {additions.mean():.1f}, Median: {additions.median():.1f}")
        
        # ----------------------------------------------------------------
        # PER-PR STATISTICS: Deletions
        # ----------------------------------------------------------------
        
        f.write("-"*70 + "\n")
        f.write("PER-PR STATISTICS: DELETIONS\n")
        f.write("-"*70 + "\n\n")
        
        deletions = df['total_deletions']
        f.write(f"Mean: {deletions.mean():.1f} lines\n")
        f.write(f"Median: {deletions.median():.1f} lines\n")
        f.write(f"Std Dev: {deletions.std():.1f}\n")
        f.write(f"Min: {deletions.min():,} lines\n")
        f.write(f"Max: {deletions.max():,} lines\n")
        f.write(f"\nPercentiles:\n")
        f.write(f"  25th: {deletions.quantile(0.25):.1f} lines\n")
        f.write(f"  50th: {deletions.quantile(0.50):.1f} lines\n")
        f.write(f"  75th: {deletions.quantile(0.75):.1f} lines\n")
        f.write(f"  90th: {deletions.quantile(0.90):.1f} lines\n")
        f.write(f"  95th: {deletions.quantile(0.95):.1f} lines\n")
        f.write("\n")
        
        logger.info(f"  Deletions - Mean: {deletions.mean():.1f}, Median: {deletions.median():.1f}")
        
        # ----------------------------------------------------------------
        # PER-PR STATISTICS: Files Touched
        # ----------------------------------------------------------------
        
        f.write("-"*70 + "\n")
        f.write("PER-PR STATISTICS: FILES TOUCHED\n")
        f.write("-"*70 + "\n\n")
        
        files = df['files_touched']
        f.write(f"Mean: {files.mean():.1f} files\n")
        f.write(f"Median: {files.median():.1f} files\n")
        f.write(f"Std Dev: {files.std():.1f}\n")
        f.write(f"Min: {files.min():,} files\n")
        f.write(f"Max: {files.max():,} files\n")
        f.write(f"\nPercentiles:\n")
        f.write(f"  25th: {files.quantile(0.25):.1f} files\n")
        f.write(f"  50th: {files.quantile(0.50):.1f} files\n")
        f.write(f"  75th: {files.quantile(0.75):.1f} files\n")
        f.write(f"  90th: {files.quantile(0.90):.1f} files\n")
        f.write(f"  95th: {files.quantile(0.95):.1f} files\n")
        f.write("\n")
        
        logger.info(f"  Files touched - Mean: {files.mean():.1f}, Median: {files.median():.1f}")
        
        # ----------------------------------------------------------------
        # PR SIZE DISTRIBUTION
        # ----------------------------------------------------------------
        
        f.write("-"*70 + "\n")
        f.write("PR SIZE DISTRIBUTION\n")
        f.write("-"*70 + "\n\n")
        
        f.write("Size categories based on lines added:\n")
        f.write("  XS: < 10 lines\n")
        f.write("  S:  10-100 lines\n")
        f.write("  M:  100-500 lines\n")
        f.write("  L:  500-1,000 lines\n")
        f.write("  XL: > 1,000 lines\n\n")
        
        size_dist = df['size_category'].value_counts().sort_index()
        size_order = ['XS', 'S', 'M', 'L', 'XL']
        
        f.write("Distribution:\n")
        for category in size_order:
            if category in size_dist.index:
                count = size_dist[category]
                pct = (count / len(df)) * 100
                f.write(f"  {category}: {count:,} PRs ({pct:.1f}%)\n")
        
        f.write("\n")
        
        logger.info(f"  Size distribution: XS={size_dist.get('XS', 0)}, S={size_dist.get('S', 0)}, M={size_dist.get('M', 0)}, L={size_dist.get('L', 0)}, XL={size_dist.get('XL', 0)}")
        
        # ----------------------------------------------------------------
        # END
        # ----------------------------------------------------------------
        
        f.write("="*70 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*70 + "\n")
    
    logger.info(f"✓ Statistical analysis saved to: {output_file}")
    
    return True

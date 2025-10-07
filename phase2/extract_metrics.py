"""
Phase 2: Extract Per-PR Metrics
Aggregates commit-level data to get per-PR statistics
"""

import logging
import pandas as pd
from collections import defaultdict


def extract_pr_metrics(dataset_state):
    """
    Extract per-PR metrics by aggregating pr_commit_details data
    
    Args:
        dataset_state: Dictionary containing loaded datasets
    
    Returns:
        tuple: (success: bool, metrics_df: DataFrame or None)
    """
    logger = logging.getLogger(__name__)
    
    logger.info("\n" + "-"*70)
    logger.info("EXTRACTING PER-PR METRICS")
    logger.info("-"*70)
    
    # Check if required configs are loaded
    if 'pull_request' not in dataset_state.get('configs', {}):
        logger.error("✗ pull_request config not loaded")
        return False, None
    
    if 'pr_commit_details' not in dataset_state.get('configs', {}):
        logger.error("✗ pr_commit_details config not loaded")
        return False, None
    
    # Get datasets
    pr_dataset = dataset_state['configs']['pull_request']['train']
    commit_details = dataset_state['configs']['pr_commit_details']['train']
    
    logger.info(f"Source datasets:")
    logger.info(f"  - pull_request: {len(pr_dataset):,} PRs")
    logger.info(f"  - pr_commit_details: {len(commit_details):,} file-level records")
    logger.info("")
    
    # Step 1: Convert PR dataset to DataFrame for easy merging
    logger.info("Step 1: Loading PR metadata...")
    pr_df = pd.DataFrame({
        'pr_id': pr_dataset['id'],
        'pr_number': pr_dataset['number'],
        'title': pr_dataset['title'],
        'agent': pr_dataset['agent'],
        'user': pr_dataset['user'],
        'state': pr_dataset['state'],
        'created_at': pr_dataset['created_at'],
        'merged_at': pr_dataset['merged_at'],
        'repo_url': pr_dataset['repo_url']
    })
    logger.info(f"  Loaded {len(pr_df):,} PRs")
    
    # Step 2: Aggregate commit details per PR
    logger.info("\nStep 2: Aggregating commit-level data per PR...")
    logger.info("  This may take a minute for 711k records...")
    
    # Use dictionaries for fast aggregation
    pr_metrics = defaultdict(lambda: {
        'total_additions': 0,
        'total_deletions': 0,
        'total_changes': 0,
        'files_touched': set(),
        'num_commits': set()
    })
    
    # Process all commit details
    processed = 0
    for i in range(len(commit_details)):
        pr_id = commit_details[i]['pr_id']
        
        # Aggregate using commit-level stats (more accurate than file-level)
        additions = commit_details[i]['commit_stats_additions']
        deletions = commit_details[i]['commit_stats_deletions']
        total = commit_details[i]['commit_stats_total']
        filename = commit_details[i]['filename']
        sha = commit_details[i]['sha']
        
        # Only count each commit once (not per file)
        if sha not in pr_metrics[pr_id]['num_commits']:
            pr_metrics[pr_id]['num_commits'].add(sha)
            pr_metrics[pr_id]['total_additions'] += additions if additions else 0
            pr_metrics[pr_id]['total_deletions'] += deletions if deletions else 0
            pr_metrics[pr_id]['total_changes'] += total if total else 0
        
        # Count unique files
        if filename:
            pr_metrics[pr_id]['files_touched'].add(filename)
        
        processed += 1
        if processed % 100000 == 0:
            logger.info(f"    Processed {processed:,} / {len(commit_details):,} records...")
    
    logger.info(f"  ✓ Processed all {len(commit_details):,} records")
    logger.info(f"  ✓ Found metrics for {len(pr_metrics):,} unique PRs")
    
    # Step 3: Convert aggregated metrics to DataFrame
    logger.info("\nStep 3: Building metrics DataFrame...")
    
    metrics_list = []
    for pr_id, metrics in pr_metrics.items():
        metrics_list.append({
            'pr_id': pr_id,
            'total_additions': metrics['total_additions'],
            'total_deletions': metrics['total_deletions'],
            'total_changes': metrics['total_changes'],
            'files_touched': len(metrics['files_touched']),
            'num_commits': len(metrics['num_commits'])
        })
    
    metrics_df = pd.DataFrame(metrics_list)
    logger.info(f"  ✓ Created metrics DataFrame: {len(metrics_df):,} rows")
    
    # Step 4: Merge with PR metadata
    logger.info("\nStep 4: Merging with PR metadata...")
    
    final_df = pr_df.merge(metrics_df, on='pr_id', how='left')
    
    # Fill NaN values with 0 for PRs without commit details
    final_df['total_additions'] = final_df['total_additions'].fillna(0).astype(int)
    final_df['total_deletions'] = final_df['total_deletions'].fillna(0).astype(int)
    final_df['total_changes'] = final_df['total_changes'].fillna(0).astype(int)
    final_df['files_touched'] = final_df['files_touched'].fillna(0).astype(int)
    final_df['num_commits'] = final_df['num_commits'].fillna(0).astype(int)
    
    logger.info(f"  ✓ Final DataFrame: {len(final_df):,} PRs with metrics")
    
    # Calculate derived metrics
    logger.info("\nStep 5: Computing derived metrics...")
    final_df['net_change'] = final_df['total_additions'] - final_df['total_deletions']
    final_df['churn_ratio'] = final_df['total_deletions'] / final_df['total_additions'].replace(0, 1)
    
    # Categorize PR size
    def categorize_pr_size(additions):
        if additions < 10:
            return 'XS'
        elif additions < 100:
            return 'S'
        elif additions < 500:
            return 'M'
        elif additions < 1000:
            return 'L'
        else:
            return 'XL'
    
    final_df['size_category'] = final_df['total_additions'].apply(categorize_pr_size)
    
    logger.info("  ✓ Added derived metrics:")
    logger.info("    - net_change (additions - deletions)")
    logger.info("    - churn_ratio (deletions / additions)")
    logger.info("    - size_category (XS/S/M/L/XL)")
    
    # Step 6: Display summary statistics
    logger.info("\n" + "="*70)
    logger.info("SUMMARY STATISTICS")
    logger.info("="*70)
    
    # Dataset Totals
    logger.info("\nDataset Totals:")
    logger.info(f"  Total PRs: {len(final_df):,}")
    logger.info(f"  Total additions: {final_df['total_additions'].sum():,} lines")
    logger.info(f"  Total deletions: {final_df['total_deletions'].sum():,} lines")
    logger.info(f"  Total files touched: {final_df['files_touched'].sum():,} files")
    
    # Per-PR Statistics
    logger.info("\nPer-PR Statistics:")
    
    logger.info("  Additions:")
    logger.info(f"    Mean: {final_df['total_additions'].mean():.1f}")
    logger.info(f"    Median: {final_df['total_additions'].median():.1f}")
    logger.info(f"    Min: {final_df['total_additions'].min()}")
    logger.info(f"    Max: {final_df['total_additions'].max()}")
    
    logger.info("  Deletions:")
    logger.info(f"    Mean: {final_df['total_deletions'].mean():.1f}")
    logger.info(f"    Median: {final_df['total_deletions'].median():.1f}")
    logger.info(f"    Min: {final_df['total_deletions'].min()}")
    logger.info(f"    Max: {final_df['total_deletions'].max()}")
    
    logger.info("  Files Touched:")
    logger.info(f"    Mean: {final_df['files_touched'].mean():.1f}")
    logger.info(f"    Median: {final_df['files_touched'].median():.1f}")
    logger.info(f"    Min: {final_df['files_touched'].min()}")
    logger.info(f"    Max: {final_df['files_touched'].max()}")
    
    logger.info("\nPR Size Distribution:")
    size_dist = final_df['size_category'].value_counts().sort_index()
    for category, count in size_dist.items():
        pct = (count / len(final_df)) * 100
        logger.info(f"  {category}: {count:,} ({pct:.1f}%)")
    logger.info("")
    
    # Step 7: Save to CSV
    logger.info("-"*70)
    logger.info("Saving results to CSV...")
    
    output_file = 'pr_metrics.csv'
    final_df.to_csv(output_file, index=False)
    logger.info(f"✓ Saved to: {output_file}")
    
    logger.info("\n✓ Extraction complete!")
    
    return True, final_df

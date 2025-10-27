"""
Phase 5: Extract Review Metrics
Aggregates comments from three datasets and categorizes them per PR
"""

import logging
import pandas as pd
from collections import defaultdict


def find_pr_id_field(dataset, dataset_name, logger):
    """
    Discover the correct field name for PR ID in a dataset
    
    Args:
        dataset: HuggingFace dataset
        dataset_name: Name for logging
        logger: Logger instance
    
    Returns:
        str: Field name for PR ID, or None if not found
    """
    if len(dataset) == 0:
        logger.warning(f"  {dataset_name} is empty")
        return None
    
    sample_keys = list(dataset[0].keys())
    logger.info(f"  {dataset_name} fields: {sample_keys}")
    
    # Try different possible field names
    for possible_name in ['pr_id', 'pull_request_id', 'pr', 'pull_request', 'id']:
        if possible_name in sample_keys:
            logger.info(f"  → Using '{possible_name}' as PR identifier")
            return possible_name
    
    logger.error(f"  ✗ Could not find PR ID field in {dataset_name}")
    return None


def extract_review_metrics(dataset_state):
    """
    Extract per-PR review metrics by aggregating and categorizing comments
    
    Args:
        dataset_state: Dictionary containing loaded datasets
    
    Returns:
        tuple: (success: bool, metrics_df: DataFrame or None)
    """
    logger = logging.getLogger(__name__)
    
    logger.info("\n" + "-"*70)
    logger.info("EXTRACTING PER-PR REVIEW METRICS")
    logger.info("-"*70)
    
    # Check if required configs are loaded
    required_configs = ['pr_review_comments', 'pr_reviews', 'pr_comments']
    for config in required_configs:
        if config not in dataset_state.get('configs', {}):
            logger.error(f"✗ {config} config not loaded")
            return False, None
    
    # Also need pull_request for PR metadata
    if 'pull_request' not in dataset_state.get('configs', {}):
        logger.error("✗ pull_request config not loaded")
        logger.info("  Note: Run Phase 1 first to load PR metadata")
        return False, None
    
    # Get datasets
    pr_dataset = dataset_state['configs']['pull_request']['train']
    review_comments = dataset_state['configs']['pr_review_comments']['train']
    pr_reviews = dataset_state['configs']['pr_reviews']['train']
    pr_comments = dataset_state['configs']['pr_comments']['train']
    
    logger.info(f"Source datasets:")
    logger.info(f"  - pull_request: {len(pr_dataset):,} PRs (metadata)")
    logger.info(f"  - pr_review_comments: {len(review_comments):,} records")
    logger.info(f"  - pr_reviews: {len(pr_reviews):,} records")
    logger.info(f"  - pr_comments: {len(pr_comments):,} records")
    logger.info(f"  Total comment records: {len(review_comments) + len(pr_reviews) + len(pr_comments):,}")
    logger.info("")
    
    # Step 1: Load PR metadata
    logger.info("Step 1: Loading PR metadata...")
    pr_df = pd.DataFrame({
        'pr_id': pr_dataset['id'],
        'pr_number': pr_dataset['number'],
        'title': pr_dataset['title'],
        'agent': pr_dataset['agent'],
        'user': pr_dataset['user'],
        'state': pr_dataset['state']
    })
    logger.info(f"  Loaded {len(pr_df):,} PRs")
    
    # Step 2: Discover field names and aggregate comments
    logger.info("\nStep 2: Discovering schemas and aggregating comments...")
    logger.info("  This may take a minute for 87k records...")
    logger.info("")
    
    pr_comment_texts = defaultdict(list)  # {pr_id: [comment1, comment2, ...]}
    
    # 2a. Review comments (line-level)
    logger.info("  Processing pr_review_comments...")
    pr_id_field_rc = find_pr_id_field(review_comments, 'pr_review_comments', logger)
    
    if pr_id_field_rc is None:
        return False, None
    
    processed = 0
    for i in range(len(review_comments)):
        pr_id = review_comments[i][pr_id_field_rc]
        body = review_comments[i].get('body')
        
        # Skip null/empty comments
        if body and isinstance(body, str) and body.strip():
            pr_comment_texts[pr_id].append(body.strip())
        
        processed += 1
        if processed % 5000 == 0:
            logger.info(f"    Processed {processed:,} / {len(review_comments):,}...")
    
    logger.info(f"  ✓ Processed {len(review_comments):,} pr_review_comments")
    logger.info("")
    
    # 2b. PR reviews (summaries)
    logger.info("  Processing pr_reviews...")
    pr_id_field_pr = find_pr_id_field(pr_reviews, 'pr_reviews', logger)
    
    if pr_id_field_pr is None:
        return False, None
    
    processed = 0
    for i in range(len(pr_reviews)):
        pr_id = pr_reviews[i][pr_id_field_pr]
        body = pr_reviews[i].get('body')
        
        if body and isinstance(body, str) and body.strip():
            pr_comment_texts[pr_id].append(body.strip())
        
        processed += 1
        if processed % 5000 == 0:
            logger.info(f"    Processed {processed:,} / {len(pr_reviews):,}...")
    
    logger.info(f"  ✓ Processed {len(pr_reviews):,} pr_reviews")
    logger.info("")
    
    # 2c. General PR comments
    logger.info("  Processing pr_comments...")
    pr_id_field_pc = find_pr_id_field(pr_comments, 'pr_comments', logger)
    
    if pr_id_field_pc is None:
        return False, None
    
    processed = 0
    for i in range(len(pr_comments)):
        pr_id = pr_comments[i][pr_id_field_pc]
        body = pr_comments[i].get('body')
        
        if body and isinstance(body, str) and body.strip():
            pr_comment_texts[pr_id].append(body.strip())
        
        processed += 1
        if processed % 5000 == 0:
            logger.info(f"    Processed {processed:,} / {len(pr_comments):,}...")
    
    logger.info(f"  ✓ Processed {len(pr_comments):,} pr_comments")
    logger.info(f"  ✓ Aggregated comments for {len(pr_comment_texts):,} unique PRs")
    
    # Calculate total comments
    total_comments = sum(len(comments) for comments in pr_comment_texts.values())
    logger.info(f"  ✓ Total valid comments: {total_comments:,}")
    logger.info("")
    
    # Step 3: Classify all comments
    logger.info("Step 3: Classifying comments into categories...")
    from .categorize_comments import categorize_all_comments
    
    category_counts = categorize_all_comments(pr_comment_texts)
    
    # Step 4: Build metrics DataFrame
    logger.info("Step 4: Building metrics DataFrame...")
    
    metrics_list = []
    for pr_id, categories in category_counts.items():
        total = sum(categories.values())
        
        # Calculate counts
        metrics_dict = {
            'pr_id': pr_id,
            'total_comments': total,
            'correctness_count': categories.get('correctness', 0),
            'style_count': categories.get('style', 0),
            'security_count': categories.get('security', 0),
            'testing_count': categories.get('testing', 0),
            'other_count': categories.get('other', 0)
        }
        
        # Calculate percentages (with division by zero protection)
        if total > 0:
            metrics_dict['correctness_pct'] = (categories.get('correctness', 0) / total * 100)
            metrics_dict['style_pct'] = (categories.get('style', 0) / total * 100)
            metrics_dict['security_pct'] = (categories.get('security', 0) / total * 100)
            metrics_dict['testing_pct'] = (categories.get('testing', 0) / total * 100)
            metrics_dict['other_pct'] = (categories.get('other', 0) / total * 100)
        else:
            metrics_dict['correctness_pct'] = 0.0
            metrics_dict['style_pct'] = 0.0
            metrics_dict['security_pct'] = 0.0
            metrics_dict['testing_pct'] = 0.0
            metrics_dict['other_pct'] = 0.0
        
        metrics_list.append(metrics_dict)
    
    metrics_df = pd.DataFrame(metrics_list)
    logger.info(f"  ✓ Created metrics DataFrame: {len(metrics_df):,} rows")
    
    # Step 5: Determine primary category for each PR
    logger.info("\nStep 5: Determining primary category per PR...")
    
    def get_primary_category(row):
        """Get category with highest count"""
        categories = {
            'correctness': row['correctness_count'],
            'style': row['style_count'],
            'security': row['security_count'],
            'testing': row['testing_count'],
            'other': row['other_count']
        }
        return max(categories, key=categories.get)
    
    metrics_df['primary_category'] = metrics_df.apply(get_primary_category, axis=1)
    logger.info("  ✓ Added primary_category column")
    
    # Step 6: Merge with PR metadata
    logger.info("\nStep 6: Merging with PR metadata...")
    
    final_df = pr_df.merge(metrics_df, on='pr_id', how='left')
    
    # Fill NaN values with 0 for PRs without comments
    comment_cols = ['total_comments', 'correctness_count', 'style_count', 
                   'security_count', 'testing_count', 'other_count',
                   'correctness_pct', 'style_pct', 'security_pct', 
                   'testing_pct', 'other_pct']
    
    for col in comment_cols:
        final_df[col] = final_df[col].fillna(0)
    
    # For PRs with no comments, set primary_category to 'none'
    final_df['primary_category'] = final_df['primary_category'].fillna('none')
    
    # Convert counts to integers
    count_cols = ['total_comments', 'correctness_count', 'style_count', 
                  'security_count', 'testing_count', 'other_count']
    for col in count_cols:
        final_df[col] = final_df[col].astype(int)
    
    logger.info(f"  ✓ Final DataFrame: {len(final_df):,} PRs total")
    
    prs_with_comments = len(final_df[final_df['total_comments'] > 0])
    prs_without_comments = len(final_df[final_df['total_comments'] == 0])
    
    logger.info(f"  ✓ PRs with comments: {prs_with_comments:,}")
    logger.info(f"  ✓ PRs without comments: {prs_without_comments:,}")
    
    # Step 7: Display summary statistics
    logger.info("\n" + "="*70)
    logger.info("SUMMARY STATISTICS")
    logger.info("="*70)
    
    # Filter to PRs with comments for statistics
    df_with_comments = final_df[final_df['total_comments'] > 0]
    
    logger.info("\nDataset Totals:")
    logger.info(f"  Total PRs: {len(final_df):,}")
    logger.info(f"  PRs with review comments: {len(df_with_comments):,}")
    logger.info(f"  Total comments: {df_with_comments['total_comments'].sum():,}")
    if len(df_with_comments) > 0:
        logger.info(f"  Average comments per PR: {df_with_comments['total_comments'].mean():.1f}")
    
    logger.info("\nCategory Distribution (Across All Comments):")
    total_all = df_with_comments['total_comments'].sum()
    for category in ['correctness', 'style', 'security', 'testing', 'other']:
        count = df_with_comments[f'{category}_count'].sum()
        pct = (count / total_all * 100) if total_all > 0 else 0
        logger.info(f"  {category.capitalize()}: {count:,} ({pct:.1f}%)")
    
    if len(df_with_comments) > 0:
        logger.info("\nPrimary Category Distribution (Per PR):")
        primary_dist = df_with_comments['primary_category'].value_counts()
        for category, count in primary_dist.items():
            pct = (count / len(df_with_comments)) * 100
            logger.info(f"  {category.capitalize()}: {count:,} PRs ({pct:.1f}%)")
    
    logger.info("")
    
    # Step 8: Save to CSV
    logger.info("-"*70)
    logger.info("Saving results to CSV...")
    
    output_file = 'review_metrics.csv'
    final_df.to_csv(output_file, index=False)
    logger.info(f"✓ Saved to: {output_file}")
    
    logger.info("\n✓ Extraction complete!")
    
    return True, final_df

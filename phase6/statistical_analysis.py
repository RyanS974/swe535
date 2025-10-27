"""
Phase 6: Statistical Analysis
Computes summary statistics for review categories and comments
"""

import logging
import pandas as pd


def perform_statistical_analysis(df):
    """
    Perform statistical analysis of review metrics
    
    Args:
        df: DataFrame with review metrics from Phase 5
    
    Returns:
        bool: True if successful
    """
    logger = logging.getLogger(__name__)
    
    logger.info("\n" + "-"*70)
    logger.info("STATISTICAL ANALYSIS")
    logger.info("-"*70)
    
    # Filter to PRs with at least one comment
    df_with_comments = df[df['total_comments'] > 0].copy()
    
    if len(df_with_comments) == 0:
        logger.warning("No PRs with comments found!")
        return False
    
    # Open output file
    output_file = "review_analysis.txt"
    with open(output_file, 'w') as f:
        
        # Write header
        f.write("="*70 + "\n")
        f.write("MSR 2026 - Question 2: What aspects receive most attention?\n")
        f.write("Review Analysis Report\n")
        f.write("="*70 + "\n\n")
        
        # ----------------------------------------------------------------
        # DATASET TOTALS
        # ----------------------------------------------------------------
        
        f.write("-"*70 + "\n")
        f.write("DATASET TOTALS\n")
        f.write("-"*70 + "\n\n")
        
        total_prs = len(df)
        prs_with_comments = len(df_with_comments)
        total_comments = df_with_comments['total_comments'].sum()
        avg_comments = df_with_comments['total_comments'].mean()
        
        f.write(f"Total PRs analyzed: {total_prs:,}\n")
        f.write(f"PRs with review comments: {prs_with_comments:,} ({prs_with_comments/total_prs*100:.1f}%)\n")
        f.write(f"Total review comments: {total_comments:,}\n")
        f.write(f"Average comments per PR (with comments): {avg_comments:.1f}\n")
        f.write("\n")
        
        logger.info(f"Dataset totals: {total_prs:,} PRs, {prs_with_comments:,} with comments, {total_comments:,} total comments")
        
        # ----------------------------------------------------------------
        # CATEGORY DISTRIBUTION (Across All Comments)
        # ----------------------------------------------------------------
        
        f.write("-"*70 + "\n")
        f.write("CATEGORY DISTRIBUTION (Across All Comments)\n")
        f.write("-"*70 + "\n\n")
        
        f.write("Total comments by category:\n")
        
        # Calculate totals per category
        category_totals = {
            'Correctness': df_with_comments['correctness_count'].sum(),
            'Style': df_with_comments['style_count'].sum(),
            'Security': df_with_comments['security_count'].sum(),
            'Testing': df_with_comments['testing_count'].sum(),
            'Other': df_with_comments['other_count'].sum()
        }
        
        # Sort by count descending
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        for category, count in sorted_categories:
            pct = (count / total_comments * 100) if total_comments > 0 else 0
            marker = " ← HIGHEST" if count == sorted_categories[0][1] else ""
            f.write(f"  {category}: {count:,} comments ({pct:.1f}%){marker}\n")
        
        f.write("\n")
        f.write(f"KEY FINDING: {sorted_categories[0][0]} receives the most attention during code review,\n")
        f.write(f"accounting for {sorted_categories[0][1]/total_comments*100:.1f}% of all review comments.\n")
        f.write("\n")
        
        logger.info(f"  Top category: {sorted_categories[0][0]} ({sorted_categories[0][1]/total_comments*100:.1f}%)")
        
        # ----------------------------------------------------------------
        # PER-PR STATISTICS
        # ----------------------------------------------------------------
        
        f.write("-"*70 + "\n")
        f.write("PER-PR STATISTICS\n")
        f.write("-"*70 + "\n\n")
        
        comments = df_with_comments['total_comments']
        
        f.write("Comments per PR:\n")
        f.write(f"  Mean: {comments.mean():.1f} comments\n")
        f.write(f"  Median: {comments.median():.1f} comments\n")
        f.write(f"  Std Dev: {comments.std():.1f}\n")
        f.write(f"  Min: {comments.min()} comment{'s' if comments.min() > 1 else ''}\n")
        f.write(f"  Max: {comments.max()} comments\n")
        f.write("\n")
        
        f.write("Percentiles:\n")
        f.write(f"  25th: {comments.quantile(0.25):.0f} comments\n")
        f.write(f"  50th: {comments.quantile(0.50):.0f} comments\n")
        f.write(f"  75th: {comments.quantile(0.75):.0f} comments\n")
        f.write(f"  90th: {comments.quantile(0.90):.0f} comments\n")
        f.write(f"  95th: {comments.quantile(0.95):.0f} comments\n")
        f.write("\n")
        
        logger.info(f"  Comments per PR - Mean: {comments.mean():.1f}, Median: {comments.median():.1f}")
        
        # ----------------------------------------------------------------
        # PRIMARY CATEGORY DISTRIBUTION
        # ----------------------------------------------------------------
        
        f.write("-"*70 + "\n")
        f.write("PRIMARY CATEGORY DISTRIBUTION\n")
        f.write("-"*70 + "\n\n")
        
        f.write("PRs by primary category:\n")
        
        primary_counts = df_with_comments['primary_category'].value_counts()
        for category, count in primary_counts.items():
            pct = (count / len(df_with_comments)) * 100
            f.write(f"  {category.capitalize()}-focused: {count:,} PRs ({pct:.1f}%)\n")
        
        f.write("\n")
        
        logger.info(f"  Primary categories: {dict(primary_counts)}")
        
        # ----------------------------------------------------------------
        # CATEGORY CO-OCCURRENCE ANALYSIS
        # ----------------------------------------------------------------
        
        f.write("-"*70 + "\n")
        f.write("CATEGORY CO-OCCURRENCE ANALYSIS\n")
        f.write("-"*70 + "\n\n")
        
        # Calculate average categories per PR
        categories_per_pr = []
        for idx, row in df_with_comments.iterrows():
            cat_count = sum([
                1 if row['correctness_count'] > 0 else 0,
                1 if row['style_count'] > 0 else 0,
                1 if row['security_count'] > 0 else 0,
                1 if row['testing_count'] > 0 else 0,
                1 if row['other_count'] > 0 else 0
            ])
            categories_per_pr.append(cat_count)
        
        avg_categories = sum(categories_per_pr) / len(categories_per_pr)
        f.write(f"Average categories per PR: {avg_categories:.1f}\n")
        f.write("\n")
        
        # Common combinations
        f.write("Common combinations:\n")
        
        style_and_correctness = len(df_with_comments[
            (df_with_comments['style_count'] > 0) & 
            (df_with_comments['correctness_count'] > 0)
        ])
        f.write(f"  Style + Correctness: {style_and_correctness/len(df_with_comments)*100:.0f}% of PRs\n")
        
        style_and_testing = len(df_with_comments[
            (df_with_comments['style_count'] > 0) & 
            (df_with_comments['testing_count'] > 0)
        ])
        f.write(f"  Style + Testing: {style_and_testing/len(df_with_comments)*100:.0f}% of PRs\n")
        
        correctness_and_testing = len(df_with_comments[
            (df_with_comments['correctness_count'] > 0) & 
            (df_with_comments['testing_count'] > 0)
        ])
        f.write(f"  Correctness + Testing: {correctness_and_testing/len(df_with_comments)*100:.0f}% of PRs\n")
        
        all_three = len(df_with_comments[
            (df_with_comments['style_count'] > 0) & 
            (df_with_comments['correctness_count'] > 0) & 
            (df_with_comments['testing_count'] > 0)
        ])
        f.write(f"  Style + Correctness + Testing: {all_three/len(df_with_comments)*100:.0f}% of PRs\n")
        f.write("\n")
        
        # Security co-occurrence
        security_prs = df_with_comments[df_with_comments['security_count'] > 0]
        if len(security_prs) > 0:
            f.write("PRs with security concerns also mention:\n")
            
            sec_with_correct = len(security_prs[security_prs['correctness_count'] > 0])
            f.write(f"  Correctness: {sec_with_correct/len(security_prs)*100:.0f}% of the time\n")
            
            sec_with_test = len(security_prs[security_prs['testing_count'] > 0])
            f.write(f"  Testing: {sec_with_test/len(security_prs)*100:.0f}% of the time\n")
            
            sec_with_style = len(security_prs[security_prs['style_count'] > 0])
            f.write(f"  Style: {sec_with_style/len(security_prs)*100:.0f}% of the time\n")
        
        f.write("\n")
        
        # ----------------------------------------------------------------
        # RESEARCH QUESTION ANSWER
        # ----------------------------------------------------------------
        
        f.write("="*70 + "\n")
        f.write("RESEARCH QUESTION ANSWER\n")
        f.write("="*70 + "\n\n")
        
        f.write("What aspects of Agentic-PRs receive the most attention during review?\n\n")
        
        # Rank categories
        for i, (category, count) in enumerate(sorted_categories, 1):
            pct = (count / total_comments * 100)
            f.write(f"{i}. {category.upper()} ({pct:.1f}%)\n")
        
        f.write("\n")
        
        # Interpretation
        top_cat = sorted_categories[0][0]
        top_pct = sorted_categories[0][1] / total_comments * 100
        second_cat = sorted_categories[1][0]
        second_pct = sorted_categories[1][1] / total_comments * 100
        
        f.write(f"Reviewers prioritize {top_cat.lower()} ({top_pct:.1f}%) over {second_cat.lower()} ")
        f.write(f"({second_pct:.1f}%), suggesting that ")
        
        if top_cat == "Style":
            f.write("AI-generated code is often\n")
            f.write("functionally correct but needs human polish for production readiness.\n")
        elif top_cat == "Correctness":
            f.write("reviewers focus heavily on\n")
            f.write("ensuring functional correctness and catching bugs in AI-generated code.\n")
        elif top_cat == "Testing":
            f.write("AI agents often miss test coverage,\n")
            f.write("requiring human reviewers to ensure adequate testing.\n")
        elif top_cat == "Security":
            f.write("security is a major concern in\n")
            f.write("AI-generated code, requiring careful human review.\n")
        
        f.write("\n")
        
        # ----------------------------------------------------------------
        # END
        # ----------------------------------------------------------------
        
        f.write("="*70 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*70 + "\n")
    
    logger.info(f"✓ Statistical analysis saved to: {output_file}")
    
    return True

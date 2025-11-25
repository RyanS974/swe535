"""
Phase 6: Generate Visualizations
Creates publication-quality plots of review category patterns
UPDATED: Enhanced font sizes and readability
"""

import logging
import matplotlib.pyplot as plt
import seaborn as sns
import os


def setup_plot_style():
    """Configure matplotlib style for publication-quality plots with enhanced readability"""
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1.8)  # Increased from 1.2 to 1.8
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['figure.figsize'] = (12, 7)  # Increased from (10, 6)
    plt.rcParams['font.size'] = 14  # Base font size
    plt.rcParams['axes.labelsize'] = 16  # Axis label size
    plt.rcParams['axes.titlesize'] = 18  # Title size
    plt.rcParams['xtick.labelsize'] = 14  # X-axis tick label size
    plt.rcParams['ytick.labelsize'] = 14  # Y-axis tick label size
    plt.rcParams['legend.fontsize'] = 14  # Legend font size
    plt.rcParams['lines.linewidth'] = 2.5  # Thicker lines


def plot_category_distribution(df):
    """Bar chart showing percentage of comments per category"""
    logger = logging.getLogger(__name__)
    logger.info("  Creating: q2_category_distribution.png")
    
    # Filter to PRs with comments
    df_with_comments = df[df['total_comments'] > 0]
    
    # Calculate total comments per category
    category_totals = {
        'Correctness': df_with_comments['correctness_count'].sum(),
        'Style': df_with_comments['style_count'].sum(),
        'Security': df_with_comments['security_count'].sum(),
        'Testing': df_with_comments['testing_count'].sum(),
        'Other': df_with_comments['other_count'].sum()
    }
    
    total_comments = sum(category_totals.values())
    
    # Calculate percentages
    categories = list(category_totals.keys())
    percentages = [(count / total_comments * 100) for count in category_totals.values()]
    
    # Sort by percentage descending
    sorted_pairs = sorted(zip(categories, percentages), key=lambda x: x[1], reverse=True)
    categories, percentages = zip(*sorted_pairs)
    
    # Create horizontal bar chart
    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.barh(categories, percentages, color='steelblue', edgecolor='black', linewidth=2)
    
    # Add percentage labels on bars with larger font
    for i, (cat, pct) in enumerate(zip(categories, percentages)):
        ax.text(pct + 1, i, f'{pct:.1f}%', va='center', fontweight='bold', fontsize=15)
    
    ax.set_xlabel('Percentage of Total Comments', fontsize=16, fontweight='bold')
    ax.set_title('What Aspects of Agentic-PRs Receive Most Attention?', 
                 fontsize=18, fontweight='bold', pad=15)
    ax.set_xlim(0, max(percentages) * 1.15)
    ax.tick_params(labelsize=14)
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('figures/q2_category_distribution.png', bbox_inches='tight', dpi=300)
    plt.close()


def plot_comments_per_pr(df):
    """Histogram of total comments per PR"""
    logger = logging.getLogger(__name__)
    logger.info("  Creating: q2_comments_per_pr.png")
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Filter PRs with at least 1 comment
    df_with_comments = df[df['total_comments'] > 0]
    
    # Histogram (clip at 50 for visibility)
    ax.hist(df_with_comments['total_comments'].clip(upper=50), 
            bins=50, color='teal', edgecolor='black', alpha=0.7, linewidth=1.5)
    
    # Add median line
    median_comments = df_with_comments['total_comments'].median()
    ax.axvline(median_comments, color='red', linestyle='--', linewidth=3,
               label=f'Median: {median_comments:.1f} comments')
    
    ax.set_xlabel('Number of Review Comments', fontsize=16, fontweight='bold')
    ax.set_ylabel('Number of PRs', fontsize=16, fontweight='bold')
    ax.set_title('Distribution of Review Comments per PR\n(Clipped at 50 for visibility)', 
                 fontsize=18, fontweight='bold', pad=15)
    ax.legend(fontsize=14, frameon=True, shadow=True)
    ax.tick_params(labelsize=14)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figures/q2_comments_per_pr.png', bbox_inches='tight', dpi=300)
    plt.close()


def plot_category_heatmap(df):
    """Heatmap showing category co-occurrence"""
    logger = logging.getLogger(__name__)
    logger.info("  Creating: q2_category_heatmap.png")
    
    # Select only category percentage columns
    category_cols = ['correctness_pct', 'style_pct', 'security_pct', 'testing_pct', 'other_pct']
    
    # Filter to PRs with comments
    df_with_comments = df[df['total_comments'] > 0]
    
    # Calculate correlation matrix
    corr_matrix = df_with_comments[category_cols].corr()
    
    # Rename columns for display
    corr_matrix.index = ['Correctness', 'Style', 'Security', 'Testing', 'Other']
    corr_matrix.columns = ['Correctness', 'Style', 'Security', 'Testing', 'Other']
    
    # Create heatmap with larger fonts
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                vmin=-1, vmax=1, square=True, linewidths=2, 
                cbar_kws={"shrink": 0.8},
                annot_kws={"fontsize": 14, "fontweight": "bold"},
                ax=ax)
    
    ax.set_title('Review Category Co-occurrence Pattern', 
                 fontsize=18, fontweight='bold', pad=20)
    
    # Increase tick label size
    ax.tick_params(labelsize=14)
    plt.setp(ax.get_xticklabels(), fontweight='bold')
    plt.setp(ax.get_yticklabels(), fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/q2_category_heatmap.png', bbox_inches='tight', dpi=300)
    plt.close()


def plot_primary_category_pie(df):
    """Pie chart of primary category distribution"""
    logger = logging.getLogger(__name__)
    logger.info("  Creating: q2_primary_category_pie.png")
    
    # Filter to PRs with comments
    df_with_comments = df[df['total_comments'] > 0]
    
    # Count PRs by primary category
    primary_counts = df_with_comments['primary_category'].value_counts()
    
    # Calculate percentages
    total_prs = len(df_with_comments)
    labels = [label.capitalize() for label in primary_counts.index.tolist()]
    sizes = primary_counts.values.tolist()
    percentages = [(count / total_prs * 100) for count in sizes]
    
    # Create pie chart
    fig, ax = plt.subplots(figsize=(12, 10))
    colors_palette = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        autopct='%1.1f%%',
        colors=colors_palette[:len(labels)],
        startangle=90,
        textprops={'fontsize': 14, 'fontweight': 'bold'}
    )
    
    # Bold percentage text and make it larger
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(16)
    
    ax.set_title('Primary Review Focus per PR', fontsize=18, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('figures/q2_primary_category_pie.png', bbox_inches='tight', dpi=300)
    plt.close()


def plot_review_overview(df):
    """Combined overview with 4 subplots"""
    logger = logging.getLogger(__name__)
    logger.info("  Creating: q2_review_overview.png")
    
    # Filter to PRs with comments
    df_with_comments = df[df['total_comments'] > 0]
    
    fig = plt.figure(figsize=(18, 14))
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.35)
    
    # Top-left: Category distribution bar
    ax1 = fig.add_subplot(gs[0, 0])
    
    category_totals = {
        'Correctness': df_with_comments['correctness_count'].sum(),
        'Style': df_with_comments['style_count'].sum(),
        'Security': df_with_comments['security_count'].sum(),
        'Testing': df_with_comments['testing_count'].sum(),
        'Other': df_with_comments['other_count'].sum()
    }
    
    total_comments = sum(category_totals.values())
    sorted_pairs = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    categories, counts = zip(*sorted_pairs)
    percentages = [(count / total_comments * 100) for count in counts]
    
    bars = ax1.barh(categories, percentages, color='steelblue', edgecolor='black', linewidth=2)
    for i, pct in enumerate(percentages):
        ax1.text(pct + 0.5, i, f'{pct:.1f}%', va='center', fontsize=13, fontweight='bold')
    
    ax1.set_xlabel('Percentage (%)', fontsize=14, fontweight='bold')
    ax1.set_title('Category Distribution', fontsize=15, fontweight='bold', pad=10)
    ax1.set_xlim(0, max(percentages) * 1.15)
    ax1.tick_params(labelsize=13)
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Top-right: Comments histogram
    ax2 = fig.add_subplot(gs[0, 1])
    
    ax2.hist(df_with_comments['total_comments'].clip(upper=50), 
             bins=30, color='teal', edgecolor='black', alpha=0.7, linewidth=1.5)
    median_comments = df_with_comments['total_comments'].median()
    ax2.axvline(median_comments, color='red', linestyle='--', linewidth=3)
    
    ax2.set_xlabel('Comments per PR', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Count', fontsize=14, fontweight='bold')
    ax2.set_title('Comments Distribution', fontsize=15, fontweight='bold', pad=10)
    ax2.tick_params(labelsize=13)
    ax2.grid(True, alpha=0.3)
    
    # Bottom-left: Primary category pie
    ax3 = fig.add_subplot(gs[1, 0])
    
    primary_counts = df_with_comments['primary_category'].value_counts()
    labels = [label.capitalize() for label in primary_counts.index[:5]]
    sizes = primary_counts.values[:5]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    
    wedges, texts, autotexts = ax3.pie(
        sizes, labels=labels, autopct='%1.1f%%',
        colors=colors[:len(labels)], startangle=90,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(14)
    
    ax3.set_title('Primary Category', fontsize=15, fontweight='bold', pad=10)
    
    # Bottom-right: Summary statistics text
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    summary_text = f"""SUMMARY STATISTICS

Total PRs: {len(df):,}
PRs with Comments: {len(df_with_comments):,}
Total Comments: {df_with_comments['total_comments'].sum():,}
Avg Comments/PR: {df_with_comments['total_comments'].mean():.1f}

CATEGORY BREAKDOWN
"""
    
    for category, count in sorted_pairs:
        pct = count / total_comments * 100
        summary_text += f"{category}: {pct:.1f}%\n"
    
    ax4.text(0.1, 0.5, summary_text, fontsize=13, family='monospace', va='center', 
             fontweight='bold')
    
    fig.suptitle('Agentic-PR Review Pattern Analysis', 
                 fontsize=20, fontweight='bold', y=0.995)
    
    plt.savefig('figures/q2_review_overview.png', bbox_inches='tight', dpi=300)
    plt.close()


def generate_all_visualizations(df):
    """
    Generate all visualizations for PR review metrics
    
    Args:
        df: DataFrame with PR review metrics
    
    Returns:
        bool: True if successful
    """
    logger = logging.getLogger(__name__)
    
    logger.info("\n" + "-"*70)
    logger.info("GENERATING VISUALIZATIONS")
    logger.info("-"*70)
    
    # Create output directory
    os.makedirs('figures', exist_ok=True)
    
    # Setup plot style
    setup_plot_style()
    
    # Generate all plots
    try:
        plot_category_distribution(df)
        plot_comments_per_pr(df)
        plot_category_heatmap(df)
        plot_primary_category_pie(df)
        plot_review_overview(df)
        
        logger.info(f"✓ All visualizations saved to: figures/")
        return True
    
    except Exception as e:
        logger.error(f"✗ Error generating visualizations: {e}")
        logger.error(f"  Error type: {type(e).__name__}")
        return False

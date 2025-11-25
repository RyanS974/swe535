"""
Phase 3: Generate Visualizations
Creates publication-quality plots of PR metrics (additions, deletions, files touched)
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


def generate_all_visualizations(df):
    """
    Generate all visualizations for PR metrics
    
    Args:
        df: DataFrame with PR metrics
    
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
    
    # 1. Additions Distribution
    logger.info("  Creating: additions_distribution.png")
    plot_additions_distribution(df)
    
    # 2. Deletions Distribution
    logger.info("  Creating: deletions_distribution.png")
    plot_deletions_distribution(df)
    
    # 3. Files Touched Distribution
    logger.info("  Creating: files_distribution.png")
    plot_files_distribution(df)
    
    # 4. PR Size Distribution
    logger.info("  Creating: size_distribution.png")
    plot_size_distribution(df)
    
    # 5. Combined Overview
    logger.info("  Creating: pr_metrics_overview.png")
    plot_combined_overview(df)
    
    logger.info(f"✓ All visualizations saved to: figures/")
    
    return True


def plot_additions_distribution(df):
    """Plot distribution of additions per PR"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Linear scale (clipped for visibility)
    ax.hist(df['total_additions'].clip(upper=1000), bins=50, edgecolor='black', alpha=0.7, linewidth=1.5)
    ax.set_xlabel('Lines Added per PR', fontsize=16, fontweight='bold')
    ax.set_ylabel('Number of PRs', fontsize=16, fontweight='bold')
    ax.set_title('Distribution of Additions per PR\n(Clipped at 1000 lines for visibility)', 
                 fontsize=18, fontweight='bold', pad=15)
    ax.axvline(df['total_additions'].median(), color='red', linestyle='--', linewidth=3,
                label=f'Median: {df["total_additions"].median():.0f}')
    ax.legend(fontsize=14, frameon=True, shadow=True)
    ax.grid(True, alpha=0.3, linewidth=1)
    
    plt.tight_layout()
    plt.savefig('figures/additions_distribution.png', bbox_inches='tight')
    plt.close()


def plot_deletions_distribution(df):
    """Plot distribution of deletions per PR"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Linear scale (clipped)
    ax.hist(df['total_deletions'].clip(upper=500), bins=50, edgecolor='black', alpha=0.7, 
            color='orange', linewidth=1.5)
    ax.set_xlabel('Lines Deleted per PR', fontsize=16, fontweight='bold')
    ax.set_ylabel('Number of PRs', fontsize=16, fontweight='bold')
    ax.set_title('Distribution of Deletions per PR\n(Clipped at 500 lines for visibility)', 
                 fontsize=18, fontweight='bold', pad=15)
    ax.axvline(df['total_deletions'].median(), color='red', linestyle='--', linewidth=3,
                label=f'Median: {df["total_deletions"].median():.0f}')
    ax.legend(fontsize=14, frameon=True, shadow=True)
    ax.grid(True, alpha=0.3, linewidth=1)
    
    plt.tight_layout()
    plt.savefig('figures/deletions_distribution.png', bbox_inches='tight')
    plt.close()


def plot_files_distribution(df):
    """Plot distribution of files touched per PR"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Clip at 50 files for better visualization
    files_clipped = df['files_touched'].clip(upper=50)
    ax.hist(files_clipped, bins=50, edgecolor='black', alpha=0.7, color='green', linewidth=1.5)
    ax.set_xlabel('Files Touched per PR', fontsize=16, fontweight='bold')
    ax.set_ylabel('Number of PRs', fontsize=16, fontweight='bold')
    ax.set_title('Distribution of Files Touched per PR\n(Clipped at 50 files for visibility)', 
                 fontsize=18, fontweight='bold', pad=15)
    ax.axvline(df['files_touched'].median(), color='red', linestyle='--', linewidth=3,
               label=f'Median: {df["files_touched"].median():.0f}')
    ax.legend(fontsize=14, frameon=True, shadow=True)
    ax.grid(True, alpha=0.3, linewidth=1)
    
    plt.tight_layout()
    plt.savefig('figures/files_distribution.png', bbox_inches='tight')
    plt.close()


def plot_size_distribution(df):
    """Plot PR size category distribution"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    size_order = ['XS', 'S', 'M', 'L', 'XL']
    size_counts = df['size_category'].value_counts()
    size_counts = size_counts.reindex(size_order)
    
    bars = ax.bar(size_counts.index, size_counts.values, edgecolor='black', alpha=0.7, linewidth=2)
    
    # Add percentages on bars with larger font
    for i, (cat, count) in enumerate(size_counts.items()):
        pct = (count / len(df)) * 100
        ax.text(i, count + 500, f'{pct:.1f}%', ha='center', va='bottom', 
                fontweight='bold', fontsize=15)
    
    ax.set_xlabel('PR Size Category', fontsize=16, fontweight='bold')
    ax.set_ylabel('Number of PRs', fontsize=16, fontweight='bold')
    ax.set_title('Distribution of PR Sizes', fontsize=18, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.3, linewidth=1, axis='y')
    
    # Add legend explaining categories with larger text
    legend_text = 'XS: <10 lines\nS: 10-100 lines\nM: 100-500 lines\nL: 500-1000 lines\nXL: >1000 lines'
    ax.text(0.98, 0.97, legend_text, transform=ax.transAxes,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5, linewidth=2),
            fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/size_distribution.png', bbox_inches='tight')
    plt.close()


def plot_combined_overview(df):
    """Create a combined overview figure with key metrics"""
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.35)
    
    # Row 1: Three distributions
    # 1. Additions histogram
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.hist(df['total_additions'].clip(upper=1000), bins=30, edgecolor='black', alpha=0.7, linewidth=1.5)
    ax1.set_xlabel('Lines Added', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Count', fontsize=14, fontweight='bold')
    ax1.set_title('Additions Distribution', fontsize=15, fontweight='bold', pad=10)
    ax1.axvline(df['total_additions'].median(), color='red', linestyle='--', linewidth=3)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(labelsize=12)
    
    # 2. Deletions histogram
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.hist(df['total_deletions'].clip(upper=500), bins=30, edgecolor='black', alpha=0.7, 
             color='orange', linewidth=1.5)
    ax2.set_xlabel('Lines Deleted', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Count', fontsize=14, fontweight='bold')
    ax2.set_title('Deletions Distribution', fontsize=15, fontweight='bold', pad=10)
    ax2.axvline(df['total_deletions'].median(), color='red', linestyle='--', linewidth=3)
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(labelsize=12)
    
    # 3. Files histogram
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.hist(df['files_touched'].clip(upper=50), bins=30, edgecolor='black', alpha=0.7, 
             color='green', linewidth=1.5)
    ax3.set_xlabel('Files Touched', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Count', fontsize=14, fontweight='bold')
    ax3.set_title('Files Distribution', fontsize=15, fontweight='bold', pad=10)
    ax3.axvline(df['files_touched'].median(), color='red', linestyle='--', linewidth=3)
    ax3.grid(True, alpha=0.3)
    ax3.tick_params(labelsize=12)
    
    # Row 2: Size category bar chart (spans all columns)
    ax4 = fig.add_subplot(gs[1, :])
    size_order = ['XS', 'S', 'M', 'L', 'XL']
    size_counts = df['size_category'].value_counts().reindex(size_order)
    bars = ax4.bar(size_counts.index, size_counts.values, edgecolor='black', alpha=0.7, linewidth=2)
    for i, (cat, count) in enumerate(size_counts.items()):
        pct = (count / len(df)) * 100
        ax4.text(i, count, f'{pct:.1f}%', ha='center', va='bottom', 
                fontweight='bold', fontsize=14)
    ax4.set_xlabel('PR Size Category', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Number of PRs', fontsize=14, fontweight='bold')
    ax4.set_title('PR Size Distribution', fontsize=15, fontweight='bold', pad=10)
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.tick_params(labelsize=12)
    
    # Add summary statistics text box with larger font
    summary_text = (
        f"Dataset Summary:\n"
        f"Total PRs: {len(df):,}\n"
        f"Total Additions: {df['total_additions'].sum():,}\n"
        f"Total Deletions: {df['total_deletions'].sum():,}\n"
        f"Total Files: {df['files_touched'].sum():,}\n\n"
        f"Per-PR Medians:\n"
        f"Additions: {df['total_additions'].median():.0f}\n"
        f"Deletions: {df['total_deletions'].median():.0f}\n"
        f"Files: {df['files_touched'].median():.0f}"
    )
    ax4.text(0.98, 0.97, summary_text, transform=ax4.transAxes,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8, linewidth=2),
            fontsize=12, family='monospace', fontweight='bold')
    
    fig.suptitle('Agentic-PR Metrics Overview', fontsize=20, fontweight='bold', y=0.995)
    
    plt.savefig('figures/pr_metrics_overview.png', bbox_inches='tight')
    plt.close()

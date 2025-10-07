"""
MSR 2026 Mining Challenge - Agentic PR Analysis
Main entry point with menu system and global state management

Question 1: How do Agentic-PRs change code?
Question 2: What aspects of Agentic-PRs receive most attention during review?
"""

import os
import sys
from utils.logging_config import setup_logging
from phase1 import run_phase1
from phase2 import run_phase2

# ============================================================================
# GLOBAL STATE - Persists across menu selections
# ============================================================================
dataset_state = {
    'configs': {},           # Will hold multiple configs: {'pull_request': dataset, ...}
    'active_config': None,   # Currently selected config
    'metadata': {}           # Metadata about loaded configs
}

pr_metrics_df = None  # Will hold extracted metrics (Phase 2)
analysis_results = None  # Will hold analysis results (Phase 3)

# Configuration mappings for MSR Challenge
PHASE_CONFIG_MAP = {
    'phase1': {
        'question': 'Question 1: How do Agentic-PRs change code?',
        'configs': ['pull_request', 'pr_commit_details'],
        'primary': 'pull_request',
        'metrics_config': 'pr_commit_details'
    },
    'phase2': {
        'question': 'Question 2: What aspects receive most attention during review?',
        'configs': ['pr_review_comments', 'pr_reviews', 'pr_comments'],
        'primary': 'pr_review_comments'
    }
}

# ============================================================================
# MENU SYSTEM
# ============================================================================
def display_menu():
    """Display main menu with current state indicators"""
    print("\n" + "="*70)
    print("MSR 2026 - Agentic PR Analysis")
    print("="*70)
    
    # Show current state
    loaded_configs = list(dataset_state.get('configs', {}).keys())
    has_configs = len(loaded_configs) > 0
    metrics_extracted = pr_metrics_df is not None
    analysis_done = analysis_results is not None
    
    print("\n[CURRENT STATE]")
    print(f"  Configs loaded: {len(loaded_configs)}")
    if has_configs:
        for config_name in loaded_configs:
            records = dataset_state['metadata'].get(f'{config_name}_records', 0)
            cache_status = dataset_state['metadata'].get(f'{config_name}_cache_status', 'unknown')
            print(f"    - {config_name}: {records:,} records ({cache_status})")
    else:
        print("    No configs loaded yet")
    
    print(f"  Metrics extracted: {'✓ Yes' if metrics_extracted else '✗ No'}")
    if metrics_extracted:
        print(f"    Rows in metrics: {len(pr_metrics_df):,}")
    print(f"  Analysis complete: {'✓ Yes' if analysis_done else '✗ No'}")
    
    print("\n[MENU OPTIONS]")
    print("1. Phase 1: Dataset Exploration (Question 1)")
    print("2. Phase 2: Data Extraction (Question 1)")
    print("3. Phase 3: Analysis & Visualization")
    print("4. Exit")
    print("\n" + "-"*70)


def phase1_handler():
    """Handle Phase 1 execution - Question 1 dataset exploration"""
    
    phase_info = PHASE_CONFIG_MAP['phase1']
    
    print("\n" + "="*70)
    print("PHASE 1: DATASET EXPLORATION")
    print("="*70)
    print(f"Research Question: {phase_info['question']}")
    print(f"Required Configs:")
    for config in phase_info['configs']:
        print(f"  - {config}")
    print("="*70)
    
    # Load both configs needed for Question 1
    configs_to_load = phase_info['configs']
    
    for config_name in configs_to_load:
        # Check if already loaded
        if config_name in dataset_state.get('configs', {}):
            print(f"\n✓ Config '{config_name}' already loaded in memory")
            continue
        
        print(f"\nLoading config: {config_name}")
        
        success = run_phase1(dataset_state, config_name=config_name)
        
        if not success:
            print(f"\n✗ Failed to load config: {config_name}")
            print("Check the log file for details: msr_analysis.log")
            input("\nPress Enter to return to menu...")
            return
    
    print("\n" + "="*70)
    print("✓ Phase 1 completed successfully!")
    print("="*70)
    print("All required configs loaded:")
    for config in configs_to_load:
        if config in dataset_state.get('configs', {}):
            records = dataset_state['metadata'].get(f'{config}_records', 0)
            print(f"  ✓ {config}: {records:,} records")
    print("\nDataset is now ready for Phase 2 (Data Extraction)")
    input("\nPress Enter to return to menu...")


def phase2_handler():
    """Handle Phase 2 execution - Extract per-PR metrics"""
    global pr_metrics_df
    
    phase_info = PHASE_CONFIG_MAP['phase1']  # Using phase1 config for Question 1
    
    print("\n" + "="*70)
    print("PHASE 2: DATA EXTRACTION")
    print("="*70)
    print(f"Research Question: {phase_info['question']}")
    print("="*70)
    
    # Check if required configs are loaded
    required_configs = phase_info['configs']
    missing_configs = []
    
    for config in required_configs:
        if config not in dataset_state.get('configs', {}):
            missing_configs.append(config)
    
    if missing_configs:
        print("\n✗ Error: Required configs not loaded!")
        print(f"Missing: {', '.join(missing_configs)}")
        print("\nPlease run Phase 1 first to load the required datasets.")
        input("\nPress Enter to return to menu...")
        return
    
    print("\nAll required configs are loaded. Starting extraction...")
    
    # Run Phase 2 extraction
    success, metrics_df = run_phase2(dataset_state)
    
    if success and metrics_df is not None:
        pr_metrics_df = metrics_df
        
        print("\n" + "="*70)
        print("✓ Phase 2 completed successfully!")
        print("="*70)
        print(f"Extracted metrics for {len(pr_metrics_df):,} PRs")
        print(f"\nMetrics DataFrame columns:")
        for col in pr_metrics_df.columns:
            print(f"  - {col}")
        print(f"\nData saved to: pr_metrics.csv")
        print("\nReady for Phase 3 (Analysis & Visualization)")
        input("\nPress Enter to return to menu...")
    else:
        print("\n" + "="*70)
        print("✗ Phase 2 encountered errors")
        print("="*70)
        print("Check the log file for details: msr_analysis.log")
        input("\nPress Enter to return to menu...")


def phase3_handler():
    """Handle Phase 3 execution - Analysis & Visualization"""
    global analysis_results
    
    if pr_metrics_df is None:
        print("\n✗ Error: Metrics not extracted!")
        print("Please run Phase 2 first.")
        input("\nPress Enter to return to menu...")
        return
    
    print("\n" + "="*70)
    print("PHASE 3: ANALYSIS & VISUALIZATION")
    print("="*70)
    print(f"Analyzing {len(pr_metrics_df):,} PRs")
    print("This will generate:")
    print("  - Statistical analysis (text report)")
    print("  - 5 visualizations (PNG files)")
    print("="*70)
    
    proceed = input("\nProceed with analysis? (Y/n): ").strip().lower()
    if proceed and proceed not in ['y', 'yes', '']:
        print("Analysis cancelled.")
        input("\nPress Enter to return to menu...")
        return
    
    # Run Phase 3
    from phase3 import run_phase3
    success = run_phase3(pr_metrics_df)
    
    if success:
        analysis_results = True
        
        print("\n" + "="*70)
        print("✓ Phase 3 completed successfully!")
        print("="*70)
        print("\nGenerated outputs:")
        print("  📊 Visualizations:")
        print("     - figures/additions_distribution.png")
        print("     - figures/deletions_distribution.png")
        print("     - figures/files_distribution.png")
        print("     - figures/pr_metrics_overview.png")
        print("\n  📄 Report:")
        print("     - analysis_summary.txt (detailed statistics)")
        print("\nThese outputs answer Question 1 for our MSR 2026 paper.")
        input("\nPress Enter to return to menu...")
    else:
        print("\n" + "="*70)
        print("✗ Phase 3 encountered errors")
        print("="*70)
        print("Check the log file for details: msr_analysis.log")
        input("\nPress Enter to return to menu...")


def main():
    """Main program loop"""
    # Setup logging
    log_file = "msr_analysis.log"
    setup_logging(log_file)
    
    print("\n" + "="*70)
    print("MSR 2026 Mining Challenge Analysis Tool")
    print("="*70)
    print(f"Working directory: {os.getcwd()}")
    print(f"Log file: {log_file}")
    print("\nAll operations will be logged to the console and log file.")
    
    # Main menu loop
    while True:
        try:
            display_menu()
            choice = input("Select option (1-4): ").strip()
            
            if choice == "1":
                phase1_handler()
            elif choice == "2":
                phase2_handler()
            elif choice == "3":
                phase3_handler()
            elif choice == "4":
                print("\n" + "="*70)
                print("Exiting MSR Analysis Tool")
                print("="*70)
                print("Thank you for using the tool!")
                break
            else:
                print("\n✗ Invalid option. Please select 1-4.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("Program interrupted by user (Ctrl+C)")
            print("="*70)
            break
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            print(f"Error type: {type(e).__name__}")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
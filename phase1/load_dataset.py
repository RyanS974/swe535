"""
Phase 1 - Step 1: Load Dataset from HuggingFace
Handles dataset downloading/loading with cache detection
"""

import logging
from pathlib import Path
from datasets import load_dataset, get_dataset_config_names
import os


def check_config_cache_status(dataset_name, config_name, cache_dir):
    """
    Check if a specific config is cached locally
    
    Args:
        dataset_name: Name of the dataset (e.g., 'hao-li/AIDev')
        config_name: Configuration name
        cache_dir: Local cache directory path
    
    Returns:
        tuple: (is_cached: bool, cache_path: str or None)
    """
    if not os.path.exists(cache_dir):
        return False, None
    
    # Look for this specific config in cache
    cache_path = Path(cache_dir)
    
    # HuggingFace cache structure: datasets/dataset_name/config_name/
    dataset_simple_name = dataset_name.split('/')[-1]  # 'AIDev'
    
    # Search for config directories
    config_dirs = list(cache_path.glob(f"**/{dataset_simple_name}/**/{config_name}*"))
    
    if config_dirs:
        return True, str(config_dirs[0])
    
    return False, None


def load_dataset_step(dataset_state, config_name='pull_request', current_phase='Phase 1'):
    """
    Step 1: Load dataset from HuggingFace with local cache
    
    Args:
        dataset_state: Dictionary to store dataset and metadata
        config_name: Dataset configuration to load (default: 'pull_request')
        current_phase: Which phase is requesting this (for logging)
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    logger.info("\n" + "-"*70)
    logger.info("[STEP 1/4] LOAD DATASET FROM HUGGINGFACE")
    logger.info("-"*70)
    
    dataset_name = "hao-li/AIDev"
    
    # Use local cache directory in project folder
    local_cache_dir = os.path.join(os.getcwd(), '.cache', 'huggingface', 'datasets')
    
    logger.info(f"Dataset: {dataset_name}")
    logger.info(f"Config: {config_name}")
    logger.info(f"Cache location: {local_cache_dir}")
    
    # Check if this specific config is cached locally
    is_cached, cache_path = check_config_cache_status(dataset_name, config_name, local_cache_dir)
    
    if is_cached:
        logger.info(f"✓ Config '{config_name}' found in local cache - loading from disk...")
    else:
        logger.info(f"Downloading config '{config_name}' from HuggingFace...")
        logger.info("  (First download may take a minute)")
        logger.info(f"  Will be cached to: {local_cache_dir}")
    
    logger.info("")
    
    try:
        # Load dataset with specific config and local cache directory
        dataset = load_dataset(
            dataset_name, 
            config_name,
            cache_dir=local_cache_dir
        )
        
        logger.info("✓ Dataset loaded successfully!")
        logger.info(f"  Available splits: {list(dataset.keys())}")
        
        # Log size of each split
        total_records = 0
        for split_name, split_data in dataset.items():
            num_records = len(split_data)
            total_records += num_records
            logger.info(f"  - Split '{split_name}': {num_records:,} records")
        
        # Store dataset in state (support multiple configs)
        if 'configs' not in dataset_state:
            dataset_state['configs'] = {}
        
        dataset_state['configs'][config_name] = dataset
        dataset_state['active_config'] = config_name
        
        # Update metadata
        if 'metadata' not in dataset_state:
            dataset_state['metadata'] = {}
        
        dataset_state['metadata']['dataset_name'] = dataset_name
        dataset_state['metadata']['cache_dir'] = local_cache_dir
        dataset_state['metadata']['loaded_configs'] = list(dataset_state['configs'].keys())
        dataset_state['metadata'][f'{config_name}_records'] = total_records
        dataset_state['metadata'][f'{config_name}_splits'] = list(dataset.keys())
        
        # Cache status for this config
        cache_status = 'cached' if is_cached else 'downloaded'
        dataset_state['metadata'][f'{config_name}_cache_status'] = cache_status
        
        # For backwards compatibility with Phase 1 code
        dataset_state['dataset'] = dataset
        dataset_state['metadata']['total_records'] = total_records
        dataset_state['metadata']['config_name'] = config_name
        dataset_state['metadata']['splits'] = list(dataset.keys())
        dataset_state['metadata']['cache_status'] = cache_status
        
        logger.info(f"\n✓ Step 1 Complete - Config '{config_name}' ready ({total_records:,} records)")
        
        return True
        
    except ValueError as e:
        # Handle missing config error specifically
        error_msg = str(e)
        if "Config name is missing" in error_msg or "available configs" in error_msg:
            logger.error(f"✗ Configuration error: '{config_name}' not found")
            logger.error(f"  The dataset requires a valid config name")
            
            # Try to get available configs
            try:
                available_configs = get_dataset_config_names(dataset_name)
                logger.error(f"\n  Available configs ({len(available_configs)}):")
                for config in available_configs:
                    logger.error(f"    - {config}")
            except:
                logger.error(f"  Could not retrieve available configs list")
            
            return False
        else:
            # Other ValueError
            logger.error(f"✗ Failed to load dataset: {e}")
            logger.error(f"  Error type: {type(e).__name__}")
            return False
            
    except Exception as e:
        logger.error(f"✗ Failed to load dataset: {e}")
        logger.error(f"  Error type: {type(e).__name__}")
        logger.error(f"  Error details: {str(e)}")
        return False

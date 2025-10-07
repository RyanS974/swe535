"""
Shared logging configuration for MSR Analysis
Provides consistent logging setup across all modules
"""

import logging
import sys
from pathlib import Path


def setup_logging(log_file="msr_analysis.log", level=logging.INFO):
    """
    Setup logging to both console and file (overwrite mode)
    
    Args:
        log_file: Path to log file (default: msr_analysis.log)
        level: Logging level (default: INFO)
    
    Returns:
        Logger instance
    """
    # Remove existing handlers to avoid duplicates
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Create formatter with timestamp
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler (overwrite mode)
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Console handler with color-friendly output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    logging.root.setLevel(level)
    logging.root.addHandler(file_handler)
    logging.root.addHandler(console_handler)
    
    # Log initialization
    logging.info("="*70)
    logging.info(f"Logging initialized - Output to console and {log_file}")
    logging.info("="*70)
    
    return logging.getLogger()


def get_logger(name):
    """
    Get a logger instance for a specific module
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

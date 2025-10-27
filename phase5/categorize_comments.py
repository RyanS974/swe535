"""
Phase 5: Comment Categorization
Keyword-based classification of review comments into categories
"""

import logging

# Comprehensive keyword dictionary for each category
CATEGORY_KEYWORDS = {
    'correctness': [
        # Bugs and errors
        'bug', 'error', 'issue', 'problem', 'fail', 'crash', 'broken',
        'incorrect', 'wrong', 'invalid', 'exception', 'throw',
        
        # Logic issues
        'logic', 'algorithm', 'implementation', 'behavior', 'expected',
        'edge case', 'boundary', 'corner case', 'overflow', 'underflow',
        
        # Null and undefined
        'null', 'undefined', 'none', 'nil', 'empty',
        'null pointer', 'null reference', 'npe',
        
        # Concurrency issues  
        'race condition', 'deadlock', 'thread safe', 'synchronize',
        'infinite loop', 'memory leak', 'resource leak', 'leak'
    ],
    
    'style': [
        # Naming
        'name', 'naming', 'rename', 'variable name', 'function name',
        'class name', 'method name', 'constant name',
        'camelcase', 'snake_case', 'pascalcase', 'kebab-case',
        
        # Formatting
        'format', 'formatting', 'indent', 'indentation', 'whitespace',
        'spacing', 'newline', 'blank line', 'line length',
        
        # Readability
        'readable', 'readability', 'clarity', 'clear', 'confusing',
        'comment', 'documentation', 'doc string', 'docstring',
        
        # Code quality
        'clean code', 'refactor', 'simplify', 'complexity',
        'duplication', 'dry', 'convention', 'style guide', 'linter',
        'lint', 'prettier', 'formatter'
    ],
    
    'security': [
        # Vulnerabilities
        'vulnerability', 'vulnerabilities', 'vulnerable', 'exploit',
        'attack', 'injection', 'xss', 'cross site scripting',
        'sql injection', 'csrf', 'cross site request forgery',
        
        # Authentication & Authorization
        'authentication', 'authorization', 'auth', 'permission',
        'access control', 'privilege', 'role', 'user rights',
        
        # Sensitive data
        'password', 'secret', 'key', 'token', 'credential',
        'sensitive', 'private', 'confidential', 'pii',
        'personal information', 'encryption', 'decrypt', 'hash',
        
        # Security practices
        'security', 'secure', 'sanitize', 'validate input',
        'escape', 'encode', 'unsafe', 'insecure'
    ],
    
    'testing': [
        # Test types
        'test', 'tests', 'testing', 'unit test', 'integration test',
        'e2e', 'end to end', 'acceptance test', 'regression test',
        
        # Test components
        'test case', 'test suite', 'test coverage', 'coverage',
        'mock', 'stub', 'fixture', 'test data',
        
        # Test assertions
        'assert', 'assertion', 'expect', 'should', 'verify',
        
        # Test issues
        'missing test', 'no test', 'untested', 'test fail',
        'flaky test', 'flaky', 'edge case test'
    ]
}


def classify_comment(comment_text):
    """
    Classify a comment into one of five categories using keyword matching
    
    Args:
        comment_text: String containing comment body
    
    Returns:
        str: Category name ('correctness', 'style', 'security', 'testing', 'other')
    """
    if not comment_text or not isinstance(comment_text, str):
        return 'other'
    
    # Convert to lowercase for matching
    text_lower = comment_text.lower()
    
    # Count keyword matches per category
    category_scores = {
        'correctness': 0,
        'style': 0,
        'security': 0,
        'testing': 0
    }
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                category_scores[category] += 1
    
    # Find category with highest score
    max_score = max(category_scores.values())
    
    # If no matches, return 'other'
    if max_score == 0:
        return 'other'
    
    # Return category with highest score
    # In case of tie, use priority order: correctness > security > testing > style
    priority = ['correctness', 'security', 'testing', 'style']
    for cat in priority:
        if category_scores[cat] == max_score:
            return cat
    
    return 'other'


def categorize_all_comments(pr_comments_dict):
    """
    Classify all comments for all PRs
    
    Args:
        pr_comments_dict: Dictionary {pr_id: [comment1, comment2, ...]}
    
    Returns:
        dict: {pr_id: {category: count}} with counts per category per PR
    """
    logger = logging.getLogger(__name__)
    
    logger.info("Classifying comments into categories...")
    logger.info("Categories: correctness, style, security, testing, other")
    logger.info("")
    
    category_counts = {}
    total_comments = 0
    processed = 0
    
    # Calculate total comments for progress tracking
    for comments in pr_comments_dict.values():
        total_comments += len(comments)
    
    logger.info(f"Total comments to classify: {total_comments:,}")
    logger.info("")
    
    # Classify all comments
    for pr_id, comments in pr_comments_dict.items():
        # Initialize category counts for this PR
        counts = {
            'correctness': 0,
            'style': 0,
            'security': 0,
            'testing': 0,
            'other': 0
        }
        
        # Classify each comment
        for comment in comments:
            category = classify_comment(comment)
            counts[category] += 1
            processed += 1
            
            # Progress logging
            if processed % 10000 == 0:
                logger.info(f"  Classified {processed:,} / {total_comments:,} comments...")
        
        category_counts[pr_id] = counts
    
    logger.info(f"✓ Classified all {total_comments:,} comments")
    logger.info(f"✓ Processed {len(category_counts):,} PRs")
    logger.info("")
    
    # Log category distribution summary
    total_by_category = {
        'correctness': 0,
        'style': 0,
        'security': 0,
        'testing': 0,
        'other': 0
    }
    
    for counts in category_counts.values():
        for category, count in counts.items():
            total_by_category[category] += count
    
    logger.info("Category distribution across all comments:")
    for category in ['correctness', 'style', 'security', 'testing', 'other']:
        count = total_by_category[category]
        pct = (count / total_comments * 100) if total_comments > 0 else 0
        logger.info(f"  {category.capitalize()}: {count:,} ({pct:.1f}%)")
    logger.info("")
    
    return category_counts

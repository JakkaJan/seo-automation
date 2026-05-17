"""
Pseudo-visibility calculator based on GSC data.
Weights are configurable via .env
"""
from src.config.settings import VISIBILITY_WEIGHTS
from src.utils.logger import get_logger

logger = get_logger(__name__)

def get_position_weight(position: float) -> float:
    """
    Get weight for a given position based on configured thresholds.

    Args:
        position: Average position from GSC

    Returns:
        Weight coefficient
    """
    if position <= 3:
        return VISIBILITY_WEIGHTS['top3']
    elif position <= 10:
        return VISIBILITY_WEIGHTS['top10']
    elif position <= 30:
        return VISIBILITY_WEIGHTS['top30']
    else:
        return VISIBILITY_WEIGHTS['other']

def calculate_visibility_score(impressions: int, position: float) -> float:
    """
    Calculate visibility score for a single query.

    Formula: impressions × weight(position)

    Args:
        impressions: Number of impressions
        position: Average position

    Returns:
        Visibility score contribution
    """
    weight = get_position_weight(position)
    return impressions * weight

def calculate_aggregate_visibility(data: list) -> float:
    """
    Calculate aggregate visibility score from list of query data.

    Args:
        data: List of dicts with 'impressions' and 'position' keys

    Returns:
        Normalized visibility score (0-100 scale)
    """
    if not data:
        return 0.0

    total_weighted = 0
    total_impressions = 0

    for item in data:
        impressions = item.get('impressions', 0)
        position = item.get('position', 100)

        weighted = calculate_visibility_score(impressions, position)
        total_weighted += weighted
        total_impressions += impressions

    if total_impressions == 0:
        return 0.0

    # Normalize to 0-100 scale
    # Max possible score = all impressions × top3 weight
    max_possible = total_impressions * VISIBILITY_WEIGHTS['top3']
    if max_possible == 0:
        return 0.0

    score = (total_weighted / max_possible) * 100
    return round(score, 2)


if __name__ == '__main__':
    # Test
    test_data = [
        {'impressions': 1000, 'position': 2.5},
        {'impressions': 500, 'position': 8.0},
        {'impressions': 200, 'position': 25.0},
    ]
    score = calculate_aggregate_visibility(test_data)
    print(f"Test visibility score: {score}")

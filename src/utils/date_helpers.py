"""
Date utility functions for weekly reporting.
"""
from datetime import datetime, timedelta
from typing import Tuple

def get_last_week_range(reference_date: datetime = None) -> Tuple[str, str]:
    """
    Get date range for the previous week (Monday to Sunday).
    Returns tuple of (start_date, end_date) as ISO format strings.
    """
    if reference_date is None:
        reference_date = datetime.now()

    # Get last Sunday
    last_sunday = reference_date - timedelta(days=reference_date.weekday() + 1)
    # Get Monday before that Sunday
    last_monday = last_sunday - timedelta(days=6)

    return last_monday.strftime('%Y-%m-%d'), last_sunday.strftime('%Y-%m-%d')

def get_weeks_ago(weeks: int = 1, reference_date: datetime = None) -> str:
    """Get date N weeks ago."""
    if reference_date is None:
        reference_date = datetime.now()
    target = reference_date - timedelta(weeks=weeks)
    return target.strftime('%Y-%m-%d')

def get_current_week_label(reference_date: datetime = None) -> str:
    """Get human-readable week label like '13-19 May 2026'."""
    if reference_date is None:
        reference_date = datetime.now()

    start, end = get_last_week_range(reference_date)
    start_dt = datetime.strptime(start, '%Y-%m-%d')
    end_dt = datetime.strptime(end, '%Y-%m-%d')

    if start_dt.month == end_dt.month:
        return f"{start_dt.day}-{end_dt.day} {end_dt.strftime('%B %Y')}"
    else:
        return f"{start_dt.day} {start_dt.strftime('%b')} - {end_dt.day} {end_dt.strftime('%b %Y')}"

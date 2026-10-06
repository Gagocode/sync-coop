from datetime import datetime, timedelta, timezone

from repositories import user_repository


def current_activity_timestamp():
    """SQLite timestamp format, always UTC, with second precision."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def record_activity(user_id):
    user_repository.update_last_activity(user_id, current_activity_timestamp())


def calculate_engagement(last_activity_at, now=None):
    if last_activity_at is None:
        return "inactive"
    now = now or datetime.now(timezone.utc)
    activity = datetime.fromisoformat(last_activity_at).replace(tzinfo=timezone.utc)
    elapsed = now - activity
    if elapsed <= timedelta(days=7):
        return "active"
    if elapsed <= timedelta(days=15):
        return "attention"
    return "inactive"

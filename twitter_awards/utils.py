from datetime import datetime
import calendar


def get_db_of_followers(followers, operations):
    db = dict()
    for follower in followers:
        follower_id = follower["id"]
        db[follower_id] = follower
        db[follower_id]["id"] = follower_id
        for label, _ in operations:
            db[follower_id][label] = 0
    return db


def get_month_interval(year, timezone):
    """
    For every month in the year, get the start and last day
    """
    result = []
    for month in range(1, 13):
        _, last_day = calendar.monthrange(year, month)
        first_date = timezone.localize(datetime(year, month, 1, 0, 0, 0))
        last_date = timezone.localize(datetime(year, month, last_day, 23, 59, 59))
        result += [(first_date.isoformat(), last_date.isoformat())]
    return result

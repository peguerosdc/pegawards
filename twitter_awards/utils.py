from datetime import datetime
import calendar


def get_db_of_followers(followers):
    db = dict()
    for follower in followers:
        follower_id = follower["id"]
        db[follower_id] = follower
        db[follower_id]["RTs"] = 0
        db[follower_id]["replies"] = 0
        db[follower_id]["quotes"] = 0
        db[follower_id]["favs"] = 0
    return db


def get_month_interval(year, timezone):
    """
    For every month in the year, get the start and last day
    """
    result = []
    for month in range(1, 13):
        _, last_day = calendar.monthrange(year, month)
        first_date = datetime(year, month, 1, tzinfo=timezone)
        last_date = datetime(year, month, last_day, tzinfo=timezone)
        result += [(first_date.isoformat(), last_date.isoformat())]
    return result

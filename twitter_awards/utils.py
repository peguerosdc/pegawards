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


def get_month_interval():
    return [
        ("2020-01-01", "2020-01-31"),
        ("2020-02-01", "2020-02-29"),
        ("2020-03-01", "2020-03-31"),
        ("2020-04-01", "2020-04-30"),
        ("2020-05-01", "2020-05-31"),
        ("2020-06-01", "2020-06-30"),
        ("2020-07-01", "2020-07-31"),
        ("2020-08-01", "2020-08-31"),
        ("2020-09-01", "2020-09-31"),
        ("2020-10-01", "2020-10-31"),
        ("2020-11-01", "2020-11-30"),
        ("2020-12-01", "2020-12-31"),
    ]
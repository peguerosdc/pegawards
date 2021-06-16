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
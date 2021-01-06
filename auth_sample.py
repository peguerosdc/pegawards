from twitter_client import TwitterClient

def get_api_keys():
    import os
    keys = {
        "TWITTER_API_KEY" : os.getenv("TWITTER_API_KEY"),
        "TWITTER_API_KEY_SECRET" : os.getenv("TWITTER_API_KEY_SECRET"),
        "TWITTER_ACCESS_TOKEN" : os.getenv("TWITTER_ACCESS_TOKEN"),
        "TWITTER_ACCESS_TOKEN_SECRET" : os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    }
    # Check that all the keys are set
    if not (keys["TWITTER_API_KEY"] and keys["TWITTER_API_KEY_SECRET"]
        and keys["TWITTER_ACCESS_TOKEN"] and keys["TWITTER_ACCESS_TOKEN_SECRET"]):
        raise NameError("Twitter API keys not found as environment variables. See README for instructions.")
    # If the keys are ok, proceed
    return keys


if __name__ == '__main__':
    # Get Twitter client with the current API keys
    keys = get_api_keys()
    client = TwitterClient(keys["TWITTER_API_KEY"], keys["TWITTER_API_KEY_SECRET"],
            keys["TWITTER_ACCESS_TOKEN"], keys["TWITTER_ACCESS_TOKEN_SECRET"])
    # Print the users metadata as an example
    user = client.me()
    print(f"User: {user['name']} ({user['id']}). Followers: {user['followers_count']}")
    # Start creating a DB with the followers
    db = dict()
    for follower in client.get_followers():
        follower_id = follower['id']
        db[follower_id] = follower
        db[follower_id]['RTs'] = 0
        db[follower_id]['replies'] = 0
        db[follower_id]['quotes'] = 0
        db[follower_id]['favs'] = 0

    # Get stats of every tweet in the timeline
    i = 0
    for tweet in client.get_tweets():
        print(tweet)

        # Get retweeters of this tweet
        for retweeter in client.get_retweeters(tweet['id']):
            # Update count in the db only for my followers
            if retweeter in db:
                db[retweeter]['RTs'] += 1

        # Get Favs
        # TODO

        # Get replies
        # TODO

        # Get Quotes
        # TODO

        i += 1
        if i==19:
            break

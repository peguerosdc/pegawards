from twitter_awards.client import TwitterClient
from twitter_awards import utils


def get_api_keys():
    import os

    keys = {
        "TWITTER_API_KEY": os.getenv("TWITTER_API_KEY"),
        "TWITTER_API_KEY_SECRET": os.getenv("TWITTER_API_KEY_SECRET"),
        "TWITTER_ACCESS_TOKEN": os.getenv("TWITTER_ACCESS_TOKEN"),
        "TWITTER_ACCESS_TOKEN_SECRET": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        "TWITTER_X_CSRF_TOKEN": os.getenv("TWITTER_X_CSRF_TOKEN"),
        "TWITTER_AUTHORIZATION": os.getenv("TWITTER_AUTHORIZATION"),
        "TWITTER_COOKIE": os.getenv("TWITTER_COOKIE"),
    }
    # Check that all the keys are set
    if not (
        keys["TWITTER_API_KEY"]
        and keys["TWITTER_API_KEY_SECRET"]
        and keys["TWITTER_ACCESS_TOKEN"]
        and keys["TWITTER_ACCESS_TOKEN_SECRET"]
        and keys["TWITTER_X_CSRF_TOKEN"]
        and keys["TWITTER_AUTHORIZATION"]
        and keys["TWITTER_COOKIE"]
    ):
        raise NameError(
            "Twitter API keys not found as environment variables. See README for instructions."
        )
    # If the keys are ok, proceed
    return keys


def get_my_client():
    keys = get_api_keys()
    return TwitterClient(
        keys["TWITTER_API_KEY"],
        keys["TWITTER_API_KEY_SECRET"],
        keys["TWITTER_ACCESS_TOKEN"],
        keys["TWITTER_ACCESS_TOKEN_SECRET"],
        keys["TWITTER_X_CSRF_TOKEN"],
        keys["TWITTER_AUTHORIZATION"],
        keys["TWITTER_COOKIE"],
    )


def get_current_timezone():
    import pytz

    return pytz.timezone("America/Mexico_City")


if __name__ == "__main__":
    # Get Twitter client with the current API keys
    client = get_my_client()
    # Print the users metadata as an example
    user = client.me()
    print(f"User: {user['name']} ({user['id']}). Followers: {user['followers_count']}")
    # Start creating a DB with the followers
    db = utils.get_db_of_followers(client.get_followers())

    # List of possible operations that the user can perform on every tweet
    operations = [
        ("quotes", client.get_quotes),
        ("replies", client.get_replies),
        ("RTs", client.get_retweeters),
        ("favs", client.get_tweet_favs),
    ]
    # Get the list of months
    months = utils.get_month_interval(2021, get_current_timezone())
    start_time, end_time = months[0][0], months[7][1]
    # Start retrieving stats of every tweet based on the possible operations to perform
    print(
        "Getting tweets with their respecive ",
        ", ".join([o for o, _ in operations]),
        f"{'from '+start_time+' to '+end_time if start_time and end_time else ''}",
        "...",
    )
    for tweet in client.get_tweets(start_time, end_time):
        tweet_id = tweet["id"]
        # Count the amount of interactions per tweet just for debugging purpouses
        interactions = dict()
        # Check which users performed every operation and store the counts in a dict()
        for label, operation in operations:
            interactions[label] = 0
            for candidate in operation(tweet_id):
                # Update count in the db only for my followers
                if candidate in db:
                    db[candidate][label] += 1
                    interactions[label] += 1
        print(
            f"[{tweet_id}]: ",
            ", ".join([f"{i}={interactions[i]}" for i in interactions]),
        )

from twitter_awards.file_helper import TweetsWriter
from twitter_awards.client import TwitterClient
from twitter_awards import utils
import argparse
import logging
from datetime import datetime


def set_up_logging(month, year):
    logging.basicConfig(
        filename=f"./data/log_{month}_{year}.txt",
        filemode="w",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )
    logging.info(f"Log file with metadata from {month}/{year}")


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


def create_parser():
    parser = argparse.ArgumentParser(
        description="Download your tweets and its metadata of a given month/year"
    )
    parser.add_argument(
        "month",
        metavar="m",
        type=int,
        choices=list(range(1, 13)),
        help="Month [1,2,3,4,5,6,7,8,9,10,11,12]",
    )
    parser.add_argument("year", metavar="y", type=int, help="Year")
    return parser


def get_created_at_nth(created_at):
    d = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
    return d.strftime("%d")


def print_tweet(tweet, interactions):
    message = (
        f"[{tweet['id']}/{get_created_at_nth(tweet['created_at'])}th]: "
        + ",\t".join(
            [
                f"{i}={interactions[i]}/{tweet['public_metrics'][i]}"
                for i in interactions
            ]
        )
    )
    print(message)
    logging.info(message)


if __name__ == "__main__":
    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()
    # Get Twitter client with the current API keys
    client = get_my_client()
    # Print the users metadata as an example
    user = client.me()
    print(f"User: {user['name']} ({user['id']}). Followers: {user['followers_count']}")
    # List of possible operations that the user can perform on every tweet
    operations = [
        ("quote_count", client.get_quotes),
        ("reply_count", client.get_replies),
        ("retweet_count", client.get_retweeters),
        ("like_count", client.get_tweet_favs),
    ]
    # Start creating a DB with the followers
    db = utils.get_db_of_followers(client.get_followers(), operations)
    # Get the list of months
    months = utils.get_month_interval(args.year, get_current_timezone())
    start_time, end_time = months[args.month - 1][0], months[args.month - 1][1]
    # Start retrieving stats of every tweet based on the possible operations to perform
    print(
        "Getting tweets with their respective ",
        ", ".join([o for o, _ in operations]),
        f"{'from '+start_time+' to '+end_time if start_time and end_time else ''}",
        "...",
    )
    # set up logging
    set_up_logging(args.month, args.year)
    with TweetsWriter(
        f"./data/{args.month}_{args.year}_tweets.csv",
        f"./data/{args.month}_{args.year}_followers.csv",
        operations,
    ) as tweets_metrics_file:
        # Start getting tweets
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
            # Print and log results
            print_tweet(tweet, interactions)
            # Save public metrics of this tweet
            tweets_metrics_file.write_tweet(tweet)
        # Write the results of the followers
        for follower_id in db:
            tweets_metrics_file.write_follower(db[follower_id])
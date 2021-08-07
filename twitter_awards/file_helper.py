import pandas as pd


def is_tweet_mine(user, tweet):
    # check if the tweet is a RT or if it is original
    if tweet["text"].startswith("RT"):
        if not tweet["text"].startswith(f"RT @{user['screen_name']}"):
            return 0
    return 1


class TweetsWriter(object):
    def __init__(self, user, metrics_path, followers_path, operations):
        self.user = user
        # create pandas dateframe for metrics
        self.metrics_path = metrics_path
        self.operations = [label for label, _ in operations]
        try:
            self.metrics = pd.read_csv(metrics_path)
        except:
            self.metrics = pd.DataFrame(
                columns=["id", "timestamp", "is_mine"] + self.operations
            )
        # create pandas dateframe for followers
        self.followers_path = followers_path
        try:
            self.followers = pd.read_csv(followers_path)
        except:
            self.followers = pd.DataFrame(columns=["id"] + self.operations)

    def write_tweet(self, tweet):
        # build object to store in the dataframe
        data = {
            "id": tweet["id"],
            "timestamp": tweet["created_at"],
            "is_mine": is_tweet_mine(self.user, tweet),
        }
        for op in self.operations:
            data[op] = tweet["public_metrics"][op]
        # append to the dataframe
        self.metrics = self.metrics.append(data, ignore_index=True)
        # save
        self.metrics.to_csv(self.metrics_path, index=False)

    def write_follower(self, follower):
        # build object to store in the dataframe
        data = {"id": follower["id"]}
        for op in self.operations:
            data[op] = follower[op]
        # append to the dataframe
        self.followers = self.followers.append(data, ignore_index=True)
        # save
        self.followers.to_csv(self.followers_path, index=False)
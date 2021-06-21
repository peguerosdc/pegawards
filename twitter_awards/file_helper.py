class TweetsWriter(object):
    def __init__(self, metrics_path, followers_path):
        self.metrics_path = metrics_path
        self.followers_path = followers_path

    def __enter__(self):
        self.metrics_file = open(self.metrics_path, "w")
        self.followers_file = open(self.followers_path, "w")
        # Store metrics of tweets for analysis
        self.metrics_file.write(
            "id,timestamp,like_count,reply_count,retweet_count,quote_count\n"
        )
        self.followers_file.write(
            "id,like_count,reply_count,retweet_count,quote_count\n"
        )
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.metrics_file.close()
        self.followers_file.close()

    def write_tweet(self, tweet):
        self.metrics_file.write(
            f"{tweet['id']},{tweet['created_at']},{tweet['public_metrics']['like_count']},{tweet['public_metrics']['reply_count']},{tweet['public_metrics']['retweet_count']},{tweet['public_metrics']['quote_count']}\n"
        )

    def write_follower(self, follower):
        self.followers_file.write(
            f"{follower['id']},{follower['favs']},{follower['replies']},{follower['RTs']},{follower['quotes']}\n"
        )
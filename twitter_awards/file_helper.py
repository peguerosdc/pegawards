class TweetsWriter(object):
    def __init__(self, metrics_path, followers_path, operations):
        self.metrics_path = metrics_path
        self.followers_path = followers_path
        self.operations = [label for label, _ in operations]

    def __enter__(self):
        self.metrics_file = open(self.metrics_path, "w")
        self.followers_file = open(self.followers_path, "w")
        # Store metrics of tweets for analysis
        self.metrics_file.write(f"id,timestamp,{','.join(self.operations)}\n")
        self.followers_file.write(f"id,{','.join(self.operations)}\n")
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.metrics_file.close()
        self.followers_file.close()

    def write_tweet(self, tweet):
        operations_data = ",".join(
            [str(tweet["public_metrics"][op]) for op in self.operations]
        )
        self.metrics_file.write(
            f"{tweet['id']},{tweet['created_at']},{operations_data}\n"
        )

    def write_follower(self, follower):
        operations_data = ",".join([str(follower[op]) for op in self.operations])
        self.followers_file.write(f"{follower['id']},{operations_data}\n")

from .twitter_scrapper import TwitterScrapper
from .twitter_api import MyTwitterAPI


class TwitterClient(object):
    def __init__(
        self,
        api_key,
        api_key_secret,
        access_token,
        access_token_secret,
        csrf_token,
        authorization,
        cookie,
    ):
        self.api = MyTwitterAPI(
            api_key, api_key_secret, access_token, access_token_secret
        )
        # Init users data as it will be used in later requests
        self.me(refresh=True)
        self.scrapper = TwitterScrapper(
            self.me()["id"], csrf_token, authorization, cookie
        )

    def me(self, refresh=False):
        """ Request the data of the user matching this ACCESS_TOKEN and ACCESS_TOKEN_SECRET """
        if refresh:
            self.metadata = self.api.me()
        return self.metadata

    def get_followers(self):
        return self.api.get_followers(self.metadata["id"])

    def get_tweets(self, start_time=None, end_time=None):
        return self.api.get_tweets(
            self.metadata["id"], start_time=start_time, end_time=end_time
        )

    def get_tweet_favs(self, tweet_id):
        return self.api.get_tweet_favs(tweet_id)

    def get_retweeters(self, tweet_id):
        return self.api.get_retweeters(tweet_id)

    def get_quotes(self, tweet_id):
        return self.scrapper.get_quotes(tweet_id)

    def get_replies(self, tweet_id):
        return self.scrapper.get_replies(tweet_id)

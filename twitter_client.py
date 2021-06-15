from TwitterAPI import TwitterAPI, TwitterPager


class TwitterClient(object):
    def __init__(self, api_key, api_key_secret, access_token, access_token_secret):
        self.api1 = TwitterAPI(
            api_key,
            api_key_secret,
            access_token,
            access_token_secret,
            api_version="1.1",
            auth_type="oAuth1",
        )
        self.api2 = TwitterAPI(
            api_key,
            api_key_secret,
            access_token,
            access_token_secret,
            api_version="2",
            auth_type="oAuth1",
        )
        # Init users data as it will be used in later requests
        self.me(refresh=True)

    def me(self, refresh=False):
        """ Request the data of the user matching this ACCESS_TOKEN and ACCESS_TOKEN_SECRET """
        if refresh:
            req = self.api1.request(
                "account/verify_credentials",
                params={
                    "include_entities": False,
                    "skip_status": True,
                    "include_email": False,
                },
            )
            if req.status_code != 200:
                raise ValueError("Twitter credentials not valid. Unable to verify user")
            data = req.response.json()
            # Update the cache
            self.metadata = data
        return self.metadata

    def get_followers(self, page_size=1000):
        """Use v2 endpoint to get the followers of this account. Followers are paginated by the max amount which is 1000
        See:
        https://developer.twitter.com/en/docs/twitter-api/users/follows/quick-start
        """

        def request_followers(next_token=None):
            req = self.api2.request(
                f"users/:{self.metadata['id']}/followers",
                params={"max_results": page_size, "pagination_token": next_token},
            )
            response = req.response.json()
            return response.get("data", []), response.get("meta", dict())

        # Start returning followers
        followers, meta = request_followers()
        while followers:
            for item in followers:
                yield item
            # Request more followers
            next_token = meta.get("next_token")
            if next_token:
                followers, meta = request_followers(next_token)
            else:
                followers = []

    def get_tweets(self, page_size=100):
        def request_tweets(next_token=None):
            req = self.api2.request(
                f"users/:{self.metadata['id']}/tweets",
                params={
                    "max_results": page_size,
                    "pagination_token": next_token,
                    "tweet.fields": "in_reply_to_user_id",
                },
            )
            response = req.response.json()
            return response.get("data", []), response.get("meta", dict())

        # Start returning tweets
        tweets, meta = request_tweets()
        while tweets:
            for item in tweets:
                yield item
            # Request more tweets
            next_token = meta.get("next_token")
            if next_token:
                tweets, meta = request_tweets(next_token)
            else:
                tweets = []

    def get_tweet_favs(self, tweet_id):
        # Get the list of users who liked this tweet
        req = self.api2.request(f"tweets/:{tweet_id}/liking_users")
        res = req.response.json()
        return [user["id"] for user in res.get("data", [])]

    def get_retweeters(self, tweet_id):
        # Get the list of everyone who has retweeted this tweet
        req = self.api1.request(
            f"statuses/retweeters/ids",
            params={"id": tweet_id, "count": 100, "stringify_ids": True},
        )
        res = req.response.json()
        return res.get("ids", [])

    def get_quotes(self, tweet_id):
        req = self.api1.request(f"search/tweets", params={"q": tweet_id})
        # TODO
        return []

    def get_replies(self, tweet_id):
        # Consider this tweet is the beginning of a conversation
        data = self.api2.request(
            f"tweets/:{tweet_id}", params={"tweet.fields": "conversation_id"}
        ).response.json()
        # conversation_id = data['data'].get('conversation_id', None)
        # if conversation_id:
        # get thread
        # thread_data = self.api.request(f"tweets/search/recent", params={'query': f"conversation_id:{tweet_id}"}, api_version="2").response.json()

    def get_replies_to_me(self):
        username = self.metadata["screen_name"]
        # try to get next reply
        pager = TwitterPager(
            self.api, "search/tweets", {"q": f"to:{username} filter:replies"}
        )
        for reply in pager.get_iterator():
            yield reply

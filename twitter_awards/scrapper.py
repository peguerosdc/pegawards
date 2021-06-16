import requests


def find_cursor(data):
    """
    Finds the cursor (if any) as seen in the Twitter's website response on June 2021 to paginate the results
    """
    cursor_candidates = data["timeline"]["instructions"]
    for candidate in cursor_candidates:
        if "replaceEntry" in candidate:
            instruction = candidate["replaceEntry"]
            if instruction["entryIdToReplace"] == "sq-cursor-bottom":
                return instruction["entry"]["content"]["operation"]["cursor"]["value"]
    return None


def build_url_with_cursor(base_url, cursor):
    """
    Builds a URL with the given cursor
    """
    return f"{base_url}&cursor={cursor}" if cursor else base_url


class TwitterScrapper:
    def __init__(self, csrf_token, authorization, cookie):
        self.csrf_token = csrf_token
        self.authorization = authorization
        self.cookie = cookie

    def get_quotes(self, tweet_id):
        """
        For the given tweet, retrieves the list of user_ids of users that have quoted this tweet
        """

        def perform_request(cursor=None):
            # Build url with cursor
            url = build_url_with_cursor(
                "https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q=quoted_tweet_id%3A"
                + tweet_id
                + "&vertical=tweet_detail_quote&count=20&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel",
                cursor,
            )
            # Build and perform the request from "copy as nodes fetch"
            headers = {
                "x-csrf-token": self.csrf_token,
                "authorization": self.authorization,
                "x-twitter-auth-type": "OAuth2Session",
                "cookie": self.cookie,
            }
            req = requests.get(url, headers=headers)
            data = req.json()
            # Get users who have quoted each tweet by iterating the global list of tweets.count()
            # This allows multiple quotes per user in contrast with only checking the list ofusers,
            # which will mistakely count 1 quote per user in the case there are more
            tweets = data["globalObjects"]["tweets"]
            users = [
                tweets[tweet_id]["user_id_str"]
                for tweet_id in tweets
                if tweets[tweet_id].get("is_quote_status", False)
            ]
            # Perform the next request until the users response is empty, which indicates the end of the results
            if users:
                next_cursor = find_cursor(data)
                if next_cursor:
                    return users + perform_request(tweet_id, next_cursor)

        return perform_request()

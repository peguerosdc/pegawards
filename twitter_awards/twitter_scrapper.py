import requests
import time


def find_cursors_in_reply(data):
    """
    Finds the cursor (if any) as seen in the Twitter's website response on June 2021 to paginate the results
    """
    cursors = []
    cursor_candidates = data["timeline"]["instructions"]
    for candidate in cursor_candidates:
        if "addEntries" in candidate:
            entries = candidate["addEntries"].get("entries", [])
            for entry in entries:
                items = (
                    entry.get("content", dict())
                    .get("timelineModule", dict())
                    .get("items", [])
                )
                for item in items:
                    item_content = item.get("item", dict()).get("content", dict())
                    timelineCursor = item_content.get("timelineCursor", dict())
                    if timelineCursor.get("cursorType", "") == "ShowMore":
                        cursors += [timelineCursor["value"]]
    return cursors


def find_cursor_in_quote(data):
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
    def __init__(
        self, user_id, csrf_token, authorization, cookie, cooldown_time_ms=4000
    ):
        self.user_id = str(user_id)
        self.csrf_token = csrf_token
        self.authorization = authorization
        self.cookie = cookie
        # value used to prevent the API from overheating
        self.last_request_timestamp = None
        self.cooldown_time_ms = cooldown_time_ms

    def _call_twitter_inner_api(self, base_url, cursor=None):
        # Build url with cursor
        url = build_url_with_cursor(
            base_url,
            cursor,
        )
        # Build and perform the request from "copy as nodes fetch"
        headers = {
            "x-csrf-token": self.csrf_token,
            "authorization": self.authorization,
            "x-twitter-auth-type": "OAuth2Session",
            "cookie": self.cookie,
        }
        # Perform the request and let some time to cool down
        try:
            req = requests.get(url, headers=headers)
            time.sleep(self.cooldown_time_ms / 1000)
            data = req.json()
        except Exception as e:
            data = None
        return data

    def get_quotes(self, tweet_id):
        """
        For the given tweet, retrieves the list of user_ids of users that have quoted this tweet
        """

        def perform_request(tweet_id, cursor=None):
            data = self._call_twitter_inner_api(
                "https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q=quoted_tweet_id%3A"
                + tweet_id
                + "&vertical=tweet_detail_quote&count=20&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel",
                cursor,
            )
            # Get users who have quoted each tweet by iterating the global list of tweets.count()
            # This allows multiple quotes per user in contrast with only checking the list ofusers,
            # which will mistakely count 1 quote per user in the case there are more
            tweets = data["globalObjects"]["tweets"]
            users = [
                tweets[temp_id]["user_id_str"]
                for temp_id in tweets
                if tweets[temp_id].get("is_quote_status", False)
            ]
            # Perform the next request until the users response is empty, which indicates the end of the results
            if users:
                next_cursor = find_cursor_in_quote(data)
                if next_cursor:
                    return users + perform_request(tweet_id, next_cursor)
            # If there are no users, stop requesting more
            return users

        return perform_request(tweet_id)

    def get_replies(self, tweet_id):
        """
        For the given tweet, simulate the action of going to its site and expanding the conversation
        for every reply (i.e. clicking on "Get more replies")
        """

        def perform_request(tweet_id, cursor=None):
            data = self._call_twitter_inner_api(
                f"https://twitter.com/i/api/2/timeline/conversation/{tweet_id}.json?include_profile_interstitial_type=0&include_blocking=0&include_blocked_by=0&include_followed_by=1&include_want_retweets=1&include_mute_edge=0&include_can_dm=0&include_can_media_tag=0&skip_status=1&cards_platform=Web-12&include_cards=0&include_ext_alt_text=false&include_quote_count=false&include_reply_count=1&tweet_mode=extended&include_entities=false&include_user_entities=true&include_ext_media_color=false&include_ext_media_availability=false&send_error_codes=true&simple_quoted_tweet=true&referrer=me&count=20&include_ext_has_birdwatch_notes=false&ext=mediaStats%2ChighlightedLabel",
                cursor,
            )
            users = []
            # For each tweet, check if it is a reply to the current user (me)
            tweets = data["globalObjects"]["tweets"]
            for temp_id in tweets:
                tweet = tweets[temp_id]
                in_reply_to_id = tweet.get("in_reply_to_user_id_str", None)
                in_reply_to_status_id = tweet.get("in_reply_to_status_id_str", None)
                owner_id = tweet.get("user_id_str", None)
                # Check if it is a reply to me and to this tweet and count it
                is_reply_to_me = (
                    in_reply_to_id == self.user_id
                    and owner_id
                    and owner_id != self.user_id
                )
                is_reply_to_tweet = in_reply_to_status_id == tweet_id
                if is_reply_to_me and is_reply_to_tweet:
                    users.append(tweet["user_id_str"])
            return users

        return perform_request(tweet_id)
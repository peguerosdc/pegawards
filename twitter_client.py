from TwitterAPI import TwitterAPI

class TwitterClient(object):

    def __init__(self, api_key, api_key_secret, access_token, access_token_secret):
        self.api = TwitterAPI(api_key, api_key_secret, access_token, access_token_secret, auth_type='oAuth1')
        # Init users data as it will be used in later requests
        self.me(refresh=True)

    def me(self, refresh=False):
        """ Request the data of the user matching this ACCESS_TOKEN and ACCESS_TOKEN_SECRET """
        if refresh:
            req = self.api.request('account/verify_credentials', params={'include_entities':False, 'skip_status': True, 'include_email':False}, api_version='1.1')
            if req.status_code != 200:
                raise ValueError("Twitter credentials not valid. Unable to verify user")
            data = req.response.json()
            # Update the cache
            self.metadata = data
        return self.metadata
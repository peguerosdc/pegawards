from TwitterAPI import TwitterAPI
from twitter_client import TwitterClient

def get_api_keys():
    import os
    keys = {
        "TWITTER_API_KEY" : os.getenv("TWITTER_API_KEY"),
        "TWITTER_API_KEY_SECRET" : os.getenv("TWITTER_API_KEY_SECRET"),
        "TWITTER_ACCESS_TOKEN" : os.getenv("TWITTER_ACCESS_TOKEN"),
        "TWITTER_ACCESS_TOKEN_SECRET" : os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    }
    # Check that all the keys are set
    if not (keys["TWITTER_API_KEY"] and keys["TWITTER_API_KEY_SECRET"]
        and keys["TWITTER_ACCESS_TOKEN"] and keys["TWITTER_ACCESS_TOKEN_SECRET"]):
        raise NameError("Twitter API keys not found as environment variables. See README for instructions.")
    # If the keys are ok, proceed
    return keys


if __name__ == '__main__':
    # Get Twitter client with the current API keys
    keys = get_api_keys()
    client = TwitterClient(keys["TWITTER_API_KEY"], keys["TWITTER_API_KEY_SECRET"],
            keys["TWITTER_ACCESS_TOKEN"], keys["TWITTER_ACCESS_TOKEN_SECRET"])
    # Print the users metadata as an example
    user = client.me()
    print(f"User: {user['name']} ({user['id']}). Followers: {user['followers_count']}")
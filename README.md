# Pegawards
Finds the followers with whom you interact the most via Favs, Replies, RTs or RT+Quotes according to a scoring function

## Set up

Set your Twitter API keys as environment variables. See `pegawards.env` for an example or modify it and run `. ./pegawards.env`

There are some requests not allowed by Twitter's API (such as retrieving the quoted tweets and an infinite amount of replies) that need to be scrapped.

To set up the scrapper, go to [Twitter](www.twitter.com) (while logged in) from any website and by inspecting any request, retrieve the following elements from the `Request Headers`:

* x-csrf-token
* authorization
* cookie

And set them as environment variables (again, see `pegawards.env` for an example). **Please note that `COOKIE` must be set with single quotes**.
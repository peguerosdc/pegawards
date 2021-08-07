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

## Usage

### Download your data

First, run `data_collector.py` to download your tweets and its metadata:

````
$ python data_collector.py --help
usage: data_collector.py [-h] m y

Download your tweets and its metadata from a given month/year

positional arguments:
  m           Month [1,2,3,4,5,6,7,8,9,10,11,12]
  y           Year

optional arguments:
  -h, --help  show this help message and exit
````

Some recommendations:

* Run month by month to prevent the Twitter Scrapper from failing

### Analysis

See the Jupyter notebooks for some use-cases.

## License

Licensed under the [MIT License](https://github.com/peguerosdc/pegawards/blob/master/LICENSE). Only for educational purposes.
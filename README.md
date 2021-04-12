# Birdwatching - Creepy Twitter Stalking & More

## Step 0: Secrets
Grab your Twitter Access Token, Consumer Key & Secrets and kindly place them in *secrets.py*.

## Step 1: Fetch
Supply the target Twitter accounts in *accounts.txt* and their tweets shall be crawled and passed on to the modules for further analysis. One account per-line, line comments with *'#'* are supported.

## Step 2: Modules
Modules in the *modules* directory will be run for each crawled tweet. The current modules are:

### Geolocation Analysis
Tweets featuring geolocation info will be analyzed and pinpointed to an address using the OpenStreet API. Twitter remembers the option to geotag your current tweet, which is carried on to future Tweets by default, unless it is disabled explicitly. Creepy.

### URL Takeovers
Birdwatching will watch out for Tweets containing links to unregistered domains. The identified domains can be registered, to host new content, and the old tweets can be given a new meaning. Creepy (not Twitter's fault though).

### Source Analysis
Birdwatching will keep an eye out for Tweets from sources (web, mobile, Tweetdeck, etc.) that stand out and display crawled tweets from those sources. 

## But that sounds creepy!
I know, the tool is not meant for stalking the online presence of Twitter users, but to raise awareness about the abuses mentioned above. Please remember to disable unintended geolocation tagging. :)

## How?
Tweepy for fetching, OpenStreetMap for resolving map data.

## Such a great idea!
Geolocation Analysis is ubiquitous, Source Analysis is kind of neat but not really and Tweet URL Takeover is not my idea but I cannot find the original article that mentioned it. If I do, I will make sure to credit the author here.



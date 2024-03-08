AUTH_URL = "https://twitter.com/i/oauth2/authorize"
TOKEN_URL = "https://api.twitter.com/2/oauth2/token"
POST_TWEET_URL = "https://api.twitter.com/2/tweets"

# have added the scopes for the twitter api. offline.access is added to refresh the token
SCOPES = ["tweet.read", "users.read", "tweet.write", "offline.access"]

import requests
import os
import json
import snscrape.modules.twitter as sntwitter
import pandas as pd
import re

bearer_token = os.environ.get("BEARER_TOKEN")


def writeTweets(username, keyword):

    query = f"(from:@{username})"
    tweets = []
    limit = 100

    if keyword:

        for tweet in sntwitter.TwitterSearchScraper(query + f" {keyword.lower()}").get_items():

            if len(tweets) == limit:
                break
            tweets.append([tweet.date, tweet.user.username, tweet.url, tweet.content])

    else:
        for tweet in sntwitter.TwitterSearchScraper(query).get_items():

            if len(tweets) == limit:
                break
            tweets.append([tweet.date, tweet.user.username, tweet.url, tweet.content])

    return tweets


def create_url():
    user_id = str(input("Enter user ID: "))
    return f"https://api.twitter.com/2/users/{user_id}/following"


def get_params():
    return {"user.fields": "created_at"}


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def extract_format_date(text):
    final = text


def main():

    url = create_url()
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    tweets = []

    keyword = str(input("Keyword: "))

    for OBJ in json_response['data']:
        tweets += writeTweets(OBJ['username'], keyword)

    df = pd.DataFrame(tweets, columns=['Date', 'Username', 'URL', 'Tweet'])
    df.to_csv("outfile.csv", index=False)


if __name__ == "__main__":
    main()

import requests
import os
import json
import snscrape.modules.twitter as sntwitter
import pandas as pd
import re

bearer_token = os.environ.get("BEARER_TOKEN")

def writeTweets(username, limit, keywords=""):

    query = f"(from:@{username})"
    tweets = []

    if not limit:
        limit = 10

    if keywords:
        if "," in keywords:
            keywords = "(" + " OR ".join([keyword.strip()
                                          for keyword in keywords.split(',')]) + ")"

    for tweet in sntwitter.TwitterSearchScraper(query + (str(keywords) if keywords else "")).get_items():
        if len(tweets) == limit:
            break
        tweets.append([tweet.date, tweet.user.username,
                      tweet.url, tweet.content])

    return tweets


def create_url():
    user_id = str(input("*REQUIRED* Enter user ID: ")).strip()

    if not user_id:
        print("| ID is required! |")
        quit()

    return f"https://api.twitter.com/2/users/{user_id}/following"


def get_params():
    return {"user.fields": "created_at"}


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token.strip()}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request(
        "GET", url, auth=bearer_oauth, params=get_params())
    if response.status_code != 200:
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}"
        )
    return response.json()


def main():

    if not bearer_token:
        print(
            '''
            ____________________
           
            Bearer token not set!
            ____________________

          In your project root, use
       export BEARER_TOKEN=<token here>     
            '''
        )

    else:

        url = create_url()
        json_response = connect_to_endpoint(url)
        tweets = []

        keywords = str(input("*OPTIONAL* Keyword(s) (separate with ,): "))
        limit = int(input("*OPTIONAL* Tweet Limit/Person: "))

        for account in json_response['data']:
            tweets += writeTweets(account['username'], limit, keywords)

        df = pd.DataFrame(tweets, columns=['Date', 'Username', 'URL', 'Tweet'])
        df.to_csv("results.csv", index=False)


if __name__ == "__main__":
    main()

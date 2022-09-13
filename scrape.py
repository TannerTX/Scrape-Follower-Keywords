import twint
import requests
import os
import json


bearer_token = os.environ.get("BEARER_TOKEN")


def writeTweets(username):
    c = twint.Config()
    c.Lang = "en"
    c.Username = "OldBurnsy2"
    c.Hide_output = True
    c.Pandas = True
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df

    outFile = open('out.txt', 'w+')

    for idx, row in Tweets_df.iterrows():
        print(f"{row.username} : {row.tweet}")

    outFile.close()


def create_url():
    user_id = str(input("Enter user ID: "))
    return f"https://api.twitter.com/2/users/{user_id}/followers"


def get_params():
    return {"user.fields": "created_at"}


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():

    url = create_url()
    params = get_params()
    json_response = connect_to_endpoint(url, params)

    for OBJ in json_response['data']:
        print(OBJ['username'])


if __name__ == "__main__":
    main()

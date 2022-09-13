const needle = require('needle')
const fs = require('fs')
require('dotenv').config()

const userId = `722509609202614272`
const follower_url = `https://api.twitter.com/2/users/${userId}/followers`
const tweet_url = `https://api.twitter.com/2/users/${userId}/tweets`
const bearerToken = process.env.BEARER_TOKEN

const getFollowers = async () => {
    let users = []
    let params = {
        "max_results": 1000,
        "user.fields": "created_at"
    }

    const options = {
        headers: {
            "User-Agent": "v2FollowersJS",
            "authorization": `Bearer ${bearerToken}`
        }
    }

    let hasNextPage = true
    let nextToken = null

    while (hasNextPage) {
        let resp = await getPage(params, options, nextToken)
        if (resp && resp.meta && resp.meta.result_count && resp.meta.result_count > 0) {
            if (resp.data) {
                tweetDict = {}

                for(const [IDX, OBJ] of resp.data.entries()) 
                    tweetDict[OBJ.username] = extractTweets(OBJ.id)
        
                // fs.writeFileSync('./data/data.txt', str)
                
            }
            if (resp.meta.next_token) {
                nextToken = resp.meta.next_token
            } else {
                hasNextPage = false
            }
        } else {
            hasNextPage = false
        }
    }

    // console.log(users)
    // console.log(`Got ${users.length} users.`)

}


const extractTweets = async (accountID) => {

}




const getPage = async (params, options, nextToken) => {
    if (nextToken) {
        params.pagination_token = nextToken
    }

    try {
        const resp = await needle('get', follower_url, params, options)

        if (resp.statusCode != 200) {
            console.log(`${resp.statusCode} ${resp.statusMessage}:\n${resp.body}`)
            return
        }
        return resp.body
    } catch (err) {
        throw new Error(`Request failed: ${err}`)
    }
}

getFollowers()
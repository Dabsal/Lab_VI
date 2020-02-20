import requests

def run_query(json, headers): # A simple function to use requests.post to make the API call. 

    request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        print(request.text)
        raise Exception("Query failed to run by returning code of {}. {}."
                        .format(request.status_code, json['query'],
                                json['variables']))

query = """
{
  search(query:"stars:>100", type:REPOSITORY, first:5){
    nodes{
      ... on Repository
      {
        nameWithOwner
        url
        primaryLanguage
        {
          name
        }
        acceptedPullRequests: pullRequests(states:MERGED)
        {
          totalCount
        }
        releases
        {
          totalCount
        }
        closedIssues: issues(states:CLOSED)
        {
          totalCount
        }
        totalIssues: issues
        {
          totalCount
        }
        createdAt
        updatedAt
      }
    }
  }
}
    """
finalQuery = query.replace("{AFTER}","")
json = {
    "query": finalQuery, "variables": {}
}

token = 'f240a57a8d0c05e66138eee8af013f036acd565f'
headers = {
    "Authorization": "Bearer " + token,
}

result = run_query(json, headers)
ans = result['data']['search']['nodes']

#if(result['data']['search']['pageInfo']['hasNextPage']):
#    finalQuery = query.replace("{AFTER}", ", after:\"" + result['data']['search']['pageInfo']['endCursor'] + "\"")
#    result = run_query(json, headers)
#    ans += result['data']['search']['nodes']

print(ans)

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
after = "null"
query = """
{
  search(query:"stars:>100", type:REPOSITORY, first:5{AFTER}){
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
    pageInfo{
      hasNextPage
      endCursor
    }
  }
}
    """
finalQuery = query.replace("{AFTER}", "")

json = {
    "query":finalQuery, "variables":{}
}

token = '020036ac3d6921485c40940f29d8bd7dc2afcbc0'
headers = {"Authorization": "Bearer " + token} 

total_pages = 1

result = run_query(json, headers)

nodes = result['data']['search']['nodes']
next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]

print ("\n\nFim da página 1\n\n")
#paginating
while (next_page and total_pages < 3):
    total_pages += 1
    cursor = result["data"]["search"]["pageInfo"]["endCursor"]
    next_query = query.replace("{AFTER}", ", after: \"%s\"" % cursor)
    json["query"] = next_query
    result = run_query(json, headers)
    nodes += result['data']['search']['nodes']
    next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]
    pagina = str(total_pages)    
    print("\n\nFim da página " + pagina + "\n\n")
#print(nodes)
for node in nodes:
    with open("/result.csv", 'a') as the_file:
        the_file.write(node['nameWithOwner'] + "\n") 

print("TERMINOU")

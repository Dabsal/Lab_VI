import requests
import time

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

token = ''
headers = {"Authorization": "Bearer " + token} 

total_pages = 1

result = run_query(json, headers)

nodes = result['data']['search']['nodes']
next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]

print ("\nFim da página 1")
#paginating
while (next_page and total_pages < 5):
    total_pages += 1
    cursor = result["data"]["search"]["pageInfo"]["endCursor"]
    next_query = query.replace("{AFTER}", ", after: \"%s\"" % cursor)
    json["query"] = next_query
    result = run_query(json, headers)
    nodes += result['data']['search']['nodes']
    next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]
    pagina = str(total_pages)    
    time.sleep(0.1)
    print("\nFim da página " + pagina)
#print(nodes)
linguagem = ''
with open("result.csv", 'a') as the_file:
    for node in nodes:
      if node['primaryLanguage']['name'] is not None:
        linguagem = str(node['primaryLanguage']['name'])
      else:
        linguagem = ''

        the_file.write(str(node['nameWithOwner']) + "\t" + str(node['primaryLanguage']['name']) + "\t" + str(node['acceptedPullRequests']['totalCount']) + "\t" + str(node['releases']['totalCount']) + "\t" + str(node['closedIssues']['totalCount']) + "\t" + str(node['totalIssues']['totalCount']) + "\t" + str(node['createdAt']) + "\t" + str(node['updatedAt']) + "\t" + "\n") 

print("TERMINOU")

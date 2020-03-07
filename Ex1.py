import requests
import time
import csv

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
  search(query:"stars:>100", type:REPOSITORY, first:10{AFTER}){
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
finalQuery = query.replace("{AFTER}", "") #Como é feito para pegar o ID da próxima página

json = {
    "query":finalQuery, "variables":{}
}

token = '8f4165a20ef8b7c0539bfdfc611bf8ee8337bee6' #Insira seu token da API do GitHub aqui
headers = {"Authorization": "Bearer " + token} 
#Primeira requisição dos dados
total_pages = 1

result = run_query(json, headers)

nodes = result['data']['search']['nodes']
next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]

print ("\nFim da página 1")
#Requisição em loop das páginas seguintes
while (next_page and total_pages < 100):
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
#--------------Construção do CSV
#Definindo o cabeçalho
with open("result.csv", 'w', newline='') as n_file:
  fnames = [
          'Nome/Dono;',
          'URL;',
          'Linguagem Primária;',
          'Pull Requests Aceitas;',
          'Releases;',
          'Issues Fechadas;',
          'Total de Issues;',
          'Data de Criação;',
          'Última Atualização;']

  csv_writer = csv.DictWriter(n_file, fieldnames=fnames, dialect="excel-tab")
  #Escrevendo o cabeçalho
  csv_writer.writeheader() 
  #Escrevendo os dados coletados
  for node in nodes:
      csv_writer.writerow(
          {
              'Nome/Dono;': "{};".format(node['nameWithOwner']),
              'URL;': "{};".format(node['url']),
              'Linguagem Primária;': "{};".format(node['primaryLanguage']['name'] if node['primaryLanguage']!= None else 'null'),
              'Pull Requests Aceitas;': "{};".format(node['acceptedPullRequests']['totalCount']),
              'Releases;': "{};".format(node['releases']['totalCount']),
              'Issues Fechadas;': "{};".format(node['closedIssues']['totalCount']),
              'Total de Issues;': "{};".format(node['totalIssues']['totalCount']),
              'Data de Criação;': "{};".format(node['createdAt']),
              'Última Atualização;': "{};".format(node['updatedAt'])
          })

#with open("result.csv", 'a') as the_file:
#    for node in nodes:
#      if len(node['primaryLanguage']['name']) != 0:
#        linguagem = str(node['primaryLanguage']['name'])
#      else:
#        linguagem = ''
#        the_file.write(str(node['nameWithOwner']) + "\t" + 
#        #str(node['primaryLanguage']['name']) + "\t" + 
#        linguagem + "\t" +
#        str(node['acceptedPullRequests']['totalCount']) + "\t" + 
#        str(node['releases']['totalCount']) + "\t" + 
#        str(node['closedIssues']['totalCount']) + "\t" + 
#        str(node['totalIssues']['totalCount']) + "\t" + 
#        str(node['createdAt']) + "\t" + 
#        str(node['updatedAt']) + "\t" + "\n") 

print("TERMINOU")

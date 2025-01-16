import boto3
import requests
from requests_aws4auth import AWS4Auth
import json

region = 'us-east-1'
service = 'es'
host = ''

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
url = f"{host}/_cat/indices?v" 
response = requests.get(url, auth=awsauth)

if response.status_code == 200:
    lines = response.text.splitlines()

    for line in lines[1:]:
        columns = line.split()
        index_name = columns[2]
else:
    print(f"Error: {response.status_code}, {response.text}")

index_name = ""
url = f"{host}/{index_name}/_search"  

query = {
    "query": {
        "match_all": {}
    }
}

response = requests.get(url, auth=awsauth, headers={"Content-Type": "application/json"}, data=json.dumps(query))

if response.status_code == 200:
    data = response.json()
    for doc in data['hits']['hits']:
        print(json.dumps(doc['_source']))
else:
    print(f"Error: {response.status_code}, {response.text}")
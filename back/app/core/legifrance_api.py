from os import name
import requests
import pandas as pd

from datetime import date
from urllib.parse import urlparse
from requests_oauthlib import OAuth2Session
from schema.document_schema import DocumentSchema

from config.helper import read_config

config = read_config()

# CONSTANTS
API_HOST       = config['APILegifrance']['hostapi']
TOKEN_URL      = config['APILegifrance']['urltoken']
BASE_URL       = config['APILegifrance']['urlbase']
ARTICLE_URL    = config['APILegifrance']['urlgetarticle']
CODE_URL       = config['APILegifrance']['urlgetcode']
LEGIFRANCE_URL = config['APILegifrance']['urlmain']
CLIENT_ID      = config['APILegifrance']['clientid']
CLIENT_SECRET  = config['APILegifrance']['clientsecret']
ALL_CODES_URL  = config['APILegifrance']['urlallcodes']

# METHODS

#Returns the authorisation token for the Legifrance API
def getToken(id, secret):
    res = requests.post(
        TOKEN_URL,
        data = {
            'grant_type': 'client_credentials',
            'client_id': id,
            'client_secret': secret,
            'scope': 'openid'
            }
        )
    token = res.json()
    client = OAuth2Session(id, token=token)
    clientToken = client.access_token
    return clientToken

def getHeaderPost(token):
    return {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

# Save a given json object into a file
# def jsonToFile(data, filename, indent):
#     json_string = json.dumps(data, indent=indent)
#     with open(filename, 'w') as outfile:
#         outfile.write(json_string)

# Get a code from the Legifrance API and returns it as a Json object    
def codeToJson(file_id):
    print(f"Getting document {file_id} from Legifrance API")
    token = getToken(CLIENT_ID, CLIENT_SECRET)

    res = requests.post(
        url = API_HOST + BASE_URL + CODE_URL,
        json = {
            'date': date.today().strftime("%Y-%m-%d"),
            'sctCid': file_id,
            'textId': file_id
        },
        headers = getHeaderPost(token)
    )
    if(res.status_code == 200):
        code = res.json()
        return code
    else:
        print('Error getting the file')
        return None
        
# Get the ID of a document given its URL
def getDocId(url):
    parsed_url = urlparse(url)
    if(parsed_url.netloc != LEGIFRANCE_URL):
        print(f'Only documents from {LEGIFRANCE_URL} can be downloaded')
        return None
    else:
        url_parts = parsed_url.path.split('/')
        id = (url_parts[-2].split('.'))[0]
        return id

# Get the articles from a document in the form of a json object
def getListeArticles(document):
    articles = pd.DataFrame(columns=['Name', 'Id', 'Cid'])
    for article in document['articles']:
        art_name = article['num']
        art_id = article['id']
        art_cid = article['cid']
        new_article = pd.DataFrame(
            {
                'Name': [art_name],
                'Id': [art_id],
                'Cid': [art_cid],
            }
        )
        articles = pd.concat([articles, new_article])
    for section in document['sections']:
        sub_articles = getListeArticles(section)
        articles = pd.concat([articles, sub_articles])
    return articles

# Get the text of an article from the Legifrance API given its id
def getArticleText(article_id):
    token = getToken(CLIENT_ID, CLIENT_SECRET)
    try:
        res = requests.post(
            url = API_HOST + BASE_URL + ARTICLE_URL,
            json = {
                'id': article_id
            },
            headers = getHeaderPost(token)
        )
        if(res.status_code == 200):
            article = res.json()
            return article['article']['texte']
    except:
        print(f'Error getting the article {article_id}')
        return None

def getAllCodes():
    token = getToken(CLIENT_ID, CLIENT_SECRET)
    res = requests.post(
        url = API_HOST + BASE_URL + ALL_CODES_URL,
        json = {
            'pageNumber': 1,
            'pageSize': 100,
            'states': [
                'VIGUEUR',
            ]
        },
        headers = getHeaderPost(token)
    )
    if(res.status_code == 200):
        all_codes = []
        codes = res.json()
        for code in codes['results']:
            code = DocumentSchema(
                doc_id = code['id'],
                name = code['titre'],
                path = code['pdfFilePath'],
                date = code['lastUpdate'],
                processed = False
            )
            all_codes.append(code)
        return sorted(all_codes, key=lambda x: x.date, reverse=True)
    else:
        print('Error getting the codes')
        return None

from datetime import datetime
from re import fullmatch

from numpy import NaN
from schema.article_schema import ArticleSchema
from schema.document_schema import DocumentSchema
from core.legifrance_api import codeToJson, getDocId, getListeArticles, getArticleText

# Returns a JSON representation of the document
def getDocument(url):
    #Extract the Document ID from the url 
    doc_id = getDocId(url)
    
    # Get the document from the API Legifrance
    document = codeToJson(doc_id)
    
    # The json object contains :
    # title: The title of the document
    # modifDate: The date of the document
    return document


# Returns a pandas dataframe containing the articles
def getDfArticles(document):
    iter = 0
    articles = getListeArticles(document)
    articles = articles.drop_duplicates().reset_index(drop=True)
    full_articles = articles.copy()
    full_articles['Text'] = None

    while full_articles['Text'].isnull().sum() > 0 and iter < 10:
        iter = iter + 1
        full_articles['Text'] = full_articles.Id.apply(lambda x : getArticleText(x)
                                                       if full_articles[full_articles['Id'] == x]['Text'].isnull().bool()
                                                       else full_articles.loc[full_articles['Id'] == x]['Text'].item()
                                                       )
        full_articles = full_articles.dropna(subset=['Text'])
    return full_articles

def jsonToDocument(doc) -> DocumentSchema:
    document = DocumentSchema(
        doc_id = doc['cid'],
        name = doc['title'],
        #path = url,
        date = datetime.strptime(doc['jurisDate'], '%Y-%m-%d'),
        processed = False
    )
    return document
    
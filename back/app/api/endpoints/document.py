import json

from typing import List
from sklearn import cluster

from sqlalchemy.sql.sqltypes import String
from fastapi import APIRouter, Response, HTTPException
from starlette.status import HTTP_200_OK \
                            ,HTTP_201_CREATED \
                            ,HTTP_404_NOT_FOUND \
                            ,HTTP_500_INTERNAL_SERVER_ERROR


from config.db import engine
from core.crud import insertArticle, insertDocument, updateProcessedDocument
from config.helper import read_config
from core.legifrance import getDocId, jsonToDocument, getDfArticles
from core.legifrance_api import codeToJson
from model.article import articles
from model.document import documents
from core.nlp import clusterDocument
from schema.article_schema import ArticleSchema
from schema.document_schema import DocumentSchema

config = read_config()

DOC_PATH = config['APPSettings']['doctemppath']
ART_PATH = config['APPSettings']['arttemppath']


router = APIRouter()

@router.post('/', response_model=str, status_code = HTTP_201_CREATED)
def save_document():
    """
    Save a document into the BD 
    """
    f = open(DOC_PATH)
    doc_json = json.load(f)
    data_document = jsonToDocument(doc_json)
    print(data_document)

    with engine.connect() as conn:
        new_document = data_document.dict()
        conn.execute(documents.insert().values(new_document))

    return data_document.doc_id


@router.get('/all/', response_model=List[DocumentSchema], status_code = HTTP_200_OK)
def get_all_documents():
    """
    Get all the documents
    """
    with engine.connect() as conn:
        result = conn.execute(documents.select()).fetchall()
    
    if not result:
        raise HTTPException(
            status_code = HTTP_404_NOT_FOUND,
            detail = f"No documents where found"
        )
    
    return(result)


@router.get('/{doc_id}', response_model=DocumentSchema, status_code = HTTP_200_OK)
def get_document(doc_id: str):
    """
    Get a document given it's id
    """
    with engine.connect() as conn:
        result = conn.execute(documents.select().where(documents.c.doc_id == doc_id)).first()
    
    if not result:
        raise HTTPException(
            status_code = HTTP_404_NOT_FOUND,
            detail = f"The document with id '{doc_id}' does not exist"
        )
    
    return(result)

@router.put('/{doc_id}', status_code = HTTP_200_OK)
def process_document(doc_id: str):
    """
    Process an existing document using NLP
    """
    clusterDocument(doc_id)
    updateProcessedDocument(doc_id)
 
    return(Response(status_code=HTTP_200_OK))


@router.delete('/{doc_id}', status_code = HTTP_200_OK)
def delete_document(doc_id: str):
    """
    Delete a document
    """
    with engine.connect() as conn:
        conn.execute(documents.delete().where(documents.c.doc_id == doc_id))
    
    return Response(status_code = HTTP_200_OK)

@router.get('/downloadCode/{doc_id}', status_code = HTTP_200_OK)
def download_code(doc_id: str):
    """
    Download a document, get it's articles, and save all into the DB
    """
    codeJson = codeToJson(doc_id)
    code = json.dumps(codeJson, indent=2)
    
    with open(DOC_PATH, 'w') as f:
         f.write(code)

    articles = getDfArticles(codeJson)
    if (articles.isnull().values.any()):
        articles = articles.dropna().reset_index(drop=True)
    articles.to_pickle(ART_PATH)
    
    return Response(status_code = HTTP_200_OK)


#@router.get('/checkId/{doc_id}', response_model=DocumentSchema)
#def check_id(doc_id: str):
#    return checkDocument(doc_id)
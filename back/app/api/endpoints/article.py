import pickle 
import pandas as pd

from typing import List
from fastapi import APIRouter, Response, HTTPException
from starlette.status import HTTP_200_OK \
                            ,HTTP_201_CREATED \
                            ,HTTP_404_NOT_FOUND
from config.db import engine
from model.article import articles
from core.crud import insertArticle
from config.helper import read_config
from core.legifrance import getDfArticles
from schema.article_schema import ArticleSchema
from schema.document_schema import DocumentSchema

config = read_config()

ART_PATH = config['APPSettings']['arttemppath']

router = APIRouter()


@router.post('/{doc_id}', status_code = HTTP_201_CREATED)
def save_articles(doc_id: str):
    """
    Save articles into the BD
    """
    articles = pickle.load(open(ART_PATH, 'rb'))

    for index, art in articles.iterrows():
        article = ArticleSchema(
            art_id = art['Id'],
            name = art['Name'],
            art_cid = art['Cid'],
            text = art['Text'],
            doc_id = doc_id
        )
        insertArticle(article)

    return Response(status_code=HTTP_201_CREATED)


@router.get('/{doc_id}', response_model=List[ArticleSchema], status_code = HTTP_200_OK)
def get_articles_from_document(doc_id: str):
    """
    Get all the articles from a specific document given it's id
    """
    with engine.connect() as conn:
        result = conn.execute(articles.select().where(articles.c.doc_id == doc_id)).all()
    
    if not result:
        raise HTTPException(
            status_code = HTTP_404_NOT_FOUND,
            detail = f"There are no articles for the document with id '{doc_id}'"
        )
    
    return(result)

"""
@router.get('/{art_id}', response_model=ArticleSchema, status_code = HTTP_200_OK)
def get_article(art_id: int):
"""
# Get an article given it's id
"""
    with engine.connect() as conn:
        result = conn.execute(articles.select().where(articles.c.art_id == art_id)).first()
    
    if not result:
        raise HTTPException(
            status_code = HTTP_404_NOT_FOUND,
            detail = f"The article with id '{art_id}' does not exist"
        )
        
    return(result)
"""
"""
@router.put('/{art_id}', response_model=ArticleSchema, status_code = HTTP_200_OK)
def update_article(article_updated: ArticleSchema, art_id: int):
"""
# Update an existing article
"""
    with engine.connect() as conn:
        conn.execute(articles.update().values(name = article_updated.name,
                                              doc_id = article_updated.doc_id,
                                              text = article_updated.text,
                                              cleaned_text = article_updated.cleaned_text,
                                              cluster = article_updated.cluster
                                              ).where(articles.c.art_id == art_id)
                     )
        result = conn.execute(articles.select().where(articles.c.art_id == art_id)).first()
    
    if not result:
        raise HTTPException(
            status_code = HTTP_404_NOT_FOUND,
            detail = f"The article with id '{art_id}' does not exist or couldn't be updated"
        )

    return(result)
"""

@router.delete('/delete/{doc_id}', status_code = HTTP_200_OK)
def delete_articles_by_doc(doc_id: str):
    """
    Delete all the articles for a document
    """
    with engine.connect() as conn:
        conn.execute(articles.delete().where(articles.c.doc_id == doc_id))
    
    return Response(status_code = HTTP_200_OK)

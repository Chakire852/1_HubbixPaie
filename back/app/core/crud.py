from config.db import engine
from model.article import articles
from model.document import documents
from schema.article_schema import ArticleSchema
from schema.document_schema import DocumentSchema

#def checkDocument(doc_id) -> DocumentSchema:
#    with engine.connect() as conn:
#        result = conn.execute(documents.select().where(documents.c.doc_id == doc_id)).first()
#    return result

def insertDocument(data_document: DocumentSchema):
    with engine.connect() as conn:
        new_document = data_document.dict()
        conn.execute(documents.insert().values(new_document))
   
def deleteDocument(doc_id: str):
    with engine.connect() as conn:
        conn.execute(documents.delete().where(documents.c.doc_id == doc_id))
    
def insertArticle(data_article: ArticleSchema):
    with engine.connect() as conn:
        new_article = data_article.dict()
        conn.execute(articles.insert().values(new_article))

def updateClusterArticle(art_id: str, cluster: int):
    with engine.connect() as conn:
        conn.execute(articles.update().values(cluster = cluster
                                               ).where(
                                                   articles.c.art_id == art_id
                                               )
                     )

def updateProcessedDocument(doc_id: str):
    with engine.connect() as conn:
        conn.execute(documents.update().values(
                                               processed = True
                                               ).where(
                                                  documents.c.doc_id == doc_id
                                               )
                     )
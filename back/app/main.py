from pathlib import Path
#from datetime import datetime
from core.nlp import clusterDocument
#from api.endpoints.article import get_articles_from_document
from fastapi import FastAPI, APIRouter
from starlette.status import HTTP_200_OK
#from multiprocessing.dummy import Process
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from api.api import api_router
# from core.legifrance import getDocId, jsonToDocument
# from core.legifrance_api import codeToJson, 
from core.legifrance_api import getAllCodes
#from core.nlp import clusterDocument
#from core.crud import insertDocument, insertArticle
#from schema.article_schema import ArticleSchema
#from schema.document_schema import DocumentSchema


BASE_PATH = Path(__file__).resolve().parent
DATA_DIR = str(BASE_PATH / "core/data")

root_router = APIRouter()
app = FastAPI(
    title="Projet 3WA - Partie 1",
)

origins = [
    "http://localhost",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/data", StaticFiles(directory=DATA_DIR), name="data")

@root_router.get("/", status_code = HTTP_200_OK)
def root() -> dict:
    """
    Get Codes from Legifrance
    """
    return getAllCodes()

app.include_router(root_router)
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")
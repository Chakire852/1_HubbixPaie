from fastapi import APIRouter

from api.endpoints import article, document

api_router = APIRouter()
api_router.include_router(article.router, prefix="/api/articles")
api_router.include_router(document.router, prefix="/api/documents")
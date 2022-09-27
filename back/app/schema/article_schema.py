from pydantic import BaseModel
from typing import Optional

class ArticleSchema(BaseModel):
    art_id: str
    name: str
    art_cid: str
    text: str
    doc_id: str
    cluster: Optional[int]
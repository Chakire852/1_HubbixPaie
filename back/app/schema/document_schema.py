import datetime
from sqlalchemy.sql.sqltypes import Boolean
from pydantic import BaseModel
    
class DocumentSchema(BaseModel):
    doc_id: str
    name: str
    #path: str
    date: datetime.datetime
    processed: bool
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Text
from sqlalchemy.dialects.mysql import INTEGER

from config.db import engine, meta_data
from model.document import documents

articles = Table('articles', meta_data,
                 Column('art_id', String(25), primary_key=True),
                 Column('name', String(255), nullable=False),
                 Column('art_cid', String(25), nullable=False),
                 Column('text', Text, nullable=False),
                 Column('doc_id', String(25), ForeignKey(documents.c.doc_id),
                        nullable=False),
                 Column('cluster', INTEGER(unsigned=True)),
                 mysql_engine="InnoDB",
                 )

meta_data.create_all(engine)
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, DateTime, Boolean

from config.db import engine, meta_data

documents = Table(
       'documents', meta_data,
              Column('doc_id', String(25), primary_key=True),
              Column('name', String(255), nullable=False),
              #Column('path', String(255), nullable=False),
              Column('date', DateTime(timezone=False), nullable=False),
              Column('processed', Boolean, nullable=False, default=False),
       mysql_engine="InnoDB",
       )

meta_data.create_all(engine)
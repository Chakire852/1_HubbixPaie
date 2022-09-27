from sqlalchemy import create_engine, MetaData

from config.helper import read_config

config = read_config()

dbEngine = config['BDSettings']['dbengine']
username = config['BDSettings']['username']
password = config['BDSettings']['password']
hostname = config['BDSettings']['hostname']
port     = config['BDSettings']['port']
database = config['BDSettings']['database']

SQLALCHEMY_DATABASE_URI = f"{dbEngine}://{username}:{password}@{hostname}:{port}/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URI)

meta_data = MetaData()
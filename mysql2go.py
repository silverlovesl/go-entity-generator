import string
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import util
import db


class MySql2Go(db.DB):
    SQL_SCHEMA = """
    select
        LOWER(COLUMN_NAME) as name,
        LOWER(DATA_TYPE)   as type,
        LOWER(IS_NULLABLE) as is_nullable
    from
        information_schema.columns
    where table_name = '{}'
    order by
        ordinal_position;
    """

    def __init__(self, dbname, tablename, username, password, host, port, is_json=False):
        db.DB.__init__(self,
                       dbname, tablename,
                       username, password,
                       host, port,
                       is_json)
        self.constr = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
            username, password, host, port, dbname)

    def convert2GoStruct(self):
        engine = create_engine(self.constr)
        return db.DB.convert2GoStruct(self, engine,  self.SQL_SCHEMA)

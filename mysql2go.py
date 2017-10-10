import string
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import util
import db
import os
import codecs


class MySql2Go(db.DB):
    COL_SCHEMA = """
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

    TABLE_SCHEMA = """
    select
        TABLE_NAME as name
    from
        information_schema.tables
    where
        TABLE_SCHEMA = '{}';
    """

    def __init__(self, params):
        db.DB.__init__(self, params)
        self.constr = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
            self.username,
            self.password,
            self.host,
            self.port,
            self.dbname)

    def convert2GoStruct(self):
        engine = create_engine(self.constr)
        return db.DB.convert2GoStruct(self, engine,  self.COL_SCHEMA.format(self.tablename))

    def convertAllTables(self):
        engine = create_engine(self.constr)
        table_names = db.DB.getAllTableNames(
            self, engine, self.TABLE_SCHEMA.format(self.dbname))
        for name in table_names:
            db.DB.tablename = name
            self.tablename = name
            go_struct_str = db.DB.convert2GoStruct(
                self, engine,  self.COL_SCHEMA.format(name))
            file_path = os.path.join(self.output, name + ".go")
            with codecs.open(file_path, mode="w", encoding='utf8') as f:
                f.write(go_struct_str)
                f.close()

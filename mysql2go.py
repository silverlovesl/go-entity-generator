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

    def __init__(self, dbname, tablename, username, password, host, port):
        db.DB.__init__(self, dbname, tablename, username, password, host, port)
        self.constr = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
            username, password, host, port, dbname)

    def convert2GoStruct(self):
        engine = create_engine(self.constr)
        connection = engine.connect()
        df = pd.read_sql(self.SQL_SCHEMA.format(self.tablename), engine)

        go_struct = [""]
        go_struct.append("type " + self.tablename.capitalize() + " struct{")
        for index, row in df.iterrows():
            is_nullable = row["is_nullable"] == "yes"
            goFiled = util.trueCase(row["name"])
            goType = util.mappingGoType(row["type"], is_nullable)
            go_struct.append(goFiled + " " + goType)
        go_struct.append("}")
        return "\n".join(go_struct)

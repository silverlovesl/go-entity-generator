import psycopg2
import util
import db
import pandas as pd
from sqlalchemy import create_engine


class Postgre2Go(db.DB):

    SQL_SCHEMA = """
      SELECT
          f.attname                                   AS name
          ,pg_catalog.format_type (f.atttypid, null)  AS type
          ,f.attnotnull                               AS is_nullable
      FROM
          pg_attribute f
      INNER JOIN pg_class c ON c.oid = f.attrelid
      INNER JOIN pg_type t ON t.oid = f.atttypid
      LEFT JOIN  pg_attrdef d ON d.adrelid = c.oid AND d.adnum = f.attnum
      LEFT JOIN  pg_namespace n ON n.oid = c.relnamespace
      LEFT JOIN  pg_constraint p ON p.conrelid = c.oid AND f.attnum = ANY (p.conkey)
      LEFT JOIN  pg_class AS g ON p.confrelid = g.oid
      WHERE
          c.relkind = 'r'::char
      AND c.relname = '{}'
      AND f.attnum > 0
      ORDER BY
          f.attnum
    """

    def __init__(self, dbname, tablename, username, password, host, port):
        db.DB.__init__(self, dbname, tablename, username, password, host, port)
        self.constr = 'postgresql://{}:{}@{}:{}/{}'.format(
            username, password, host, port, dbname)

    def convert2GoStruct(self):
        print(self.constr)
        engine = create_engine(self.constr)
        df = pd.read_sql(self.SQL_SCHEMA.format(self.tablename), engine)
        go_struct = [""]
        tableName = util.trueCase(self.tablename)
        go_struct.append("type " + tableName + " struct{")
        for index, row in df.iterrows():
            is_nullable = row["is_nullable"] == "yes"
            goFiled = util.trueCase(row["name"])
            goType = util.mappingGoType(row["type"], is_nullable)
            go_struct.append(goFiled + " " + goType)
        go_struct.append("}")
        return "\n".join(go_struct)

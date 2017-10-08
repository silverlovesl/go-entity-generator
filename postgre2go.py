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

    def __init__(self, dbname, tablename, username, password, host, port, is_json=False):
        db.DB.__init__(self,
                       dbname, tablename,
                       username, password,
                       host, port,
                       is_json)
        self.constr = 'postgresql://{}:{}@{}:{}/{}'.format(
            username, password, host, port, dbname)

    def convert2GoStruct(self):
        engine = create_engine(self.constr)
        return db.DB.convert2GoStruct(self, engine,  self.SQL_SCHEMA)

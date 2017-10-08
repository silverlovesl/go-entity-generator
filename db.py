import pandas as pd
from sqlalchemy import create_engine
import util


class DB:
    def __init__(self, dbname, tablename, username, password, host, port, is_json=False):
        self.dbname = dbname
        self.tablename = tablename
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.is_json = is_json

    def convert2GoStruct(self, engine, schema_query):
        connection = engine.connect()
        df = pd.read_sql(schema_query.format(self.tablename), engine)
        go_struct = [""]
        go_struct.append(
            "type " + util.trueCase(self.tablename) + " struct{")
        for _, row in df.iterrows():
            is_nullable = row["is_nullable"] == "yes"
            col_name = row["name"]
            col_type = row["type"]
            go_filed = util.trueCase(col_name)
            _json_ = is_nullable or self.is_json
            go_type = util.mappingGoType(col_type, _json_)
            json_def = ""
            if self.is_json:
                json_def = "`json:\"" + \
                    util.fistWordLowerCase(go_filed) + "\"`"

            go_struct.append(util.specialWord(go_filed) +
                             " " + go_type + " " + json_def)
        go_struct.append("}")
        return "\n".join(go_struct)

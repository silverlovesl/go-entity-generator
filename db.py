import pandas as pd
from sqlalchemy import create_engine
import util


class DB:
    def __init__(self, params):
        self.dbname = params.dbname
        self.tablename = params.tablename
        self.username = params.username
        self.password = params.password
        self.host = params.host
        self.port = params.port
        self.is_json = params.is_json
        self.pgname = params.pgname
        self.output = params.output

    def convert2GoStruct(self, engine, query):
        connection = engine.connect()
        df = pd.read_sql(query, engine)
        go_struct = []
        table_name = util.trueCase(self.tablename)
        go_struct.append("package {}".format(self.pgname))
        go_struct.append("\n")
        go_struct.append("// {} [Comment]".format(table_name))
        go_struct.append("type {} struct{{".format(table_name))
        for _, row in df.iterrows():
            is_nullable = row["is_nullable"] == "yes"
            col_name = row["name"]
            col_type = row["type"]
            go_filed = util.trueCase(col_name)
            _json_ = False
            if not self.is_json:
                _json_ = is_nullable
            go_type = util.mappingGoType(col_type, _json_)
            json_def = ""
            xorm_def = ""
            if self.is_json:
                json_def = "`json:\"" + \
                    util.fistWordLowerCase(go_filed) + "\"`"
            else:
                xorm_def = "`xorm:\"'{}'\"`".format(col_name)

            go_struct.append("{} {} {} {}".format(util.specialWord(
                go_filed), go_type, xorm_def, json_def))
        go_struct.append("}")
        return "\n".join(go_struct)

    def getAllTableNames(self, engine, query):
        connection = engine.connect()
        df = pd.read_sql(query, engine)
        table_names = []
        for _, row in df.iterrows():
            table_names.append(row["name"])
        return table_names

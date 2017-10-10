class Option:
    dbname = ""
    tablename = ""
    username = ""
    password = ""
    host = ""
    port = ""
    is_json = False
    is_export_all = False
    output = ""
    pgname = ""

    def __init__(self, dbname, tablename, username, password, host, port, is_json=False, is_export_all=False, output="", pgname=""):
        self.dbname = dbname
        self.tablename = tablename
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.is_json = is_json
        self.is_export_all = is_export_all
        self.output = output
        self.pgname = pgname

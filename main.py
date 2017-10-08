import argparse
import mysql2go
import postgre2go

ap = argparse.ArgumentParser()
# group = ap.add_mutually_exclusive_group(required=True)
ap.add_argument('-T', '--type', help="M:Mysql P:Postgres", default="M")
ap.add_argument('-d', '--database', required=True)
ap.add_argument('-t', '--tablename', required=True)
ap.add_argument('-u', '--username', default="root")
ap.add_argument('-p', '--password', default="")
ap.add_argument('-H', '--host', default="localhost")
ap.add_argument('-P', '--port', default="3306")

opts = ap.parse_args()

print(opts)

if opts.type == "M":
    convertor = mysql2go.MySql2Go(opts.database, opts.tablename, opts.username,
                                  opts.password, opts.host, opts.port)
    print(convertor.convert2GoStruct())

if opts.type == "P":
    convertor = postgre2go.Postgre2Go(opts.database, opts.tablename, opts.username,
                                      opts.password, opts.host, opts.port)
    print(convertor.convert2GoStruct())

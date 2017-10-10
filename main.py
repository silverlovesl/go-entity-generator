import argparse
import mysql2go
import postgre2go
import option
import os
from subprocess import call

ap = argparse.ArgumentParser()
# group = ap.add_mutually_exclusive_group(required=True)

ap.add_argument(
    '-T', '--type', help="Database type M:mysql P:PostgreSQL (Default:M)", default="M")
ap.add_argument('-a', '--all', help="Export all tables", required=False)
ap.add_argument('-o', '--output', help="Output Directory", required=False)
ap.add_argument('--pgname', help="go package name",
                default="entity", required=False)
ap.add_argument('-d', '--database', help="Database name", required=True)
ap.add_argument('-t', '--tablename', help="Target table name", required=False)
ap.add_argument('-u', '--username',
                help="Login user (Default:'root')", default="root")
ap.add_argument('-p', '--password',
                help="Login password (Default:'')", default="")
ap.add_argument('-H', '--host', help="Host (Default:localhost)",
                default="localhost")
ap.add_argument('-P', '--port', help="Port (Default:3306)", default="3306")
ap.add_argument(
    '-j', '--json', help="with json declaration (Default:0)", default="0")

opts = ap.parse_args()

print(opts)

if not opts.all and not opts.tablename:
    print("You should choose [export all: -a] or [sepcify tablename -t]")
    os._exit(0)

if opts.all and not opts.output:
    print("When out all tables, you have to sepcify output directory")
    os._exit(0)

if opts.output:
    if not os.path.exists(opts.output):
        print("The output path is not exists")
        os._exit(0)

params = option.Option(opts.database, opts.tablename, opts.username,
                       opts.password, opts.host, opts.port, opts.json == "1", opts.all == "1", opts.output, opts.pgname)


if opts.type == "M":
    convertor = mysql2go.MySql2Go(params)
    if opts.all == "1":
        convertor.convertAllTables()
        call(["goreturns", "-w", opts.output])
    else:
        print(convertor.convert2GoStruct())

if opts.type == "P":
    convertor = postgre2go.Postgre2Go(opts.database, opts.tablename, opts.username,
                                      opts.password, opts.host, opts.port, opts.json == "1")
    print(convertor.convert2GoStruct())

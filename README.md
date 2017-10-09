# Depends library
1) install pyenv https://github.com/pyenv/pyenv
```bash
pip install pymysql
pip install sqlalchemy
pip install psycopg2
```

# Usage
```bash
# Option
-T | --type      Database type "M":mysql "P":PostgreSQL (Default:M)
-d | --database  Database name
-t | --tablename Target table name
-u | --username  Login user (Default:"root")
-p | --password  Login password (Default:'')
-H | --host      Host (Default:localhost)
-P | --port      Port (Default:3306)
-j | --json      with json declaration (Default:0)


# mysql
python main.py -d espire_development -t students -u root

# postgres
python main.py -T P -d keerp -t t_p_expense -u andysilver -p 65570480 -H localhost -P 5432 -j 1
```

# Generation rule
> "first_name" -> "firstName" <br/>
> "id" -> "ID"
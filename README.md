# Depends library
1) install pyenv https://github.com/pyenv/pyenv
```bash
pip install pymysql
pip install sqlalchemy
pip install psycopg2
```

# Usage
```bash
# mysql
python main.py -d espire_development -t students -u root

# postgres
python main.py -T P -d keerp -t t_p_expense -u andysilver -p 65570480 -H localhost -P 5432 -j 1
```
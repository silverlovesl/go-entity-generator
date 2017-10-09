import string
import re

MYSQL_SCHEMA = """
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


def trueCase(colName):
    return ''.join(x.capitalize() or '_' for x in colName.split('_'))


def specialWord(word):
    word = re.sub(r"(i|I)d$", "ID", word, re.RegexFlag.IGNORECASE)
    word = re.sub(r"(i|I)p$", "IP", word, re.RegexFlag.IGNORECASE)
    return word


def fistWordLowerCase(word):
    if len(word) >= 2:
        return word[0].lower() + word[1:]
    else:
        return word


def mappingGoType(colType, isNullable):
    rv = ""
    if colType in ("char", "varchar", "text", "character", "character varying"):
        rv = "null.String" if isNullable else "string"
    elif colType in ("int", "integer", "smallint"):
        rv = "zero.Int" if isNullable else "int"
    elif colType == "bigint":
        rv = "zero.Int" if isNullable else "int64"
    elif colType in ("float", "decimal", "numeric"):
        rv = "zero.Float" if isNullable else "float64"
    elif colType in ("datetime", "date", "timestamp without time zone"):
        rv = "time.Time"
    elif colType in("tinyint", "bool"):
        rv = "bool"
    return rv

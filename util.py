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


def mappingGoType(colType, isNullable):
    rv = ""
    if colType in ("char", "varchar", "text", "character", "character varying"):
        rv = "string" if isNullable else "null.String"
    elif colType in ("int", "integer", "smallint"):
        rv = "int" if isNullable else "zero.Int"
    elif colType == "bigint":
        rv = "int64" if isNullable else "zero.Int"
    elif colType in ("float", "decimal", "numeric"):
        rv = "float" if isNullable else "zero.Float"
    elif colType in ("datetime", "date", "timestamp without time zone"):
        rv = "time.Time"
    elif colType in("tinyint", "bool"):
        rv = "bool"
    return rv

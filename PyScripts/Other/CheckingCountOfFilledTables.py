from PyScripts.base.base_functions import db_conn


def check_tables(table_schema):
    cur.execute("SELECT table_schema, table_name FROM " + '"information_schema"' +
                f".tables WHERE table_schema = '{table_schema}'")

    tables = [schema_and_table[:2] for schema_and_table in cur.fetchall()]

    filled_tables = []

    for schema_and_table in tables:
        if schema_and_table[0] != 'information_schema' and schema_and_table[0] != 'pg_catalog':
            cur.execute(f'SELECT * FROM "{schema_and_table[0]}".{schema_and_table[1]}')
            table = cur.fetchall()
            if len(table) > 0:
                filled_tables.append((schema_and_table[0], schema_and_table[1], len(table)))

    print(f'Схема {table_schema}: {len(filled_tables)}/{len(tables)}')

    return len(filled_tables), len(tables)


cur, conn = db_conn()
cur.execute("SELECT schema_name FROM " + '"information_schema"' + ".schemata")
schemas = [schema[0] for schema in cur.fetchall()]
all_filled_cnt, all_cnt = 0, 0
for schema in schemas:
    if schema != 'information_schema' and schema != 'pg_catalog':
        filled, all = check_tables(schema)
        all_filled_cnt += filled
        all_cnt += all

print(f"{all_filled_cnt}/{all_cnt}")

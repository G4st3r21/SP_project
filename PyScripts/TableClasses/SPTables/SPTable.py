import sys

import psycopg2


class SPTable:
    def __init__(self, table_name, cur, conn, schema='public'):
        self.schema = f'"{schema}"' if schema != 'public' else schema
        self.table_name = table_name
        self.cur, self.conn = cur, conn

        self.columns = self._check_columns()
        self.hasSerialID = self._has_serial_id()
        self.isEmpty = self._is_empty_table()

    def fetchall(self):
        try:
            return self.cur.fetchall()
        except psycopg2.ProgrammingError:
            return False

    def commit(self):
        self.conn.commit()

    def _check_columns(self):
        schema = self.schema.replace('"', "'") if self.schema != 'public' else "'public'"
        self.cur.execute(
            "SELECT * FROM " + '"information_schema"' +
            f".columns WHERE table_name = '{self.table_name}' and table_schema = {schema}")

        return [(column[3], column[7]) for column in self.cur.fetchall()]

    def _has_serial_id(self):
        self.cur.execute(
            "SELECT * FROM " + '"information_schema"' +
            ".columns WHERE table_name = '{self.table_name}' AND ordinal_position = 1")

        id_type = self.fetchall()
        if id_type:
            return id_type[0][5]
        else:
            return False

    def _is_empty_table(self):
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name}")
        obj = self.fetchall()

        return False if obj else True

    def get_id_by_title(self, title):
        title_name = self.columns[1][0]
        title = f"'{title}'" if not self.columns[0][1] != 'integer' else f'{title}'
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} WHERE {title_name} = {title}")
        obj = self.fetchall()

        return obj[0][0] if obj else False

    def get_title_by_id(self, obj_id):
        id_name = self.columns[0][0]
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE {id_name} = {obj_id}")
        obj = self.fetchall()

        return obj[0][1] if obj else False

    def add(self, *args):
        if len(args) > 1:
            sys.exit(f'Слишком много аргументов для метода "add" таблицы {self.table_name}\n'
                     f'(Ожидалось 1, получено {len(args)})')

        obj_id = self.get_id_by_title(args[0])
        if obj_id:
            return obj_id

        title_name = self.columns[1][0]
        id_name = self.columns[0][0]
        title = f"'{args[0]}'" if 'integer' not in self.columns[1][1] else f'{args[0]}'
        if self.hasSerialID:
            if self.isEmpty:
                self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES (1, {title})")
            else:
                self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name}({title_name}) VALUES ({title})")
            self.isEmpty = False

            return self.get_id_by_title(title)
        else:
            self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} ORDER BY {id_name}")
            obj_id = self.cur.fetchall()
            if not obj_id:
                obj_id = 1
            else:
                obj_id = obj_id[-1][0] + 1
            self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ({obj_id}, {title})")

            return obj_id

import sys

from PyScripts.TableClasses.SPTables.SPTable import SPTable


class SPTableArbitrary(SPTable):
    def __init__(self, table_name, cur, conn, schema='public'):
        super().__init__(table_name, cur, conn, schema)

    def get_by_column(self, column_name, title):
        title = f"'{title}'" if not self.columns[0][1] != 'integer' else f'{title}'
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id = {id}")
        obj = self.cur.fetchall()

        return obj[0] if obj else False

    def get_by_tuple(self, *args):
        get_args = [f"{self.columns[args.index(arg)][0]} = '{arg}'" if type(
            arg) is str else f"{self.columns[args.index(arg)][0]} = {arg}" for arg in args]
        if len(args) == len(self.columns):
            self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} WHERE {' AND '.join(get_args[1:])}")
        elif len(args) + 1 == len(self.columns):
            self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} WHERE {' AND '.join(get_args)}")
        obj = self.cur.fetchall()

        return obj[0][0] if obj else False

    def add(self, *args):
        obj_id = self.get_by_tuple(args)
        if obj_id:
            return obj_id

        request_args = ", ".join([f"'{arg}'" if type(arg) is str else str(arg) for arg in args])
        if len(args) == len(self.columns):
            self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ({request_args})")
        elif len(args) + 1 == len(self.columns):
            if 'integer' in self.columns[0][1]:
                request_columns = ', '.join([column[0] for column in self.columns[1:]])
                self.cur.execute(
                    f"INSERT INTO {self.schema}.{self.table_name}({request_columns}) VALUES ({request_args})")
                if self.hasSerialID:
                    if self.isEmpty:
                        self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES (1, {request_args})")
                    else:
                        self.cur.execute(
                            f"INSERT INTO {self.schema}.{self.table_name}({request_columns}) VALUES ({request_args})")
                    self.isEmpty = False

                    return self.get_by_tuple(args)
                else:
                    self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} ORDER BY {self.columns[0][0]}")
                    obj_id = self.cur.fetchall()
                    if not obj_id:
                        obj_id = 1
                    else:
                        obj_id = obj_id[-1][0] + 1
                    self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ({obj_id}, {request_args})")

                    return obj_id
        elif len(args) > len(self.columns):
            sys.exit(f'Слишком много аргументов для метода "add" таблицы {self.table_name}\n'
                     f'(Ожидалось {len(self.columns)} или {len(self.columns) - 1}, получено {len(args)})')
        else:
            sys.exit(f'Слишком мало аргументов для метода "add" таблицы {self.table_name}\n'
                     f'(Ожидалось {len(self.columns)} или {len(self.columns) - 1}, получено {len(args)})')

import sys
from datetime import date

from psycopg2 import ProgrammingError
from psycopg2 import cursor, connection

from PyScripts.TableClasses.SPTables.SPTable import SPTable


class SPTableArbitrary(SPTable):
    def __init__(self, table_name: str, cur: cursor, conn: connection, schema: str = 'public'):
        super().__init__(table_name, cur, conn, schema)

    def get_by_column(self, column_name, title):
        title = f"'{title}'" if not self.columns[0][1] != 'integer' else f'{title}'
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE {column_name} = {title}")
        obj = self.fetchall()

        return obj[0] if obj else False

    def get_by_tuple(self, *args, condition_type='AND'):
        args = list(args)
        if len(args) == len(self.columns):
            get_args = [f"{self.columns[args.index(arg)][0]} = '{arg}'" if type(
                arg) is str else f"{self.columns[args.index(arg)][0]} = {arg}" for arg in args]
            self.cur.execute(
                f"SELECT * FROM {self.schema}.{self.table_name} WHERE {f' {condition_type} '.join(get_args[1:])}")
        elif len(args) + 1 == len(self.columns):
            get_args = [f"{self.columns[args.index(arg) + 1][0]} = '{arg}'" if type(
                arg) is str else f"{self.columns[args.index(arg) + 1][0]} = {arg}" for arg in args]
            self.cur.execute(
                f"SELECT * FROM {self.schema}.{self.table_name} WHERE {f' {condition_type} '.join(get_args)}")

        obj = self.fetchall()

        return obj[0][0] if obj else False

    def _format_arguments(self, request_args: list[str, int]):
        for arg, arg_type in zip(request_args, self.columns):
            match arg_type[-1]:
                case "text", "character varying":
                    if type(arg) is not str:
                        raise TypeError(
                            f"Неверно указан аргумент {arg_type[0]}, ожидался тип {arg_type[-1]}, получен {type(arg)}"
                        )
                    else:
                        arg = f"'{arg}'"
                case "integer", "bigint", "smallint":
                    if type(arg) is str and not arg.isdigit():
                        raise TypeError(
                            f"Неверно указан аргумент {arg_type[0]}, ожидался тип {arg_type[-1]}, получен {type(arg)}"
                        )
                    elif type(arg) is str and arg.isdigit():
                        arg = f"{int(arg)}"
                case "double precision", "boolean":
                    if type(arg) is str and arg not in ["True", "False"]:
                        raise TypeError(
                            f"Неверно указан аргумент {arg_type[0]}, ожидался тип {arg_type[-1]}, получен {type(arg)}"
                        )
                    elif type(arg) is bool:
                        arg = "True" if arg else "False"
                case "real":
                    try:
                        if type(arg) is str:
                            arg = f"{float(arg)}"
                    except Exception:
                        raise TypeError(
                            f"Неверно указан аргумент {arg_type[0]}, ожидался тип {arg_type[-1]}, получен {type(arg)}"
                        )
                case "date":
                    try:
                        temp_date = arg.split(".")
                        arg = date(year=int(temp_date[2]), month=int(temp_date[1]), day=int(temp_date[0]))
                        arg = f"'{arg.__str__()}'"
                    except Exception:
                        raise TypeError(
                            f"Неверно указан аргумент {arg_type[0]}, ожидался тип {arg_type[-1]}, получен {type(arg)}"
                        )

        return request_args

    def add(self, *args, condition_type='AND'):
        args = list(args)
        obj_id = self.get_by_tuple(*args, condition_type)
        if obj_id:
            return obj_id

        request_args = self._format_arguments(args)
        request_args = ", ".join(request_args)
        if len(args) == len(self.columns):
            self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ({request_args})")
        elif len(args) + 1 == len(self.columns):
            if 'integer' in self.columns[0][1]:
                request_columns = ', '.join([column[0] for column in self.columns[1:]])
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

                    self.isEmpty = False
                    return obj_id
        elif len(args) > len(self.columns):
            sys.exit(f'Слишком много аргументов для метода "add" таблицы {self.table_name}\n'
                     f'(Ожидалось {len(self.columns)} или {len(self.columns) - 1}, получено {len(args)})')
        else:
            sys.exit(f'Слишком мало аргументов для метода "add" таблицы {self.table_name}\n'
                     f'(Ожидалось {len(self.columns)} или {len(self.columns) - 1}, получено {len(args)})')

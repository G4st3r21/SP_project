import sys

from PyScripts.TableClasses.PublicClasses.SPTable import SPTable


class SPTableArbitrary(SPTable):
    def __init__(self, table_name, table_title, cur, conn, schema='public'):
        super().__init__(table_name, table_title, cur, conn, schema)
        self.columns = self.check_columns()

    def check_columns(self):
        self.cur.execute(
            f"SELECT * FROM information_schema.columns WHERE table_name = '{self.table_name}' and table_schema = '{self.schema}'")
        columns = [(column[3], column[7]) for column in self.cur.fetchall()]

        return columns

    def get_name_by_id(self, obj_id):
        sys.exit("Error: method 'find_name_by_id' can't be called by 'SPTableArbitrary' class\n")

    def get_id_by_name(self, title):
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} WHERE {self.title} like '{title}'")
        obj = self.cur.fetchall()

        return obj[0][0] if obj else False

    def get_by_id(self, obj_id):
        id = f"'{obj_id}'" if not self.columns[0][1] != 'integer' else f'{obj_id}'
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id = {id}")
        obj = self.cur.fetchall()

        return obj[0] if obj else False

    def add(self, *args):
        title = [arg for arg in args if type(arg) is str][0]
        obj_id = self.get_id_by_name(title)
        if obj_id:
            return obj_id

        request_args = ", ".join([f"'{arg}'" if type(arg) is str else str(arg) for arg in args])
        request_columns = ', '.join([column[0] for column in self.columns])
        self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name}({request_columns}) VALUES ({request_args})")

        return args[0]

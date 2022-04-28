import sys

from PyScripts.TableClasses.PublicClasses.SPTable import SPTable


class SPTableManyToMany(SPTable):
    def __init__(self, table_name, cur, conn, table_title=None, schema='public'):
        super().__init__(table_name, table_title, cur, conn, schema)
        self.columns = self.check_columns()
        if self.title is not None:
            print(f"[Warning]: This class doesn't need a table_title parameter")
        if len(self.columns) > 2:
            sys.exit("[Error]: SPTableManyToMany works only with tables type 'Many to Many'\n")

    def check_columns(self):
        schema = self.schema.replace('"', "'")
        self.cur.execute(
            "SELECT * FROM " + '"information_schema"' +
            f".columns WHERE table_name = '{self.table_name}' and table_schema = {schema}")
        columns = [(column[3], column[7]) for column in self.cur.fetchall()]

        return columns

    def get_first_columns_by_second(self, second_title):
        second_title = f"'{second_title}'" if 'integer' not in self.columns[1][1] else second_title
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} WHERE {self.columns[1][0]} = {second_title}")
        obj = self.cur.fetchall()

        return obj if obj else False

    def get_second_columns_by_first(self, first_title):
        first_title = f"'{first_title}'" if 'integer' not in self.columns[0][1] else first_title
        self.cur.execute(
            f"SELECT * FROM {self.schema}.{self.table_name} WHERE {self.columns[0][0]} = {first_title}")
        obj = self.cur.fetchall()

        return obj if obj else False

    def find_tuple(self, first_title, second_title):
        first_title = f"'{first_title}'" if 'integer' not in self.columns[0][1] else first_title
        second_title = f"'{second_title}'" if 'integer' not in self.columns[1][1] else second_title
        self.cur.execute(
            f"SELECT * FROM {self.schema}.{self.table_name} WHERE {self.columns[0][0]} = {first_title}"
            f" and {self.columns[1][0]} = {second_title} ")
        obj = self.cur.fetchall()

        return True if obj else False

    def add(self, first_title, second_title):
        if self.find_tuple(first_title, second_title):
            print(f"[Warning]: This tuple is already in the table '{self.table_name}'")
        else:
            first_title = f"'{first_title}'" if 'integer' not in self.columns[0][1] else first_title
            second_title = f"'{second_title}'" if 'integer' not in self.columns[0][1] else second_title
            self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ({first_title}, {second_title})")

    def get_id_by_name(self, title):
        sys.exit("[Error]: Not possible for this class\n")

    def get_name_by_id(self, obj_id):
        sys.exit("[Error]: Not possible for this class\n")

    def delete(self, title=None, obj_id=None):
        sys.exit("[Error]: Not possible for this class\n")

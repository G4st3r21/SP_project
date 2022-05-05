import sys

from PyScripts.TableClasses.SPTables.SPTable import SPTable


class SPTableManyToMany(SPTable):
    def __init__(self, table_name, cur, conn, schema='public'):
        super().__init__(table_name, cur, conn, schema)
        if len(self.columns) > 2:
            sys.exit("[Error]: SPTableManyToMany works only with tables type 'Many to Many'\n")

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

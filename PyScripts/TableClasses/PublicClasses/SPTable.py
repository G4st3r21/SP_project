class SPTable:
    def __init__(self, table_name, table_title, cur, conn, schema='public'):
        self.schema = schema
        self.table_name = table_name
        self.title = table_title
        self.cur, self.conn = cur, conn
        self.hasSerialID = self.has_serial_id()
        self.isEmpty = self.is_empty_table()

    def commit(self):
        self.conn.commit()

    def has_serial_id(self):
        self.cur.execute(
            "SELECT * FROM " + '"information_schema"' +
            ".columns WHERE table_name = '{self.table_name}' AND ordinal_position = 1")

        id_type = self.cur.fetchall()
        if id_type:
            return id_type[0][5]
        else:
            return False

    def is_empty_table(self):
        self.cur.execute("SELECT * FROM " + f'"{self.schema}"' + f".{self.table_name}")
        obj = self.cur.fetchall()

        return False if obj else True

    def get_id_by_name(self, title):
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} WHERE {self.title} like '{title}'")
        obj = self.cur.fetchall()

        return obj[0][0] if obj else False

    def get_name_by_id(self, obj_id):
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id = {obj_id}")
        obj = self.cur.fetchall()

        return obj[0][1] if obj else False

    def add(self, title, is_int=False):
        obj_id = self.get_id_by_name(title)
        if obj_id:
            return obj_id

        if self.hasSerialID:
            title = f"'{title}'" if not is_int else f'{title}'
            if self.isEmpty:
                self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES (1, {title})")
            else:
                self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name}({self.title}) VALUES ({title})")
            self.isEmpty = False

            return self.get_id_by_name(title)
        else:
            self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} ORDER BY id")
            obj_id = self.cur.fetchall()
            if not obj_id:
                obj_id = 1
            else:
                obj_id = obj_id[-1][0] + 1
            self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ({obj_id}, '{title}')")

            return obj_id

    def delete(self, title=None, obj_id=None):
        if title and self.get_id_by_name(title):
            self.cur.execute(f"DELETE FROM {self.schema}.{self.table_name} WHERE {self.title} = '{title}'")
            self.is_empty_table()
            return True
        elif obj_id and self.get_name_by_id(obj_id):
            self.cur.execute(f"DELETE FROM {self.schema}.{self.table_name} WHERE id = {obj_id}")
            self.is_empty_table()
            return True

        return False

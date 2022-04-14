
class BasicTable:
    def __init__(self, table_name, table_title, cur, conn):
        self.table_name = table_name
        self.schema = 'public'
        self.title = table_title
        self.cur, self.conn = cur, conn
        self.isEmpty = None
        self.is_empty_table()

    def commit(self):
        self.conn.commit()

    def is_empty_table(self):
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name}")
        obj = self.cur.fetchall()
        self.isEmpty = False if obj else True

    # Возвращает id ответственного объекта по его title
    # False, если такого объекта нет
    def find_id_by_name(self, title: str) -> int:
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} WHERE {self.title} like '{title}'")
        obj = self.cur.fetchall()

        return obj[0][0] if obj else False

    # Возвращает title ответственного объекта по его id
    # False, если такого объекта нет
    def find_name_by_id(self, obj_id: int) -> int:
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id = {obj_id}")
        obj = self.cur.fetchall()

        return obj[0][1] if obj else False

    # Добавление нового объекта только по title (c проверкой на наличие в таблице)
    # Возвращает id
    def add(self, title: str, is_int=False) -> int:
        obj_id = self.find_id_by_name(title)
        if obj_id:
            return obj_id
        title = f"'{title}'" if not is_int else f'{title}'
        if self.isEmpty:
            self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name}(id, {self.title}) VALUES (1, {title})")
        else:
            self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name}({self.title}) VALUES ({title})")
        self.isEmpty = False

        return self.find_id_by_name(title)


    # Возвращает True, если объект по указанному id или title был найден и удален
    # Иначе False
    def del_obj(self, title=None, obj_id=None) -> bool:
        if title and self.find_id_by_name(title):
            self.cur.execute(f"DELETE FROM {self.schema}.{self.table_name} WHERE {self.title} = '{title}'")
            self.is_empty_table()
            return True
        elif obj_id and self.find_name_by_id(obj_id):
            self.cur.execute(f"DELETE FROM {self.schema}.{self.table_name} WHERE id = {obj_id}")
            self.is_empty_table()
            return True

        return False


class BasicTableWithoutSerialType(BasicTable):
    def __init__(self, table_name, table_title, cur, conn):
        super().__init__(table_name, table_title, cur, conn)

    def add(self, title: str) -> int:
        obj_id = self.find_id_by_name(title)
        if obj_id:
            return obj_id

        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} ORDER BY id")
        obj_id = self.cur.fetchall()
        if not obj_id:
            obj_id = 1
        else:
            obj_id = obj_id[-1][0] + 1
        self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ({obj_id}, '{title}')")

        return obj_id


class BasicTable3(BasicTable):
    def __init__(self, table_name, first_table_title, second_table_title, cur, conn):
        super().__init__(table_name=table_name, table_title=[first_table_title, second_table_title], cur=cur, conn=conn)

    def find_id_by_name(self, title: str) -> int:
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} WHERE {self.title[1]} like '{title}'")
        obj = self.cur.fetchall()

        return obj[0][0] if obj else False

    def find_name_by_id(self, obj_id: int) -> int:
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id = {obj_id}")
        obj = self.cur.fetchall()

        return obj[0][2] if obj else False

    def add(self, first_title, second_title) -> int:
        obj_id = self.find_id_by_name(second_title)
        if obj_id:
            return obj_id
        print(obj_id)
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} ORDER BY id")
        obj_id = self.cur.fetchall()
        print(obj_id)
        if not obj_id:
            obj_id = 1
        else:
            obj_id = obj_id[-1][0] + 1
        self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ({obj_id}, {first_title}, '{second_title}')")

        return obj_id
from PyScripts.base.base_functions import db_conn


class ResponseObjects:
    def __init__(self):
        self.table_name = "response_obj"
        self.schema = "public"
        self.cur, self.conn = db_conn()

    # Возвращает id ответственного объекта по его title
    # False, если такого объекта нет
    def find_id_by_name(self, title):
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE response_obj like '{title}'")
        resp_obj = self.cur.fetchall()

        return resp_obj[0][0] if resp_obj else False

    # Возвращает title ответственного объекта по его id
    # False, если такого объекта нет
    def find_name_by_id(self, obj_id):
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id = {obj_id}")
        resp_obj = self.cur.fetchall()

        return resp_obj[0][1] if resp_obj else False

    # Добавление нового объекта только по title
    # Возвращает id объекта
    def add_new(self, title):
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} ORDER BY id")
        obj_id = self.cur.fetchall()[-1][0] + 1
        self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ({obj_id}, '{title}')")
        self.conn.commit()

        return obj_id


rp = ResponseObjects()

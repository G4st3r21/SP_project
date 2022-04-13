from PyScripts.TableClasses.PublicClasses.BasicTables import BasicTableWithoutSerialType


class GosprogramVO(BasicTableWithoutSerialType):
    def __init__(self, cur, conn):
        super().__init__(table_name='gosprogram_vo', table_title='title_prog', cur=cur, conn=conn)

    def find_id_by_name(self, title: str) -> str:
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} WHERE {self.title} like '{title}'")
        obj = self.cur.fetchall()

        return obj[0][0] if obj else False

    def find_name_by_id(self, obj_id: str) -> str:
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id like '{obj_id}'")
        obj = self.cur.fetchall()

        return obj[0][1] if obj else False

    def add_new(self, id_obj, title, ) -> str:
        obj_id = self.find_id_by_name(title)
        if obj_id:
            return obj_id
        self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ('{id_obj}', '{title}')")
        self.isEmpty = False

        return id_obj

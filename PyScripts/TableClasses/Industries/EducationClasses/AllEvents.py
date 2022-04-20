from PyScripts.TableClasses.PublicClasses.SPTable import SPTable


class AllEvents(SPTable):
    def __init__(self, year, cur, conn):
        super().__init__(table_name='all_events'+year, table_title='events', cur=cur, conn=conn)
        self.schema = 'Education'

    def get_id_by_name(self, title: str) -> str:
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} WHERE {self.title} like '{title}'")
        obj = self.cur.fetchall()

        return obj[0][0] if obj else False

    def get_name_by_id(self, obj_id: str) -> str:
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id like '{obj_id}'")
        obj = self.cur.fetchall()

        return obj[0][1] if obj else False

    def add(self, id_obj, title: str) -> str:
        obj_id = self.get_id_by_name(title)
        if obj_id:
            return obj_id
        self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ('{id_obj}', '{title}')")
        self.isEmpty = False

        return id_obj

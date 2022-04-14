from PyScripts.TableClasses.PublicClasses.BasicTables import BasicTableWithoutSerialType


class GosprogramTasks(BasicTableWithoutSerialType):
    def __init__(self, cur, conn):
        super().__init__(table_name='tasks', table_title='task', cur=cur, conn=conn)

    def add(self, cyr_id, title) -> int:
        obj_id = self.find_id_by_name(title)
        if obj_id:
            return obj_id

        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} ORDER BY id")
        obj_id = self.cur.fetchall()
        if not obj_id:
            obj_id = 1
        else:
            obj_id = obj_id[-1][0] + 1
        self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ({obj_id}, '{cyr_id}', '{title}')")

        return obj_id

from PyScripts.TableClasses.PublicClasses.BasicTables import BasicTable


class GosprogramTasks(BasicTable):
    def __init__(self, cur, conn):
        super().__init__(table_name='gosprogram_tasks', table_title='id_task', cur=cur, conn=conn)

    def find_id_prog_by_id_task(self, id_task: str) -> int:
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} WHERE {self.title} like '{id_task}'")
        obj = self.cur.fetchall()

        return obj[0][0] if obj else False

    def find_id_task_by_id_prog(self, id_prog: int) -> str:
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id_prog = {id_prog}")
        obj = self.cur.fetchall()

        return obj[0][1] if obj else False

    def add_new(self, id_prog, id_task) -> int:
        obj_id = self.find_id_prog_by_id_task(id_task)
        if obj_id:
            return obj_id
        self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ({id_prog}, '{id_task}')")
        self.isEmpty = False

        return self.find_id_prog_by_id_task(id_task)

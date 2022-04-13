from PyScripts.TableClasses.PublicClasses.BasicTables import BasicTable


class ControlEvent(BasicTable):
    def __init__(self, cur, conn):
        super().__init__(table_name='control_event2020', table_title='control_event', cur=cur, conn=conn)

    def find_id_by_name(self, title: str) -> int:
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} WHERE {self.title} like '{title}'")
        obj = self.cur.fetchall()

        return obj[0][0] if obj else False

    def find_all(self, obj_code=False, code_main_event=False, control_event=False):
        if obj_code:
            self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} WHERE code like '{obj_code}'")
        elif code_main_event:
            self.cur.execute(
                f"SELECT * FROM {self.schema}.{self.table_name} WHERE code_main_event like '{code_main_event}'")
        elif control_event:
            self.cur.execute(
                f"SELECT * FROM {self.schema}.{self.table_name} WHERE control_event like '{control_event}'")

        obj = self.cur.fetchall()
        if obj:
            return obj if obj else False

    def find_name_by_id(self, code: str) -> str:
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE code = '{code}'")
        obj = self.cur.fetchall()

        return obj[0][1] if obj else False

    def add_new(self, obj_code, code_main_event, control_event):
        obj_id = self.find_id_by_name(control_event)
        if obj_id:
            return obj_id
        self.cur.execute(
            f"INSERT INTO {self.schema}.{self.table_name}VALUES ('{obj_code}', '{code_main_event}', '{control_event}')")
        self.isEmpty = False

        return obj_code

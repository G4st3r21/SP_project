class GosprogramTarget:
    def __init__(self, cur, conn):
        self.table_name = "gosprogram_target"
        self.schema = "public"
        self.cur, self.conn = cur, conn

    def commit(self):
        self.conn.commit()

    def get_all_by_id(self, obj_id):
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id_prog = '{obj_id}'")
        event = self.cur.fetchall()

        return event[0] if event else False

    def add(self, id_prog, id_target):
        event_id = self.get_all_by_id(id_prog)
        if event_id:
            return event_id
        self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES"
                         f" ('{id_prog}', {id_target})")

        return id_prog
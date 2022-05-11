class GosprogramVO:
    def __init__(self, cur, conn):
        self.table_name = "gosprogram_vo"
        self.schema = "public"
        self.cur, self.conn = cur, conn

    def commit(self):
        self.conn.commit()

    def get_id_by_name(self, title):
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id_prog like '{title}'")
        main_event_id = self.cur.fetchall()

        return main_event_id[0][0] if main_event_id else False

    def get_all_by_id(self, obj_id):
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id = '{obj_id}'")
        event = self.cur.fetchall()

        return event[0] if event else False

    def add(self, id_prog, id_response, id_ind_rf, id_ind_vo):
        obj_id = self.get_id_by_name(id_prog)
        if obj_id:
            return obj_id

        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} ORDER BY id")
        obj_id = self.cur.fetchall()
        if not obj_id:
            obj_id = 1
        else:
            obj_id = obj_id[-1][0] + 1
        self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ({obj_id}, "
                         f"'{id_prog}', {id_response}, {id_ind_rf}, {id_ind_vo})")

        return obj_id
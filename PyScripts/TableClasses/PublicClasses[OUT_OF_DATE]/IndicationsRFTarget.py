class IndicationsRFTarget:
    def __init__(self, cur, conn):
        self.table_name = "indications_rf_target"
        self.schema = "public"
        self.cur, self.conn = cur, conn

    def commit(self):
        self.conn.commit()

    def get_id_by_id_target(self, id_target):
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id_target = {id_target}")
        main_event_id = self.cur.fetchall()

        return main_event_id[0][0] if main_event_id else False

    def get_all_by_id(self, obj_id):
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id_ind_rf = '{obj_id}'")
        event = self.cur.fetchall()

        return event[0] if event else False

    def add(self, id_ind_rf, id_target):
        event_id = self.get_id_by_id_target(id_target)
        if event_id:
            return event_id
        self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES"
                         f" ({id_ind_rf}, {id_target})")

        return self.get_id_by_id_target(id_target)
def char_index_from_number(number):
    if isinstance(number, str):
        n = int(number, 10)
    else:
        n = int(number)
        # now convert decimal to 'to_base' base
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < len(alphabet):
        return alphabet[n]
    else:
        return char_index_from_number(n // len(alphabet) - 1) + alphabet[n % len(alphabet)]


def number_from_char_index(str_id):
    str_id = str_id[::-1]
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    number = alphabet.index(str_id[0]) + 1
    if len(str_id) == 1:
        return alphabet.index(str_id[0])
    for i in range(1, len(str_id)):
        number += (alphabet.index(str_id[i]) + 1) * len(alphabet) * i

    return number - 1


class Gosprogram:
    def __init__(self, cur, conn):
        self.table_name = "gosprogram"
        self.schema = "public"
        self.cur, self.conn = cur, conn

    def commit(self):
        self.conn.commit()

    # Возвращает id ответственного объекта по его title
    # False, если такого объекта нет
    def find_id_by_name(self, title, id_type=str):
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE title_prog like '{title}'")
        gp = self.cur.fetchall()
        if id_type == int:
            return number_from_char_index(gp[0][0]) if gp else False

        return gp[0][0] if gp else False

    # Возвращает title ответственного объекта по его id
    # False, если такого объекта нет
    def find_name_by_id(self, gp_id):
        gp_id = gp_id if gp_id is str else char_index_from_number(gp_id)
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} * WHERE id = {gp_id}")
        gp = self.cur.fetchall()

        return gp[0][1] if gp else False

    # Добавление нового объекта только по title
    # Возвращает id объекта
    def add_new(self, title):
        obj_id = self.find_id_by_name(title)
        if obj_id:
            return obj_id
        self.cur.execute(f"SELECT * FROM {self.schema}.{self.table_name} ORDER BY length(id), id")
        gp_id = char_index_from_number(number_from_char_index(self.cur.fetchall()[-1][0]) + 1)
        self.cur.execute(f"INSERT INTO {self.schema}.{self.table_name} VALUES ('{gp_id}', '{title}')")

        return gp_id

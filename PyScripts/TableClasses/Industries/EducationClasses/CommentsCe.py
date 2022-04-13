from PyScripts.TableClasses.PublicClasses.BasicTables import BasicTable


class CommentsCe(BasicTable):
    def __init__(self, cur, conn):
        super().__init__(table_name='comments_ce2020', table_title='comments', cur=cur, conn=conn)

    
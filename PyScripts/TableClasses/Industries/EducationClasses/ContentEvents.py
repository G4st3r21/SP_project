from PyScripts.TableClasses.PublicClasses.BasicTables import BasicTable


class ContentEvents(BasicTable):
    def __init__(self, year, cur, conn):
        super().__init__(table_name='content_events'+year, table_title='content', cur=cur, conn=conn)
        self.schema = 'Education'

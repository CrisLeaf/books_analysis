import psycopg2

class BooksScraperPipeline(object):

    def open_spider(seld, spider):
        host = "localhosts"
        user = "postgres"
        password = "password"
        dbname = "booksdb"
        try:
            self.connection = psycopg2.connect(
                    host=host, user=user, password=password, dbname=dbname
                )
        except:
            raise ConnectionError("Unable to connect to {dbname}.")
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                f"INSERT INTO books(bk_id, bk_name, bk_author, ws_id) \
                values (1, 'crislan', 'cris', 3)";
            )
            self.connection.commit()
        except:
            self.connection.rollback()
            raise
        return item

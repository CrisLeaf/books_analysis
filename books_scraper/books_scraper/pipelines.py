import psycopg2
from datetime import date

class BooksScraperPipeline(object):

    def open_spider(self, spider):
        host = "localhost"
        user = "postgres"
        password = "password"
        dbname = "booksdb"
        try:
            self.connection = psycopg2.connect(
                    host=host, user=user, password=password, dbname=dbname
                )
        except:
            raise ConnectionError("Unable to connect to {dbname}")
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(f"SELECT * FROM websites WHERE name = '{item['website'][0]}'")
            record = self.cursor.fetchall()
            ws_id = record[0][0]
            self.cursor.execute(f"SELECT * FROM books WHERE link = '{item['link']}'")
            record = self.cursor.fetchall()
            if not record:
                self.cursor.execute(f"INSERT INTO books(name, author, link, ws_id) VALUES('{item['name']}', '{item['author']}', '{item['link']}', {ws_id})")
                self.connection.commit()
                self.cursor.execute(f"SELECT bk_id FROM books WHERE link = '{item['link']}'")
                record = self.cursor.fetchall()
                last_id = record[0][0]
                self.cursor.execute(f"INSERT INTO prices(bk_id, price, date) VALUES('{last_id}' , {item['price']}, '{date.today()}')")
                self.connection.commit()
            else:
                self.cursor.execute(f"SELECT bk_id FROM books WHERE link = '{item['link']}'")
                record = self.cursor.fetchall()
                last_id = record[0][0]
                self.cursor.execute(f"INSERT INTO prices(bk_id, price, date) VALUES('{last_id}' , {item['price']}, '{date.today()}')")
                self.connection.commit()
        except:
            self.connection.rollback()
            raise
        return item
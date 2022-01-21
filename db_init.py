import psycopg2
from psql_secrets import psql_params


def reset_tables():
	commands = (
		"""
		DROP TABLE IF EXISTS books
		""",
		"""
		DROP TABLE IF EXISTS websites
		""",
		"""
		CREATE TABLE websites (
			id SERIAL PRIMARY KEY,
			web_name TEXT
		)
		""",
		"""
		CREATE TABLE books (
			id SERIAL PRIMARY KEY,
			book_url TEXT NOT NULL UNIQUE,
			book_review TEXT NOT NULL,
			book_category TEXT NOT NULL,
			web INT,
			CONSTRAINT fk_web FOREIGN KEY (web) REFERENCES websites(id)
		)
		"""
	)
	
	conn = psycopg2.connect(**psql_params)
	curr = conn.cursor()
	
	for command in commands:
		curr.execute(command)
	
	print("Base de datos creada")
	
	conn.commit()
	curr.close()
	conn.close()


if __name__ == "__main__":
	reset_tables()

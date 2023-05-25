import sqlite3
from sqlite3 import Error

class items_database:

	def create_connection(db_file):

		conn = None
		try:
			conn = sqlite3.connect(db_file)
		except Error as e:
			print(e)

		return conn

	def create_table(conn, create_table_sql):

		try:
			c = conn.cursor()
			c.execute(create_table_sql)
		except Error as e:
			print(e)
			

			##ITEMS##

	def create_items(conn, items):
		sql = ''' INSERT INTO items(item,price)
					VALUES(?,?)'''
		cur = conn.cursor()
		cur.execute(sql, items)
		conn.commit()

		return cur.lastrowid

	def select_items(conn):
		cur = conn.cursor()
		cur.execute("SELECT * FROM items")
		rows = cur.fetchall()

		return rows

	def delete_item(conn, id):
		sql = 'DELETE FROM items WHERE id=?'
		cur = conn.cursor()
		cur.execute(sql, (id,))
		conn.commit()

			##STORAGE##

	def create_storage(conn, storage):
		sql = ''' INSERT INTO storage(item, amount)
					VALUES(?,?)'''
		cur = conn.cursor()
		cur.execute(sql, storage)
		conn.commit()
		
		return cur.lastrowid

	def select_all_from_storage(conn):
		cur = conn.cursor()
		cur.execute("SELECT * FROM storage")
		rows = cur.fetchall()
		return rows

	def select_item_amount_by_id(conn, id):
		cur = conn.cursor()
		cur.execute("SELECT * FROM storage WHERE id=?", (id,))
		rows = cur.fetchall()
		return rows[0][2]

	def update_amount(conn, storage):
		sql = ''' 	UPDATE storage
					SET amount = ?
					WHERE id = ?'''
		cur = conn.cursor()
		cur.execute(sql, storage)
		conn.commit()

	def setup():

		database = r"database.db"
		conn = items_database.create_connection(database)

		sql_storage = """ CREATE TABLE IF NOT EXISTS storage (
							id integer PRIMARY KEY,
							item text NOT NULL,
							amount integer NOT NULL
						); """

		sql_items = """ CREATE TABLE IF NOT EXISTS items (
							id integer PRIMARY KEY,
							item text NOT NULL,
							price text NOT NULL
						); """

		if conn != None:
			items_database.create_table(conn, sql_storage)
			items_database.create_table(conn, sql_items)
		else:
				print("Error! No connection with database.")

		items_list = [  ["Banana", "1.00"],
                		["Cokolada", "2.00"],
                		["Igracka", "20.00"],
                		["Jabuka", "0.50"],
                		["Jaja", "0.75"],
                		["Kruh", "1.20"],
                		["Mlijeko", "2.50"],
                		["Sladoled", "3.00"],
                		["Vino", "10.00"],
                		["Voda", "1.50"]
                                        ]

		for i in items_list:
			with conn:
				storage = (i[0], 100)
				storage_id = items_database.create_storage(conn, storage)

				items = (i[0], i[1])
				items_id = items_database.create_items(conn, items)

		conn.close()
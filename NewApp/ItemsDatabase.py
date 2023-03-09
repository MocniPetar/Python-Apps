import sqlite3
from sqlite3 import Error

class items_database:

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


#database = r"database.db"
#conn = save_to_database.create_connection(database)
#
#sql_items = """ CREATE TABLE IF NOT EXISTS items (
#                    id integer PRIMARY KEY,
#                    item text NOT NULL,
#                    price text NOT NULL
#                ); """
#
#if conn != None:
#    save_to_database.create_table(conn, sql_items)
#else:
#        print("Error! No connection with database.")
#
#items_list = [  ["Banana", "1.00"],
#                ["Cokolada", "2.00"],
#                ["Igracka", "20.00"],
#                ["Jabuka", "0.50"],
#                ["Jaja", "0.75"],
#                ["Kruh", "1.20"],
#                ["Mlijeko", "2.50"],
#                ["Sladoled", "3.00"],
#                ["Vino", "10.00"],
#                ["Voda", "1.50"]
#                                        ]
#
#for i in items_list:
#    with conn:
#        items = (i[0], i[1])
#        items_id = save_to_database.create_items(conn, items)
#
#conn.close()
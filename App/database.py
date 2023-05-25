import sqlite3
from sqlite3 import Error

class save_to_database:
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
            
            ## TASKS ##       
    
    def create_task(conn, task):
        sql = ''' INSERT INTO tasks(name,description,state)
                    VALUES(?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid
    
    def select_every_task(conn):
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks")
        rows = cur.fetchall()
        return rows
    
    def delete_every_task(conn):
        sql = 'DELETE FROM tasks'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    
    def delete_task(conn, id):
        sql = 'DELETE FROM tasks WHERE id=?'
        cur = conn.cursor()
        cur.execute(sql, (id,))
        conn.commit()

    def set_state(conn, task):
        sql = '''   UPDATE tasks
                    SET state = ?
                    WHERE id = ?'''

        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit() 
                    
            ## PHONEBOOK ##    
    
    def create_phonebook(conn, phonebook):
        sql = ''' INSERT INTO phonebook(name,number)
                    VALUES(?,?)'''
        cur = conn.cursor()
        cur.execute(sql, phonebook)
        conn.commit()
        return cur.lastrowid
    
    def delete_phonebook(conn, id):
        sql = 'DELETE FROM phonebook WHERE id=?'
        cur = conn.cursor()
        cur.execute(sql, (id,))     
        conn.commit()
        
    def delete_whole_phonebook(conn):
        sql = 'DELETE FROM phonebook'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    def select_all_phonebook(conn):
        cur = conn.cursor()
        cur.execute("SELECT * FROM phonebook")
        rows = cur.fetchall()
        return rows
    
            ## BILLS ##
            
    def create_bills(conn, bills):
        sql = ''' INSERT INTO bills(name,date,item,amount,price)
                    VALUES(?,?,?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, bills)
        conn.commit()
        return cur.lastrowid
    
    def delete_bills(conn, id):
        sql = 'DELETE FROM bills WHERE id=?'
        cur = conn.cursor()
        cur.execute(sql, (id,))
        conn.commit()
        
    def selec_all_bills(conn):
        cur = conn.cursor()
        cur.execute("SELECT * FROM bills")
        rows = cur.fetchall()
        return rows
    
    def select_bill(conn, name):
        cur = conn.cursor()
        cur.execute("SELECT * FROM bills WHERE name=?", (name,))
        rows = cur.fetchall()
        return rows

        ##UPDATING THE DATABASE##

    def database_control():

        database = r"database.db"
        conn = save_to_database.create_connection(database)
        
        sql_tasks = """ CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    description text NOT NULL,
                                    state intger NOT NULL
                                ); """
        
        if conn != None:
            save_to_database.create_table(conn, sql_tasks)
        else:
                print("Error! No connection with database.")
        
        conn.close()
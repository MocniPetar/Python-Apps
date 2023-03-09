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
        sql = ''' INSERT INTO tasks(name,description)
                    VALUES(?,?)'''
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
import sqlite3

def create_db():
    con = sqlite3.connect(database=r'IMS.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee (eid INTEGER PRIMARY KEY AUTOINCREMENT,  gender text,  contact text,  name text,  DOJ text,  DOB text,  email text,  pass text,  utype text,  salary text,  address text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS supplier (invoice INTEGER PRIMARY KEY AUTOINCREMENT,  contact text,  name text, desc  text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS category (cid INTEGER PRIMARY KEY AUTOINCREMENT,   name text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS product  (pid INTEGER PRIMARY KEY AUTOINCREMENT,category, supplier, name, price, quantity, status,total_cost)")
    con.commit()
    
   
# Call the function to create the database and table
create_db()
 
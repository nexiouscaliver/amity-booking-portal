import sqlite3
import hashlib
import sys
import os

dbname = "user.db"


def init_db():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    q1 = "CREATE TABLE IF NOT EXISTS user(id int auto increment , username text primary key, password text, name text);"
    cur.execute(q1)
    q1 = "CREATE TABLE IF NOT EXISTS doc(id int auto increment , username text primary key, password text, name text);"
    cur.execute(q1)
    cur.close()
    print("SQL init compleated!")
    conn.commit()
    conn.close()


def create_user(username:str,password:str,name:str):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    hpass = hashlib.md5(password.encode()).hexdigest()
    sql = f'insert into user(username,password,name) values ("{username}","{hpass}","{name}");'
    try:
        cur.execute(sql)
        print(f"User {username}::{password} successfully generated")
        return True
    except sqlite3.Error as error:
        print(f"SQL Error Occured:: {username} :: {error}")
        return False
    except Exception as e:
        print(f"PY Error Occured:: {username} :: {e}")
        return False
    finally:
        cur.close()
        conn.commit()
        conn.close()

def load_user(username:str,password:str):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    uhpass = hashlib.md5(password.encode()).hexdigest()
    sql = f'select password from user where username="{username}";'
    try:
        cur.execute(sql)
        shpass = cur.fetchall()
        #print(shpass)
        if shpass == []:
            print(f"USER User {username} not found")
            return False
        elif uhpass == shpass[0][0]:
            print(f"User {username} has correct password {password}")
            return True
        elif shpass == []:
            print(f"USER User {username} not found")
            return False
        else:
            print(f"USER Incorrect password :: {username}")
            return False
    except sqlite3.Error as error:
        print(f"SQL Error occured :: {username} :: {error}")
        return False
    except Exception as e:
        print(f"PY Error Occured:: {username} :: {e}")
        return False
    finally:
        cur.close()
        conn.commit()
        conn.close()


def getname_user(username:str):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    sql = f'select name from user where username="{username}";'
    try:
        cur.execute(sql)
        shpass = cur.fetchall()
        #print(shpass)
        if shpass == []:
            print(f"USER User {username} not found")
            return False
        if shpass:
            print(f"User {username} has full name {shpass[0][0]}")
            return shpass[0][0]
        else:
            print(f"USER Incorrect password :: {username}")
            return False
    except sqlite3.Error as error:
        print(f"SQL Error occured :: {username} :: {error}")
        return False
    except Exception as e:
        print(f"PY Error Occured:: {username} :: {e}")
        return False
    finally:
        cur.close()
        conn.commit()
        conn.close()









        

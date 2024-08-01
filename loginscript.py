import mysql.connector
import hashlib
import sys
import os

hostname = "127.0.0.1"
username="root"
passwd = "3388"
portnum = "3388"

try:
    conn = mysql.connector.connect(
    host=hostname,
    user=username,
    password=passwd,
    port = portnum,
    database = "amilogin"
    )
except Exception as e:
    print("Error in connection : ",e)
    print("Reconnecting to server and creating database")
    conntemp = mysql.connector.connect(
    host=hostname,
    user=username,
    password=passwd,
    port = portnum,
    )
    c = conntemp.cursor(buffered=True)
    sql = "create database if not exists amilogin;"
    c.execute(sql)
    conntemp.commit()
    conntemp.close()
    print("Database created! Reconnecting to server...")

conn = mysql.connector.connect(
    host=hostname,
    user=username,
    password=passwd,
    port = portnum,
    database = "amilogin"
    )


def close():
    conn.commit()
    conn.close()

def init_db(): #server
    cur = conn.cursor(buffered=True)
    q1 = "CREATE TABLE IF NOT EXISTS user(username varchar(30) primary key, password varchar(100), name varchar(30));"
    cur.execute(q1)
    q1 = "CREATE TABLE IF NOT EXISTS admin(username varchar(30) primary key, password varchar(100), name varchar(30));"
    cur.execute(q1)
    cur.close()
    create_admin("testadmin",'12345','admin')
    print("SQL init compleated!")
    conn.commit()
    

#email = name
#name = email
def create_user(username:str,password:str,name:str):
    cur = conn.cursor(buffered=True)
    hpass = hashlib.md5(password.encode()).hexdigest()
    sql = f'insert into user(username,password,name) values ("{username}","{hpass}","{name}");'
    try:
        cur.execute(sql)
        print(f"User {username}::{password} successfully generated")
        return True
    except mysql.connector.Error as error:
        print(f"SQL Error Occured:: {username} :: {error}")
        return False
    except Exception as e:
        print(f"PY Error Occured:: {username} :: {e}")
        return False
    finally:
        cur.close()
        conn.commit()
        

def load_user(username:str,password:str):
    cur = conn.cursor(buffered=True)
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
            print(f"User {username} has correct password ")
            return True
        elif shpass == []:
            print(f"USER User {username} not found")
            return False
        else:
            print(f"USER Incorrect password :: {username}")
            return False
    except mysql.connector.Error as error:
        print(f"SQL Error occured :: {username} :: {error}")
        return False
    except Exception as e:
        print(f"PY Error Occured:: {username} :: {e}")
        return False
    finally:
        cur.close()
        conn.commit()

def genhash(password:str):
    return hashlib.md5(password.encode()).hexdigest()

def cmd(s):       #idle-de-bugging
    c = conn.cursor(buffered=True)
    c.execute(s)
    b=c.fetchall()
    # print(b)
    # print('type : ',type(b))
    # print('len : ',len(b))
    conn.commit()
    return {"DATABASE" :"logindb","Command" :s,"data": b,"type" :str(type(b)),"len" :len(b)}

def getname_user(username:str):
    cur = conn.cursor(buffered=True)
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
    except mysql.connector.Error as error:
        print(f"SQL Error occured :: {username} :: {error}")
        return False
    except Exception as e:
        print(f"PY Error Occured:: {username} :: {e}")
        return False
    finally:
        cur.close()
        conn.commit()
        
def seeall():
    cur = conn.cursor(buffered=True)
    sql = f'select * from user;'
    cur.execute(sql)
    o = cur.fetchall()
    d = {}
    d['user'] = o
    sql = f'select * from admin;'
    cur.execute(sql)
    o = cur.fetchall()
    d['admin'] = o
    return d

def create_admin(username:str,password:str,name:str):
    cur = conn.cursor(buffered=True)
    hpass = hashlib.md5(password.encode()).hexdigest()
    sql = f'insert into admin(username,password,name) values ("{username}","{hpass}","{name}");'
    try:
        cur.execute(sql)
        # print(f"admin {username}::{password} successfully generated")
        return True
    except mysql.connector.Error as error:
        print(f"SQL Error Occured:: {username} :: {error}")
        return False
    except Exception as e:
        print(f"PY Error Occured:: {username} :: {e}")
        return False
    finally:
        cur.close()
        conn.commit()
        

def load_admin(username:str,password:str):
    cur = conn.cursor(buffered=True)
    uhpass = hashlib.md5(password.encode()).hexdigest()
    sql = f'select password from admin where username="{username}";'
    try:
        cur.execute(sql)
        shpass = cur.fetchall()
        #print(shpass)
        if shpass == []:
            print(f"USER admin {username} not found")
            return False
        elif uhpass == shpass[0][0]:
            print(f"admin {username} has correct password ")
            return True
        elif shpass == []:
            print(f"USER admin {username} not found")
            return False
        else:
            print(f"admin Incorrect password :: {username}")
            return False
    except mysql.connector.Error as error:
        print(f"SQL Error occured :: {username} :: {error}")
        return False
    except Exception as e:
        print(f"PY Error Occured:: {username} :: {e}")
        return False
    finally:
        cur.close()
        conn.commit()
        

def getname_admin(username:str):
    cur = conn.cursor(buffered=True)
    sql = f'select name from admin where username="{username}";'
    try:
        cur.execute(sql)
        shpass = cur.fetchall()
        print(shpass)
        if shpass == []:
            print(f"USER admin {username} not found")
            return False
        if shpass:
            print(f"admin {username} has correct name {shpass[0][0]}")
            return shpass[0][0]
        else:
            print(f"admin Incorrect password :: {username}")
            return False
    except mysql.connector.Error as error:
        print(f"SQL Error occured :: {username} :: {error}")
        return False
    except Exception as e:
        print(f"PY Error Occured:: {username} :: {e}")
        return False
    finally:
        cur.close()
        conn.commit()
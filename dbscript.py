import sqlite3
#conn = sqlite3.connect("test1.db")
#c = conn.cursor()
#conn.commit()
#conn.close()

def cmd(s):
    conn = sqlite3.connect("test1.db")
    c = conn.cursor()
    a=c.execute(s)
    b=a.fetchall()
    print(b)
    print('type : ',type(b))
    print('len : ',len(b))
    conn.commit()
    conn.close()

def see(table):
    conn = sqlite3.connect("test1.db")
    c = conn.cursor()
    a=c.execute(f'select * from {table};')
    b=a.fetchall()
    for i in b:
        print(i)
    print('type : ',type(b))
    print('len : ',len(b))
    conn.commit()
    conn.close()


def init():  #server
    conn = sqlite3.connect("test1.db")
    c = conn.cursor()
    sql = "create table if not exists halls(hallid integer primary key autoincrement,hallname varchar(35));"
    c.execute(sql)
    sql = "create table if not exists book(bookid integer primary key autoincrement , hallid integer, school varchar(50) , date varchar(20) , stime integer, etime integer , event text);"
    c.execute(sql)
    sql = "create table if not exists confirm(bookid integer primary key , hallid integer, school varchar(50) , date varchar(20) , stime integer, etime integer , event text);"
    c.execute(sql)
    sql = "create table if not exists reject(bookid integer primary key , hallid integer, school varchar(50) , date varchar(20) , stime integer, etime integer , event text);"
    c.execute(sql)
    sql = "create table if not exists userreq(userid integer primary key autoincrement , username text , bookid integer)"
    c.execute(sql)
    sql = "create table if not exists status(bookid integer primary key , state varchar(15))"
    c.execute(sql)
    try:
        sql='select * from halls;'
        a=c.execute(sql)
        o=a.fetchall()
        s=[(1, 'audi'), (2, 'sem'), (3, 'a2'), (4, 'crc')]
        if(o==s):
            pass
        else:
            sql='insert into halls(hallname) values("audi"),("sem"),("a2"),("crc")'
            c.execute(sql)
    except:
        pass
    conn.commit()
    conn.close()


def request_hall(hallid:int , school:str , date:str , stime:int , etime:int , event:str , username:str):  #user
    conn = sqlite3.connect("test1.db")
    c = conn.cursor()
    sql=f'insert into book(hallid,school,date,stime,etime,event) values({hallid},"{school}","{date}",{stime},{etime},"{event}");'
    c.execute(sql)
    sql='select * from book'
    a = c.execute(sql)
    o = a.fetchall()
    last = o[-1]
    bid = last[0]
    sql=f'insert into userreq(username,bookid) values("{username}",{bid})'
    c.execute(sql)
    sql=f'insert into status(bookid,state) values({bid},"pending")'
    c.execute(sql)
    conn.commit()
    conn.close()
    return bid

def check_request(username:str):   #user
    conn = sqlite3.connect("test1.db")
    c = conn.cursor()    
    sql=f'select * from userreq where username="{username}"'
    a = c.execute(sql)
    o = a.fetchall()
    q=[]
    for i in o:
        bid = i[2]
        sql=f'select state from status where bookid={bid}'
        a = c.execute(sql)
        o = a.fetchall()
        l = [bid,o[0][0]]
        q.append(l)
    for i in q:print(i)
    return q
    conn.commit()
    conn.close()

def check_hall(hallid:int , date:str , stime:int , etime:int):   #user
    conn = sqlite3.connect("test1.db")
    c = conn.cursor()
    final=[]
    flag=True
    sql=f'select * from book where hallid={hallid} and date="{date}"'
    a = c.execute(sql)
    o = a.fetchall()
    print(o)
    for i in o:
        final.append(i)
    sql=f'select * from confirm where hallid={hallid} and date="{date}"'
    a = c.execute(sql)
    o = a.fetchall()
    print(o)
    for i in o:
        final.append(i)

    for i in final:
        endtime = i[5]
        if(endtime>stime):
            flag=False

    return flag
        
    conn.commit()
    conn.close()

def confirm_hall(bookid:int):   #admin
    conn = sqlite3.connect("test1.db")
    c = conn.cursor()
    sql=f'select * from book where bookid={bookid};'
    a = c.execute(sql)
    o = a.fetchall()
    s = o[0]
    hallid = s[1]
    school = s[2]
    date = s[3]
    stime = s[4]
    etime = s[5]
    event = s[6]
    sql=f'insert into confirm(bookid,hallid,school,date,stime,etime,event) values({bookid},{hallid},"{school}","{date}",{stime},{etime},"{event}");'
    c.execute(sql)
    sql=f'delete from book where bookid={bookid};'
    c.execute(sql)
    sql=f'update status set state="confirm" where bookid={bookid}'
    c.execute(sql)
    conn.commit()
    conn.close()
    
def reject_hall(bookid:int):      #admin
    conn = sqlite3.connect("test1.db")
    c = conn.cursor()
    sql=f'select * from book where bookid={bookid};'
    a = c.execute(sql)
    o = a.fetchall()
    s = o[0]
    hallid = s[1]
    school = s[2]
    date = s[3]
    stime = s[4]
    etime = s[5]
    event = s[6]
    sql=f'insert into reject(bookid,hallid,school,date,stime,etime,event) values({bookid},{hallid},"{school}","{date}",{stime},{etime},"{event}");'
    c.execute(sql)
    sql=f'delete from book where bookid={bookid};'
    c.execute(sql)
    sql=f'update status set state="reject" where bookid={bookid}'
    c.execute(sql)
    conn.commit()
    conn.close()





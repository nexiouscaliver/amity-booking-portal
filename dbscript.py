import sqlite3
#conn = sqlite3.connect("test1.db")
#c = conn.cursor()
#conn.commit()
#conn.close()

dbname = "data.db"

def cmd(s):       #idle-de-bugging
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    a=c.execute(s)
    b=a.fetchall()
    print(b)
    print('type : ',type(b))
    print('len : ',len(b))
    conn.commit()
    conn.close()

def see(table):       #idle-de-bugging
    conn = sqlite3.connect(dbname)
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
    conn = sqlite3.connect(dbname)
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
    sql = "create table if not exists info(bookid integer primary key, hallid integer , schoolname text , fname text , hod text , eventname text ,date text , stime text , etime text, email text , phone text , rpname text , rpdetail text)"
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


#user flow -> check_hall:request_hall | reject / check_request
#admin flow -> check_pending:confirm_hall:reject_hall

def request_hall(hallid:int , school:str , date:str , stime:int , etime:int , event:str , username:str):  #user
    conn = sqlite3.connect(dbname)
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

def info_dump(bookid:int, hallid:int , school:str, fname:str, hod:str, email:str , phone:str , date:str , stime:int , etime:int , event:str ,rpname:str , rpdetail:str):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    sql=f'insert into info values({bookid}, {hallid} , "{school}", "{fname}", "{hod}", "{event}","{date}", "{stime}", "{etime}", "{email}", "{phone}", "{rpname}", "{rpdetail}")'
    c.execute(sql)
    conn.commit()
    conn.close()

def info_fetch(bookid:int):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    sql = f'select * from info where bookid={bookid};'
    f = c.execute(sql)
    o = f.fetchall()
    conn.commit()
    conn.close()
    return o

def check_request(username:str):   #user
    conn = sqlite3.connect(dbname)
    c = conn.cursor()    
    sql=f'select * from userreq where username="{username}"'
    a = c.execute(sql)
    o = a.fetchall()
    q=[]
    for i in o:
        bid = i[2]
        # print(bid)
        sql=f'select state from status where bookid={bid}'
        # print(sql)
        a = c.execute(sql)
        o = a.fetchall()
        status = o[0][0]
        # print(status)
        sql=f'select * from info where bookid={bid}'
        # print(sql)
        f = c.execute(sql)
        p = f.fetchall()
        print(p)
        # print(p)
        if (status == "confirm"):
            status = 'Confirmed'
        elif (status == "reject"):
            status = 'Rejected'
        elif (status == "pending"):
            status = "Pending"
        l = [bid,p[0][1],p[0][2],p[0][6],p[0][5],p[0][8],status]
        q.append(l)
    for i in q:print(i)
    conn.commit()
    conn.close()
    return q
    

def check_hall(hallid:int , date:str , stime:int , etime:int):   #user
    conn = sqlite3.connect(dbname)
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

    conn.commit()
    conn.close()
    return flag

def all_status():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    sql='select * from status;'
    a = c.execute(sql)
    o = a.fetchall()
    conn.commit()
    conn.close()
    return o

def check_pending():    #admin
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    sql='select * from book;'
    a = c.execute(sql)
    o = a.fetchall()
    conn.commit()
    conn.close()
    return o



def confirm_hall(bookid:int):   #admin
    try:
        conn = sqlite3.connect(dbname)
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
        return True
    except:
        return False
    
def reject_hall(bookid:int):      #admin
    try:
        conn = sqlite3.connect(dbname)
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
        return True
    except:
        return False





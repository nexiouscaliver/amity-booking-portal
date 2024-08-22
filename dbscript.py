import mysql.connector

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
    database = "amievent"
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
    ct = conntemp.cursor(buffered=True)
    sql = "create database if not exists amievent;"
    ct.execute(sql)
    conntemp.commit()
    conntemp.close()
    print("Database created! Reconnecting to server...")

conn = mysql.connector.connect(
    host=hostname,
    user=username,
    password=passwd,
    port = portnum,
    database = "amievent"
    )

def close(conn):       #idle-de-bugging
    conn.commit()
    conn.close()

def checkconn(conn):       #idle-de-bugging
    if conn.is_connected():
        return ("Connected to server")
        # return conn
    else:
        return("Not connected to server")
        # try:
        #     conn.reconnect()
        #     if conn.is_connected():
        #         print ("Reconnected to server")
        #         return conn
        #     else:
        #         print ("Failed to reconnect to server")
        #         close(conn)
        #         conn = mysql.connector.connect(
        #             host=hostname,
        #             user=username,
        #             password=passwd,
        #             port = portnum,
        #             database = "amievent"
        #             )
        #         return conn
        # except Exception as e:
        #     print (f"Error during reconnection: {e}")
        #     close(conn)
        #     conn = mysql.connector.connect(
        #         host=hostname,
        #         user=username,
        #         password=passwd,
        #         port = portnum,
        #         database = "amievent"
        #         )
        #     return conn


def cmd(s):       #idle-de-bugging
    if not conn.is_connected(): conn.reconnect()
    c = conn.cursor(buffered=True)
    c.execute(s)
    b=c.fetchall()
    # print(b)
    # print('type : ',type(b))
    # print('len : ',len(b))
    conn.commit()
    return {"DATABASE" :"maindb","Command" :s,"data": b,"type" :str(type(b)),"len" :len(b)}



def see(table):       #idle-de-bugging
    if not conn.is_connected(): conn.reconnect()
    c = conn.cursor(buffered=True)
    c.execute(f'select * from {table};')
    b=c.fetchall()
    for i in b:
        print(i)
    print('type : ',type(b))
    print('len : ',len(b))
    conn.commit()
    


def init():  #server
    c = conn.cursor(buffered=True)
    sql = "create table if not exists halls(hallid integer primary key AUTO_INCREMENT,hallname varchar(35));"
    c.execute(sql)
    sql = "create table if not exists book(bookid integer primary key AUTO_INCREMENT , hallid integer, school varchar(350) , date varchar(20) , stime integer, etime integer , event varchar(350));"
    c.execute(sql)
    sql = "create table if not exists confirm(bookid integer primary key , hallid integer, school varchar(350) , date varchar(20) , stime integer, etime integer , event varchar(350));"
    c.execute(sql)
    sql = "create table if not exists reject(bookid integer primary key , hallid integer, school varchar(350) , date varchar(20) , stime integer, etime integer , event varchar(350));"
    c.execute(sql)
    sql = "create table if not exists userreq(userid integer primary key AUTO_INCREMENT , username varchar(100) , bookid integer);"
    c.execute(sql)
    sql = "create table if not exists status(bookid integer primary key , state varchar(15));"
    c.execute(sql)
    sql = "create table if not exists info(bookid integer primary key, hallid integer , schoolname varchar(350) , fname varchar(100) , hod varchar(100) , eventname varchar(350) ,date varchar(100) , stime varchar(100) , etime varchar(100), email varchar(100) , phone varchar(100) , rpname varchar(100) , rpdetail varchar(350));"
    c.execute(sql)
    try:
        sql='select * from halls;'
        c.execute(sql)
        o=c.fetchall()
        s=[(1, 'audi'), (2, 'sem'), (3, 'a2'), (4, 'crc')]
        if(o==s):
            pass
        else:
            sql='insert into halls(hallname) values("audi"),("sem"),("a2"),("crc");'
            c.execute(sql)
    except:
        pass
    conn.commit()
    


#user flow -> check_hall:request_hall | reject / check_request
#admin flow -> check_pending:confirm_hall:reject_hall

def request_hall(hallid:int , school:str , date:str , stime:int , etime:int , event:str , username:str):  #user  
    if not conn.is_connected(): conn.reconnect()
    c = conn.cursor(buffered=True)
    sql=f'insert into book(hallid,school,date,stime,etime,event) values({hallid},"{school}","{date}",{stime},{etime},"{event}");'
    c.execute(sql)
    sql='select * from book'
    c.execute(sql)
    o = c.fetchall()
    last = o[-1]
    bid = last[0]
    sql=f'insert into userreq(username,bookid) values("{username}",{bid})'
    c.execute(sql)
    sql=f'insert into status(bookid,state) values({bid},"pending")'
    c.execute(sql)
    conn.commit()
    
    return bid

def info_dump(bookid:int, hallid:int , school:str, fname:str, hod:str, email:str , phone:str , date:str , stime:int , etime:int , event:str ,rpname:str , rpdetail:str):
    if not conn.is_connected(): conn.reconnect()
    c = conn.cursor(buffered=True)
    sql=f'insert into info values({bookid}, {hallid} , "{school}", "{fname}", "{hod}", "{event}","{date}", "{stime}", "{etime}", "{email}", "{phone}", "{rpname}", "{rpdetail}")'
    c.execute(sql)
    conn.commit()
    

def info_fetch(bookid:int):
    if not conn.is_connected(): conn.reconnect()
    c = conn.cursor(buffered=True)
    sql = f'select * from info where bookid={bookid};'
    c.execute(sql)
    o = c.fetchall()
    conn.commit()
    
    return o

def check_request(username:str):   #user
    if not conn.is_connected(): conn.reconnect()
    c = conn.cursor(buffered=True)
    sql=f'select * from userreq where username="{username}"'
    c.execute(sql)
    o = c.fetchall()
    q=[]
    for i in o:
        bid = i[2]
        # print(bid)
        sql=f'select state from status where bookid={bid}'
        # print(sql)
        c.execute(sql)
        o = c.fetchall()
        status = o[0][0]
        # print(status)
        sql=f'select * from info where bookid={bid}'
        # print(sql)
        f = c.execute(sql)
        p = c.fetchall()
        # print(p)
        # print(p)
        if (status == "confirm"):
            status = 'Confirmed'
        elif (status == "reject"):
            status = 'Rejected'
        elif (status == "pending"):
            status = "Pending"
        l = [bid,p[0][1],p[0][2],p[0][6],p[0][5],p[0][8],status,p[0][7]]
        q.append(l)
    for i in q:print(i)
    conn.commit()
    
    return q
    

def check_hall(hallid:int , date:str , stime:int , etime:int):   #user
    if not conn.is_connected(): conn.reconnect()
    c = conn.cursor(buffered=True)
    final=[]
    flag=True
    sql=f'select * from book where hallid={hallid} and date="{date}"'    #for rejecting pending req.
    c.execute(sql)
    o = c.fetchall()
    print(o)
    for i in o:
        final.append(i)
    sql=f'select * from confirm where hallid={hallid} and date="{date}"'
    c.execute(sql)
    o = c.fetchall()
    print(o)
    for i in o:
        final.append(i)

    for i in final:
        endtime = i[5]
        if(int(endtime)>int(stime)):
            flag=False

    conn.commit()
    
    return flag

def all_accept_and_pending():
    if not conn.is_connected(): conn.reconnect()
    c = conn.cursor(buffered=True)
    sql='select * from status where state="confirm" or state="pending";'
    c.execute(sql)
    o = c.fetchall()
    conn.commit()
    
    return o

def calender():
    if not conn.is_connected(): conn.reconnect()
    c = conn.cursor(buffered=True)
    # sql='select * from status where state="confirm" or state="pending";'
    sql='select * from status where state="confirm";'
    c.execute(sql)
    o = c.fetchall()
    final=[]
    for i in o:
        bid = i[0]
        sql=f'select date,etime from info where bookid={bid};'
        c.execute(sql)
        f = c.fetchone()
        final.append(list(f))
    for i in final:
        if i[1]==1300 or i[1]=="1300":
            i[1] = "first-half"
        elif i[1]==1700 or i[1]=="1700":
            i[1]= "second-half"
        elif i[1]==1701 or i[1]=="1701":
            i[1]= "full"
    for i in final:
        for j in (final[final.index(i):]):
            if(i[0]==j[0]):
                if(i[1]=="first-half"and j[1]=="second-half"):
                    i[1] = "full"
                    j[1] = "full"
                if(i[1]=="second-half"and j[1]=="first-half"):
                    i[1] = "full"
                    j[1] = "full"
    conn.commit()
    
    return final

def seeall():
    if not conn.is_connected(): conn.reconnect()
    c = conn.cursor(buffered=True)
    x = ['book','confirm','reject','userreq','info','status']
    d = {}
    for i in x:
        sql=f'select * from {i};'
        c.execute(sql)
        o = c.fetchall()
        # print(f"====={i}::TABLE::START=====")
        d[i]=o
        # for j in o:
        #     print(j)
        # print(f"TYPE : {type(i)}")
        # print(f"LEN : {len(i)}")
        # print(f"====={i}::TABLE::END=======")
    return d
def calendermain():
    if not conn.is_connected(): conn.reconnect()
    c = conn.cursor(buffered=True)
    sql='select * from status where state="confirm" or state="pending";'
    # sql='select * from status where state="confirm";'
    c.execute(sql)
    o = c.fetchall()
    # print(o)
    final=[]
    for i in o:
        bid = i[0]
        sql=f'select state from status where bookid={bid};'
        c.execute(sql)
        e = c.fetchone()
        x = e[0]
        if x == "confirm":
            x = "booked"
        sql=f'select date,etime,schoolname,hallid,stime,fname,eventname from info where bookid={bid};'
        c.execute(sql)
        f = c.fetchone()
        f = list(f)
        f.append(x)
        final.append(list(f))
    for i in final:
        # if i[1]==1300 or i[1]=="1300":
        #     i[1] = "first-half-booked"
        # elif i[1]==1700 or i[1]=="1700":
        #     i[1]= "second-half-booked"
        # elif i[1]==1701 or i[1]=="1701":
        #     i[1]= "full-booked"
        if i[3]==1 or i[3]=="1":
            i[3]="Auditorium"
        elif i[3]==2 or i[3]=="2":
            i[3]="Seminar Hall"
        elif i[3]==3 or i[3]=="3":
            i[3]="Room No. 105, A2 Building"
        elif i[3]==4 or i[3]=="4":
            i[3]="CRC Conference Room"
        elif i[3]==5 or i[3]=="5":
            i[3]="AIIT Conference Room"
        elif i[3]==6 or i[3]=="6":
            i[3]="RICS Conference Room"
        elif i[3]==7 or i[3]=="7":
            i[3]="Atrium"
    for i in final:
        for j in (final[final.index(i):]):
            if(i[0]==j[0] and i[3]==j[3]):
                if(i[1]=="first-half-booked"and j[1]=="second-half-booked"):
                    i[1] = "full-booked"
                    j[1] = "full-booked"
                if(i[1]=="second-half-booked"and j[1]=="first-half-booked"):
                    i[1] = "full-booked"
                    j[1] = "full-booked"
    a = []
    s = []
    r = []
    c = []
    d = []
    e = []
    f = []
    for i in final:
        if i[3] == "Auditorium":
            a.append(i)
        if i[3] == "Seminar Hall":
            s.append(i)
        if i[3] == "Room No. 105, A2 Building":
            r.append(i)
        if i[3] == "CRC Conference Room":
            c.append(i)
        if i[3] == "AIIT Conference Roomm":
            d.append(i)
        if i[3] == "RICS Conference Room":
            e.append(i)
        if i[3] == "Atrium":
            f.append(i)
    final2 = []
    final2.append(a)
    final2.append(s)
    final2.append(r)
    final2.append(c)
    final2.append(d)
    final2.append(e)
    final2.append(f)
    # for i in final2:
    #     for j in i:
    #         print(j)
    #         # print(i) 1 ,4
    conn.commit()
    
    return final2

def reject_app(bid:int , status:str):
    if not conn.is_connected(): conn.reconnect()
    if status == "Confirmed":
        c = conn.cursor(buffered=True)
        sql=f'delete from confirm where bookid={bid};'
        c.execute(sql)
        sql=f'delete from userreq where bookid={bid};'
        c.execute(sql)
        sql=f'delete from info where bookid={bid};'
        c.execute(sql)
        sql=f'delete from status where bookid={bid};'
        c.execute(sql)
        conn.commit()
        
        return True
    elif status == "Pending":
        
        c = conn.cursor(buffered=True)
        sql=f'delete from book where bookid={bid};'
        c.execute(sql)
        sql=f'delete from userreq where bookid={bid};'
        c.execute(sql)
        sql=f'delete from info where bookid={bid};'
        c.execute(sql)
        sql=f'delete from status where bookid={bid};'
        c.execute(sql)
        conn.commit()
        
        return True
    return False

def all_status():
    if not conn.is_connected(): conn.reconnect()
    c = conn.cursor(buffered=True)
    sql='select * from status;'
    c.execute(sql)
    o = c.fetchall()
    conn.commit()
    
    return o

def check_pending():    #admin
    if not conn.is_connected(): conn.reconnect()
    c = conn.cursor(buffered=True)
    sql='select * from book;'
    c.execute(sql)
    o = c.fetchall()
    conn.commit()
    
    return o

def reject_hall(bookid:int):      #admin
    if not conn.is_connected(): conn.reconnect()
    try:
        
        c = conn.cursor(buffered=True)
        sql=f'select * from book where bookid={bookid};'
        c.execute(sql)
        o = c.fetchall()
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
        
        return True
    except Exception as e:
        print(e)
        return False

def confirm_hall(bookid:int):   #admin
    if not conn.is_connected(): conn.reconnect()
    try:
        
        c = conn.cursor(buffered=True)
        sql=f'select * from book where bookid={bookid};'
        c.execute(sql)
        o = c.fetchall()
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
        o = check_pending()
        conn.commit()
        
        # print(o)
        for i in o:
            # print(i)
            d = (i[3])
            h = (i[1])
            et = (i[5])
            b = i[0]
            print(d,h,et,"org",date,hallid,etime,"||",b,"|",bookid)
            if(d == date and h == hallid and et == etime and str(b) != str(bookid)):
                reject_hall(int(b))
                print('finaltrigg!!')
                
        
        return True
    except Exception as e:
        print(e)
        return False
    
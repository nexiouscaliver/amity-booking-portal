##main flask app :: Shahil kadia hii sundu
##Set-ExecutionPolicy Unrestricted -Scope Process;.\.venv\Scripts\activate;
##cd D:\projects\amity-booking-portal
from flask import *
from flask import request, jsonify
from flask import send_from_directory
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from time import ctime
import os
import random
import dbscript as db
import loginscript as login

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
app.secret_key =  "AMITY_792739"
app.config['SECRET_KEY'] = "AMITY_792739"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'amieventhub@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'ffoi rhgz arbn gnaw'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'amieventhub@gmail.com'  # Replace with your email
admin_email = 'amieventhub@gmail.com'  # Replace with the admin's email
mail = Mail(app)
server_link = "http://127.0.0.1:8000" #replace with production server initial routing address.

#task-related functions
def hallname(hallid:int):
    l = [0,"Auditorium Hall","Seminar Hall","Room No. 105, A2 Building","CRC Conference Room"]
    #l = [0,'auditorium','seminar','room105','crc']
    return (l[hallid])

def hallid(hallname:str):
    l = [0,'auditorium','seminar','room105','crc']
    return (l.index(hallname))

def trimtime(time:str):
    a = time.split(':')
    c = ""
    for i in a:
        c = c + i
    return int(c)

def maketime(time:int):
    if len(str(time))==3:
        time = "0"+str(time)
        time = time[:2]+":"+time[2:]
        return time
    else:
        time=str(time)
        time = time[:2]+":"+time[2:]
        return time

#db task functions
def get_sorted_status():
    out = db.all_status()
    accept = []
    pending = []
    reject = []
    final = []
    for i in out:
        if i[1] == 'pending':
            pending.append(i)
        elif i[1] == 'reject':
            reject.append(i)
        else:
            accept.append(i)
    final.append(pending)
    final.append(accept)
    final.append(reject)
    return final  #then use db.infofect for each bid.
    # print(accept,"\n",pending,"\n",reject)

# global code_list
code_list = []

def gen_code():
    # global code_list
    code = random.randint(101,199999)
    if code not in code_list:
        code_list.append(code)
    else:
        code = gen_code()
    return code

def send_mail(event_name,event_venue,event_date,start_time,end_time,school_name,hoi_name,resource_person_name,resource_person_details,faculty_phone,faculty_name,faculty_email,bid):
    email_body = f"""
    Dear Sir,

    I hope this message finds you well.

    I am writing to request your permission to conduct an event titled "{event_name}" at {event_venue} on {event_date} from {start_time} to {end_time}. Below are the details of the event:
    1. School Name: {school_name}
    2. Head of Institution/Director Name: {hoi_name}
    3. Resource Person Name: {resource_person_name}
    4. Resource Person Details: {resource_person_details}
    5. Phone Number of Faculty: {faculty_phone}

    We believe that this event will provide significant value and insights to our attendees, fostering an environment of learning and engagement.

    For your convenience, please click on the link below to visit AmiEventHUB and grant us permission to organize this event:

    [{server_link}/adminlogin]

    link<{server_link}/adminlogin>

    Best regards,
    {faculty_name}
    {school_name}
    {faculty_email}
    """
    
    html = f"""<pre>
    Dear Sir,

    I hope this message finds you well.

    I am writing to request your permission to conduct an event titled "{event_name}" at {event_venue} on {event_date} from {start_time} to {end_time}. Below are the details of the event:
    1. School Name: {school_name}
    2. Head of Institution/Director Name: {hoi_name}
    3. Resource Person Name: {resource_person_name}
    4. Resource Person Details: {resource_person_details}
    5. Phone Number of Faculty: {faculty_phone}
    6. Booking ID : {bid}

    We believe that this event will provide significant value and insights to our attendees, fostering an environment of learning and engagement.

    For your convenience, please click on the link below to visit AmiEventHUB and grant us permission to organize this event.

    Shortcut Links:

        Admin Page :  <a href='{server_link}/admin'>Login Link</a>
    
        Approve Request :    <a href='{server_link}/admin/email/approve/{bid}'>Approve</a>
    
        Reject Request :     <a href='{server_link}/admin/email/reject/{bid}'>Reject</a>
                    
    Best regards,
    {faculty_name}
    {school_name}
    {faculty_email}</pre>
    """
    # Send the email
    try:
        msg = Message(subject='Request for Permission to Conduct an Event', recipients=[admin_email])
        msg.body = email_body
        msg.html = html
        mail.send(msg)
        return True
    except Exception as e:
        print(e)
        return False

def send_mail2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status,user_email,bid):
    email_body = f"""
    Dear Faculty,

    I hope this message finds you well.

    The request for permission to conduct an event titled "{event_name}" at {event_venue} on {event_date} from {start_time} to {end_time}. Below are the details of the event:
    1. School Name: {school_name}
    2. Resource Person Name: {resource_person_name}
    3. Resource Person Details: {resource_person_details}
    

    Your Request has been {status} by the Admin. 

    Kindly check for more details in status section of AmiEventHub.For your convenience, please click on the link below to visit AmiEventHUB

    Shortcut Links:

        User Page :  <a href='{server_link}/user'>Login Link</a>

    Best regards,
    AmiEventHub
    """
    html = f"""<pre>
    Dear Faculty,

    I hope this message finds you well.

    The request for permission to conduct an event titled "{event_name}" at {event_venue} on {event_date} from {start_time} to {end_time}. Below are the details of the event:
    1. School Name: {school_name}
    2. Resource Person Name: {resource_person_name}
    3. Resource Person Details: {resource_person_details}
    4. Booking ID: {bid}
    

    Your Request has been {status} by the Admin. 

    Kindly check for more details in status section of AmiEventHub.For your convenience, please click on the link below to visit AmiEventHUB
    
    Shortcut Links:

        User Page :  <a href='{server_link}/user'>Login Link</a>

    Best regards,
    AmiEventHub</pre>"""
    # Send the email
    try:
        msg = Message(subject='Response to Event Permission', recipients=[user_email])
        msg.body = email_body
        msg.html = html
        mail.send(msg)
        return True
    except Exception as e:
        print(e)
        return False

def send_mail3(user_email,code):
    email_body = f"""
    Dear Faculty,

    I hope this message finds you well.

    Your Verification code for {user_email} is {code}.

    Best regards,
    AmiEventHub
    """

    # Send the email
    try:
        msg = Message(subject='Email Verification by AmiEventHub', recipients=[user_email])
        msg.body = email_body
        mail.send(msg)
        return True
    except Exception as e:
        print(e)
        return False

#context functions
@app.context_processor
def utility_processor():
    def make_time(time:int):
        if str(time)=="0":
            return "00:00"
        if len(str(time))==3:
            time = "0"+str(time)
            time = time[:2]+":"+time[2:]
            return time
        else:
            time=str(time)
            time = time[:2]+":"+time[2:]
            return time
    return dict(make_time=make_time)

#before-request functions
@app.before_request
def make_session_permanent():
    session.permanent = True

#routing functions
@app.route('/')
def home():
    #session['username'] = "TEST"
    return render_template("front.html")

@app.route('/alert')
def alert():
    #error="Your Request has been successfully sent!"
    error = send_mail('event_name','event_venue','event_date','start_time','end_time','school_name','hoi_name','resource_person_name','resource_person_details','faculty_phone','faculty_name','faculty_email',0)
    print(error)
    return render_template("test1.html",error=error)

@app.route('/index' ,methods=['GET', 'POST'])
def index():
    error = None
    if session:
        uname = session['username']
        print(uname)
        if request.method == 'POST':
            
            hall = ['auditorium','seminar','room105','crc']
            place = ['SchoolName','FacultyName','HodName','EventName','Date','sTime','eTime','Email','Phone','ResourcePersonName','ResourcePersonDetail']
            final=[]
            loc = ''
            for i in hall:
                for j in place:
                    try:
                        f = i+j
                        #print(f)
                        final.append(request.form[f])
                        loc = i
                    except KeyError as e:
                        print(e)
            final[5] = trimtime(final[5])
            final[6] = trimtime(final[6])
            hid = hallid(loc)
            
            #print(final)
            #print('location = ',hallid(loc))
            if db.check_hall(hid,final[4],final[5],final[6]):
                bid = db.request_hall(hid,final[0],final[4],final[5],final[6],final[3],uname)
                db.info_dump(bookid=bid, hallid=hid , school=final[0], fname=final[1], hod=final[2], email=final[7] , phone=final[8] , date=final[4] , stime=final[5] , etime=final[6] , event=final[3],rpname=final[9],rpdetail=final[10])
                #db.info_dump(bid, hid , sfinal[0], final[1], final[2],final[7] , final[8] , final[4] , final[5] , final[6] , final[3])
                if (send_mail(final[3],hallname(hid),final[4],final[5],final[6],final[0],final[2],final[9],final[10],final[8],final[1],final[7],bid)):
                    
                    error = "Your Request Is Successfully Sent for Approval!"
                    return render_template("index.html",error=error)
                else:
                    error=f"Email not sent to Admin due to server issue. But request is sent please send an email manually to {admin_email}."
                    return render_template("index.html",error=error)
            else:
                error = "Hall Not Available At given Date and Time."
                return render_template("index.html",error=error)
            
        return render_template("index.html",error=error)
    else:
        return redirect(url_for('userlogin'))

@app.route('/requeststatus' ,methods=['GET', 'POST'])
def status():
    if session['username']:
        username = session['username']
        output = db.check_request(username)
        return render_template("statuspage.html",output=output)
    else:
        return redirect(url_for('userlogin'))
        
@app.route('/admin' ,methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        bid = request.form["bookingId"]
        status = request.form["confirmEvent"]
        event_name = request.form["eventName"]
        event_venue = request.form["venue"]
        event_date = request.form["eventDate"]
        start_time = request.form["startTime"]
        end_time = request.form["endTime"]
        school_name = request.form["schoolName"]
        resource_person_name = request.form["resourcePersonName"]
        resource_person_details = request.form["resourcePersonDetail"]
        facultyEmail = request.form["facultyEmail"]
        print(bid , status)
        if status=="ACCEPT":
            try:
                db.confirm_hall(bid)
                status2 = "ACCEPTED"
                send_mail2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bid)
                return redirect(url_for('admin'))
            except:
                return redirect(url_for('admin'))
        elif status=="REJECT":
            try:
                db.reject_hall(bid)
                status2 = "REJECTED"
                send_mail2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bid)
                return redirect(url_for('admin'))
            except:
                return redirect(url_for('admin'))
    try:
        if session['admin_username']:
            username = session['admin_username']
            if (username.split("+")[0]=='ADMIN'):
                #print("ACCEPTED")
                output1 = db.check_pending()
                #print(output1)
                output = []
                for i in output1:
                    output2 = db.info_fetch(i[0])
                    #output2[0][1] = hallname(output2[0][1])
                    output.append(output2)
                #print(output)
                
                
                return render_template("admintable.html",output=output)
            else:
                return redirect(url_for('adminlogin'))
        else:
            return redirect(url_for('adminlogin'))
        
        
            
        return redirect(url_for('adminlogin'))
    except:
        return redirect(url_for('adminlogin'))

@app.route('/login' ,methods=['GET', 'POST'])
def userlogin():
    error = None
    session.pop('username',None)
    if request.method == 'POST':
        username = request.form["user-username"]
        passwd = request.form["user-password"]
        #print(username,passwd)
        if login.load_user(username,passwd) == True:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            if login.load_user(username,passwd) == "verify":
                email = login.getname_user(username)
                #send_mail3(email,gen_code())
                return redirect(url_for('userlogin'))
            else:
                error = "Incorrect Credentials!"
                return render_template('loginuser.html',error=error)
    return render_template('loginuser.html',error=error)

@app.route('/signup' ,methods=['GET', 'POST'])
def usersignup():
    alert = None
    session.pop('username',None)
    if request.method == 'POST':
        username = request.form["user-username"]
        passwd = request.form["user-password"]
        email = request.form["user-email"]
        
        if (email.split("@")[-1]!="mum.amity.edu"):
            alert = 'Please use a valid @mum.amity.edu email address for signup.'
            return render_template('signup.user.html',error=alert)
        else:
            #return redirect(url_for('verifyemail',username=username,password=passwd))
            if login.create_user(username=username,password=passwd,name=email):
                print(username,passwd,email)
                #send_mail3(email,gen_code())
                #return redirect(url_for('verifyemail',username=username))
                return redirect(url_for('userlogin',username=username))
            else:
                alert = 'Account creation failed. Select different username and Please try again later.'
                return render_template('signup.user.html',error=alert)
        
    return render_template('signup.user.html',error=alert)

@app.route('/adminlogin' ,methods=['GET', 'POST'])
def adminlogin():
    error = None
    session.pop('admin_username',None)
    if request.method == 'POST':
        username = request.form["admin-username"]
        passwd = request.form["admin-password"]
        #print(username,passwd)
        if login.load_admin(username,passwd):
            adname = "ADMIN+"+username
            session['admin_username'] = adname
            return redirect(url_for('admin'))
        else:
            error = "Incorrect Credentials!"
            return render_template('loginadmin.html',error=error)
    return render_template('loginadmin.html',error=error)

@app.route('/adminsignup' ,methods=['GET', 'POST'])
def adminsignup():
    alert = None
    session.pop('admin_username',None)
    if request.method == 'POST':
        username = request.form["admin-username"]
        passwd = request.form["admin-password"]
        email = request.form["admin-email"]
        
        if (email.split("@")[-1]!="mum.amity.edu"):
            alert = 'Please use a valid @mum.amity.edu email address for signup.'
            return render_template('signup.admin.html',error=alert)
        else:
            #return redirect(url_for('verifyemail',username=username,password=passwd))
            if login.create_admin(username=username,password=passwd,name=email):
                print(username,passwd,email)
                return redirect(url_for('adminlogin'))
            else:
                alert = 'Account creation failed. Select different username and Please try again later.'
                return render_template('signup.admin.html',error=alert)
        
    return render_template('signup.admin.html',error=alert)

#email get requests (admin):

@app.route('/admin/email/approve/<bookid>')
def admingetapprove(bookid):
    bookid = int(bookid)
    if db.confirm_hall(bookid):
        error=f"Booking Number: {bookid}. Request APPROVED successfully."
        return render_template('closetab.html',error=error)
    else:
        error=f"Booking Number: {bookid}. Request to server Failed. Please Contact Technical Team if Problem Presists"
        return render_template('closetab.html',error=error)

@app.route('/admin/email/reject/<bookid>')
def admingetreject(bookid):
    bookid = int(bookid)
    if db.reject_hall(bookid):
        error=f"Booking Number: {bookid}. Request DISAPPROVED successfully."
        return render_template('closetab.html',error=error)
    else:
        error=f"Booking Number: {bookid}. Request to server Failed. Please Contact Technical Team if Problem Presists"
        return render_template('closetab.html',error=error)

#future
@app.route('/verifyemail/<username>' ,methods=['GET', 'POST'])
def verifyemail(username):
    # global code_list
    alert = None
    email = login.getname_user(username)
    if request.method == 'POST':
        code = request.form["verification-code"]
        print(code_list)
        print(code)
        print(username)
        if (int(code) in code_list):
            #alert = 'Please use a valid @mum.amity.edu email address for signup.'
            print(code)    
            state = login.verifyemail(username)
            print(state)

            if state == True :
                return redirect(url_for('userlogin'))
            else:
                alert = "Incorrect server response entered please try again."
                print(code)
                print(code_list)
                return render_template('verifyemail.html',error=alert,email=email)
        else:
            alert = "Incorrect code entered please try again."
            print(code)
            print(code_list)
            return render_template('verifyemail.html',error=alert,email=email)
    else:
        return render_template('verifyemail.html',error=alert,email=email)
        
    return render_template('verifyemail.html',error=alert,email=email)


#main runtime
if __name__ == '__main__':
    app.run(debug=True,port=8000)
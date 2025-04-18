##main flask app :: Shahil kadia 
#Set-ExecutionPolicy Unrestricted CurrentUser;.\.venue\Scripts\activate;
# Description: This file contains the main code for the Ami-Scheduler application.# -*- coding: utf-8 -*-
import os
import random
from datetime import date as dt
from datetime import datetime
from datetime import timedelta
import threading
from flask import *
from flask import jsonify, request, send_from_directory
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from logging.config import dictConfig
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
app.config['MAIL_PASSWORD'] = 'axey unjy zyzj cfdw'  # Replace with your email password
#app.config['MAIL_PASSWORD'] = 'ffoi rhgz arbn gnaw'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'amieventhub@gmail.com'  # Replace with your email
admin_email = 'amieventhub@gmail.com'  # Replace with the admin's email
it_email = 'itamitymumbai@gmail.com'  # Replace with the admin's email
admin2_mail = 'amitydirector01@gmail.com' # Replace with the admin2's email
mail = Mail(app)
server_link = "http://amischeduler.aum.amity.edu.in" #replace with production server initial routing address.
#server_link = "http://127.0.0.1:8000" #replace with production server initial routing address.
#server_link = "http://10.5.2.29" #replace with production server initial routing address.
#server_link = "https://786gkd71-8000.inc1.devtunnels.ms/" #replace with production server initial routing address.

vcmail = ['vcaum@mum.amity.edu']
dirmails = ['diradmin1@mum.amity.edu' , 'diradmin@mum.amity.edu']
itmails = ['acghatge@it.amity.edu', 'itmum@amity.edu']
vcofficemails = ['vcoffice@mum.amity.edu']
comb1 = vcmail + dirmails + itmails + vcofficemails #upon confirmed rejection


#vcmail = ['amieventhub@gmail.com']
#dirmails = ['amitydirector01@gmail.com' , 'amitydirector01@gmail.com']
#itmails = ['itamitymumbai@gmail.com', 'itamitymumbai@gmail.com']
#vcofficemails = ['amieventhub@gmail.com']
#comb1 = vcmail + dirmails + itmails + vcofficemails #upon confirmed rejection

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(process)d] [%(levelname)s] in %(module)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S %z"
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "DEBUG", "handlers": ["wsgi"]},
    }
)

app.logger.info("STARTING APPLICATION AND LOGGING...")

#task-related functions
def hallname(hallid:int):
    l = [0,"Auditorium Hall","Seminar Hall","Room No. 105, A2 Building","CRC Conference Room","Seminar VIP Hall","RICS Conference Room","Atrium","VVIP Room","AIB Room 206","ABS Room 304","AIBAS Room 504","ASET Room 123","ALS Room 602"]
    #l = [0,'auditorium','seminar','room105','crc']
    return (l[hallid])

def hallid(hallname:str):
    l = [0,'auditorium','seminar','room105','crc','Seminarvip','RICSConferenceRoom','Atrium','VVIP','AIB206','ABS304','AIBAS504','ASET123','ALS602']
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
    # app.logger.info(final2)
    return final2[::-1]  #reverse the order for latest first

# cookie-username-function
def getusername():
    userdict = {'ASET':'ASET - Amity School of Engineering and Technology',
                'ABS':'ABS - Amity Business School',
                'AFS':'AFS - Amity Film School',
                'AIBAS':'AIBAS - Amity Institute of Behavioural & Allied Sciences',
                'AIB':'AIB - Amity Institute of Biotechnology',
                'AIIT':'AIIT - Amity Institute of Information Technology',
                'AILA':'AILA - Amity Institute of Liberal Arts',
                'AIP':'AIP - Amity Institute of Pharmacy',
                'AIT':'AIT - Amity Institute of Technology',
                'AITT':'AITT - Amity Institute of Travel & Tourism',
                'ALS':'ALS - Amity Law School',
                'ASAP':'ASAP - Amity School of Architecture & Planning',
                'ASAS':'ASAS - Amity School of Applied Sciences',
                'ASCO':'ASCO - Amity School of Communication',
                'ASFT':'ASFT - Amity School of Fashion Technolog',
                'ASL':'ASL - Amity School of Languages',
                'CIIOL':'CIIOL - CII Logistics',
                'TUCSSBERICS':'RICS',
                'ASFA':'ASFA - Amity School of Fine Arts',
                'AIE':'AIE - Amity Institute of Education',
                'AIN':'AIN - Amity Institute of Nanotechnology',
                'Administrator':'Administrator',
                'Director_Admin_1':'Director Admin 1',
                'Director_Admin_2':'Director Admin 2',
                'CRC_Dept':'CRC Department',
                'HR_Dept':'HR Department',
                'Hostel_Security_Dept':'Hostel Security Department',
                'Admissions_Dept':'Admissions Department',
                'Examinations_Dept':'Examinations Department',
                'testdebug':'testdebug',
                'IT_Dept':'IT Department',
                'Registrar' : 'Registrar',
		'Accounts' : 'Accounts',
                'Accounts_Dept' : 'Accounts Department',
                }
    cook = session['username']
    if cook == "Director_Admin_1": schoolname = "Director_Admin_1"
    elif cook == "Director_Admin_2": schoolname = "Director_Admin_2"
    elif cook == "CRC_Dept": schoolname = "CRC_Dept"
    elif cook == "HR_Dept": schoolname = "HR_Dept"
    elif cook == "Hostel_Security_Dept": schoolname = "Hostel_Security_Dept"
    elif cook == "Admissions_Dept": schoolname = "Admissions_Dept"
    elif cook == "Examinations_Dept": schoolname = "Examinations_Dept"
    elif cook == "IT_dept": schoolname = "IT_Dept"
    elif cook == "Accounts": schoolname = "Accounts"
    elif cook == "Accounts_Dept": schoolname = "Accounts_Dept"
    else:
        schoolname = cook.split("_")[0]
    fullname = userdict[schoolname]
    # print(fullname)
    return fullname
    pass

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

    For your convenience, please click on the link below to visit Ami-Scheduler and grant us permission to organize this event.

    Shortcut Links:

        Admin Page :  <a href='{server_link}/admin'>Login Link</a>
    
        Approve Request :    <a href='{server_link}/admin/email/approve/{bid}'>Approve</a>
    
        Reject Request :     <a href='{server_link}/admin/email/reject/{bid}'>Reject</a>
                    
    Best regards,
    {faculty_name}
    {school_name}
    {faculty_email}
    
    [This mail is computer generated by Ami-Scheduler.]</pre>
    """
    # Send the email
    try:
        msg = Message(subject=f'Request for Permission to Conduct an Event: {event_name} at {event_date}', recipients=vcmail)
        # msg.body = email_body
        msg.html = html
        @copy_current_request_context
        def send_message(message):
            mail.send(message)
        sender = threading.Thread(name='mail_sender1', target=send_message, args=(msg,))
        sender.start()
        # mail.send(msg)
        return True
    except Exception as e:
        app.logger.info(e)
        app.logger.error(e)
        return False

#email to user response to event
def send_mail2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status,user_email,bid):
    
    html = f"""<pre>
    Dear Faculty,

    I hope this message finds you well.

    The request for permission to conduct an event titled "{event_name}" at {event_venue} on {event_date} from {start_time} to {end_time}. Below are the details of the event:
    • School Name: {school_name}
    • Resource Person Name: {resource_person_name}
    • Resource Person Details: {resource_person_details}
    • Email of Event Coordinator: {user_email}
    • Booking ID : {bid}
    • Event Venue: {event_venue}
    • Event Date: {event_date}
    • Duration: {start_time} to {end_time}
    

    Your Request has been {status} by the Admin. 

    Kindly check for more details in status section of Ami-Scheduler.For your convenience, please click on the link below to visit Ami-Scheduler
    
    Shortcut Links:

        User Page :  <a href='{server_link}/user'>Login Link</a>

    Best regards,
    Ami-Scheduler
    
    [This mail is computer generated by Ami-Scheduler.]</pre>"""
    # Send the email
    try:
        msg = Message(subject=f'Response to Event: {event_name} Permission at {event_date}', recipients=[user_email])
        # msg.body = email_body
        msg.html = html
        @copy_current_request_context
        def send_message(message):
            mail.send(message)
        sender = threading.Thread(name='mail_sender2', target=send_message, args=(msg,))
        sender.start()
        # mail.send(msg)
        return True
    except Exception as e:
        app.logger.info(e)
        app.logger.error(e)
        return False

#cc mails after confirmation

#adminstration mail
def send_mail4(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status,user_email,bid):
    
    html = f"""<pre>
    Dear Administrative Department,

    I hope this message finds you well.

    The request for permission to conduct an event titled "{event_name}" at {event_venue} on {event_date} from {start_time} to {end_time}. Below are the details of the event:
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
            <td>{start_time}</td>
            <td>    </td>
            <td>{end_time}</td>
            <td>    </td>
            <td>{status}</td>
            <td>    </td>
            
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
    • Duration: {start_time} to {end_time}
    
    This Event Request has been Approved by Hon. Vice-Chancellor Sir and this is a confirmation email.  Kindly manage and coordinate the event. Your timely assistance and support in making the event a success are greatly appreciated.

    Kindly check for more details in Ami-Scheduler.For your convenience, please click on the link below to visit Ami-Scheduler
    
    Shortcut Links:

        Login Page :  <a href='{server_link}'>Login Link</a>

    Best regards,
    Ami-Scheduler
    
    [This mail is computer generated by Ami-Scheduler.]</pre>"""
    # Send the email
    try:
        msg = Message(subject=f'New Event: {event_name} dated {event_date}', recipients=dirmails)
        # msg.body = email_body
        msg.html = html
        @copy_current_request_context
        def send_message(message):
            mail.send(message)
        sender = threading.Thread(name='mail_sender4', target=send_message, args=(msg,))
        sender.start()
        # mail.send(msg)
        return True
    except Exception as e:
        app.logger.info(e)
        app.logger.error(e)
        return False

#itmails
def send_mail4v2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status,user_email,bid):
    
    html = f"""<pre>
    Dear IT Department,

    I hope this message finds you well.

    The request for permission to conduct an event titled "{event_name}" at {event_venue} on {event_date} from {start_time} to {end_time}. Below are the details of the event:
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
            <td>{start_time}</td>
            <td>    </td>
            <td>{end_time}</td>
            <td>    </td>
            <td>{status}</td>
            <td>    </td>
            
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
    • Duration: {start_time} to {end_time}
    
    This Event Request has been Approved by Hon. Vice-Chancellor Sir and this is a confirmation email.  Kindly help with IT Services and audio system services. Your timely assistance and support in making the event a success are greatly appreciated.

    Kindly check for more details in Ami-Scheduler.For your convenience, please click on the link below to visit Ami-Scheduler
    
    Shortcut Links:

        Login Page :  <a href='{server_link}'>Login Link</a>

    Best regards,
    Ami-Scheduler
    
    [This mail is computer generated by Ami-Scheduler.]</pre>"""
    # Send the email
    try:
        msg = Message(subject=f'New Event: {event_name} dated {event_date}', recipients=itmails)
        # msg.body = email_body
        msg.html = html
        @copy_current_request_context
        def send_message(message):
            mail.send(message)
        sender = threading.Thread(name='mail_sender4', target=send_message, args=(msg,))
        sender.start()
        # mail.send(msg)
        return True
    except Exception as e:
        app.logger.info(e)
        app.logger.error(e)
        return False

#vcoffice mail
def send_mail4v3(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status,user_email,bid):
    
    html = f"""<pre>
    Respected VC Office,

    Greetings of the Day!!!

    The request for permission to conduct an event titled "{event_name}" at {event_venue} on {event_date} from {start_time} to {end_time}. Below are the details of the event:
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
            <td>{start_time}</td>
            <td>    </td>
            <td>{end_time}</td>
            <td>    </td>
            <td>{status}</td>
            <td>    </td>
            
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
    • Duration: {start_time} to {end_time}
    
    This Event Request has been Approved by Hon. Vice-Chancellor Sir and this is a confirmation email.

    Kindly check for more details in Ami-Scheduler.For your convenience, please click on the link below to visit Ami-Scheduler
    
    Shortcut Links:

        Login Page :  <a href='{server_link}'>Login Link</a>

    Best regards,
    Ami-Scheduler
    
    [This mail is computer generated by Ami-Scheduler.]</pre>"""
    # Send the email
    try:
        msg = Message(subject=f'New Event: {event_name} dated {event_date}', recipients=vcofficemails)
        # msg.body = email_body
        msg.html = html
        @copy_current_request_context
        def send_message(message):
            mail.send(message)
        sender = threading.Thread(name='mail_sender4', target=send_message, args=(msg,))
        sender.start()
        # mail.send(msg)
        return True
    except Exception as e:
        app.logger.info(e)
        app.logger.error(e)
        return False

#cancellatoin email to emaillist
def send_mail5(event_name,event_venue,event_date,start_time,end_time,school_name,status,bid,emaillist):
    
    html = f"""<pre>
    Respected Department,

    I hope this message finds you well.

    The request for permission to conduct an event titled "{event_name}" at {event_venue} on {event_date} from {start_time} to {end_time}. Below are the details of the event:
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
            <td>{start_time}</td>
            <td>    </td>
            <td>{end_time}</td>
            <td>    </td>
            <td>CANCELLED</td>
            <td>    </td>
            
        </tr>
    </table>
    </form>
    The Request has been CANCELLED by the USER.

    • School Name: {school_name}
    • Booking ID : {bid}
    • Event Venue: {event_venue}
    • Event Date: {event_date}
    • Duration: {start_time} to {end_time}


    Kindly check for more details in Ami-Scheduler.For your convenience, please click on the link below to visit Ami-Scheduler
    
    Shortcut Links:

        Login Page :  <a href='{server_link}'>Login Link</a>

    Best regards,
    Ami-Scheduler
    
    [This mail is computer generated by Ami-Scheduler.]</pre>"""
    # Send the email
    try:
        msg = Message(subject=f'Cancel Event: {event_name} dated {event_date}', recipients=emaillist)
        # msg.body = email_body
        msg.html = html
        @copy_current_request_context
        def send_message(message):
            mail.send(message)
        sender = threading.Thread(name='mail_sender5', target=send_message, args=(msg,))
        sender.start()
        # mail.send(msg)
        return True
    except Exception as e:
        app.logger.info(e)
        app.logger.error(e)
        return False

#email-verification mail(experimental)  
def send_mail3(user_email,code):
    html = f"""
    <pre>
    Dear Faculty,

    I hope this message finds you well.

    Your Verification code for {user_email} is {code}.

    Best regards,
    Ami-Scheduler

    [This mail is computer generated by Ami-Scheduler.]
    </pre>
    """

    # Send the email
    try:
        msg = Message(subject='Email Verification by Ami-Scheduler', recipients=[user_email])
        # msg.body = email_body
        msg.html = html
        @copy_current_request_context
        def send_message(message):
            mail.send(message)
        sender = threading.Thread(name='mail_sender3', target=send_message, args=(msg,))
        sender.start()
        # mail.send(msg)
        return True
    except Exception as e:
        app.logger.info(e)
        app.logger.error(e)
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
        l = [0,"Auditorium Hall","Seminar Hall","Room No. 105, A2 Building","CRC Conference Room","Seminar VIP Hall","RICS Conference Room","Atrium","VVIP Room","AIB Room 206","ABS Room 304","AIBAS Room 504","ASET Room 123","ALS Room 602"]
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

@app.route('/checkconn',methods=['GET'])
def reconnect():
    a = db.checkconn()
    return a

@app.route('/reconn',methods=['GET'])
def reconnect2():
    a = db.reconnect()
    return a

@app.route('/alert')
def alert():
    #error="Your Request has been successfully sent!"
    error = send_mail('event_name','event_venue','event_date','900','1100','school_name','hoi_name','resource_person_name','resource_person_details','faculty_phone','faculty_name','faculty_email',0)
    app.logger.info(error)
    return render_template("test1.html",error=error)

@app.route('/user' ,methods=['GET', 'POST'])
def index():
    error = None
    try:
        if session:
            uname = session['username']
            app.logger.info(uname)
            cal = db.calender()
            app.logger.info(f"CAL: {cal}")
            output = db.calendermain()
            scname = getusername()
            app.logger.info(scname)
            app.logger.info(output)
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
            
            if request.method == 'POST':
                
                hall = ['auditorium','seminar','room105','crc','Seminarvip','RICSConferenceRoom','Atrium','VVIP','AIB206','ABS304','AIBAS504','ASET123','ALS602']
                place = ['SchoolName','FacultyName','HodName','EventName','date','startime','endtime','Email','Phone','ResourcePersonName','ResourcePersonDetail']
                final=[]
                loc = ''
                for i in hall:
                    for j in place:
                        try:
                            f = i+j
                            #app.logger.info(f)
                            final.append(request.form[f])
                            loc = i
                        except KeyError as e:
                            app.logger.info(e)
                            app.logger.error(e)
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
                # app.logger.info(final)
                #app.logger.info('location = ',hallid(loc))
                app.logger.info(f'index FINAL  = {final}')
                app.logger.info(f'location = {hallid(loc)}')
                app.logger.info(f'CHECK : location = {hallid(loc)} , date = {final[4]} ,final[6] = {final[6]} and final[5] = {final[5]}')
                app.logger.info(f'function details : {hid},{final[4]},{final[5]},{final[6]}')
                if db.check_hall(hid,final[4],final[5],final[6]):
                    
                    year = final[4][:4]
                    month = final[4][5:7]
                    day = final[4][8:]
                    today = dt.today()
                    # today = datetime.date.today() && and given>=today
                    given = dt(int(year),int(month),int(day))
                    app.logger.info(f'today {today} and given {given}')
                    app.logger.info(f'final[6] {final[6]} and final[5] {final[5]}')
                    if int(final[6]) > int(final[5]) and given>=today:
                        app.logger.info("PASS")
                        # pass
                        
                        bid = db.request_hall(hid,final[0],final[4],final[5],final[6],final[3],uname)
                        db.info_dump(bookid=bid, hallid=hid , school=final[0], fname=final[1], hod=final[2], email=final[7] , phone=final[8] , date=final[4] , stime=final[5] , etime=final[6] , event=final[3],rpname=final[9],rpdetail=final[10])
                        #db.info_dump(bid, hid , sfinal[0], final[1], final[2],final[7] , final[8] , final[4] , final[5] , final[6] , final[3])
                        if (send_mail(final[3],hallname(hid),final[4],final[5],final[6],final[0],final[2],final[9],final[10],final[8],final[1],final[7],bid)):
                            
                            error = "Your Request Is Successfully Sent for Approval!"
                            return render_template("index.html",error=error,cal=cal,output=output,scname=scname)
                        else:
                            error=f"Email not sent to Admin due to server issue. But request is sent please send an email manually to {admin_email}."
                            return render_template("index.html",error=error,cal=cal,output=output,scname=scname)
                    else:
                        error = "The Time or Date Entered Is Incorrect. Please Enter Correct Time and Date."
                        return render_template("index.html",error=error,cal=cal,output=output,scname=scname)
                else:
                    error = "Hall Not Available At given Date and Time."
                    return render_template("index.html",error=error,cal=cal,output=output,scname=scname)
            
            return render_template("index.html",error=error,cal=cal,output=output,scname=scname)
        else:
            return redirect(url_for('userlogin'))
    except Exception as e:
        import traceback
        print(f"ERROR OCCURED HERE : {traceback.format_exc()}")
        app.logger.info(e)
        app.logger.error(e)
        app.logger.exception(f"ERROR OCCURED HERE : {e}")
        return redirect(url_for('userlogin'))

@app.route('/requeststatus' ,methods=['GET', 'POST'])
def status():
    if request.method == 'POST':
        try:
            if session['username']:
                username = session['username']
                app.logger.info("METHOD ACTIVATE")
                bid = request.form["booking_id"]
                status = request.form["status"]
                event_venue = request.form["hall_name"]
                event_date = request.form['date']
                start_time = request.form['start_time']
                end_time = request.form['end_time']
                event_name = request.form['ename']
                school_name = request.form['sname']
                app.logger.info(f'{bid},{status}')
                o = db.info_fetch(bid)
                email = o[0][9]
                app.logger.info(email)
                if db.reject_app(bid=int(bid),status=status):
                    #status = Pending / Confirmed
                    if status == "Pending":
                        error = "Venue hall request Cancelled Successfully."
                        comb = vcmail + [email]
                        send_mail5(event_name,event_venue,event_date,start_time,end_time,school_name,status,bid,comb)
                        output = db.check_request(username)
                        return render_template("statuspage.html",output=output,error=error)
                    else:
                        error = "Venue hall request Cancelled Successfully."
                        send_mail5(event_name,event_venue,event_date,start_time,end_time,school_name,status,bid,comb1)
                        output = db.check_request(username)
                        return render_template("statuspage.html",output=output,error=error)
                else:
                    error = "Error : Venue hall request NOT Cancelled. Please retry again."
                    output = db.check_request(username)
                    return render_template("statuspage.html",output=output,error=error)
            else:
                return redirect(url_for('userlogin'))
        except Exception as e:
            app.logger.info(e)
            app.logger.error(e)
            error = "Request in Process. Please wait and reload page if not reflected."
            output = db.check_request(username)
            return render_template("statuspage.html",output=output,error=error)
    try:
        if session['username']:
            username = session['username']
            output = db.check_request(username)
            # app.logger.info(output)
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
    except Exception as e:
        app.logger.error(e)
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
        # app.logger.info(bid , status)
        if status=="ACCEPT":
            try:
                if(db.confirm_hall(bid)): #db.confirm_hall(bid)
                    status2 = "ACCEPTED"
                    send_mail2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bid)
                    send_mail4(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bid)
                    send_mail4v2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bid)
                    send_mail4v3(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bid) 

                    return redirect(url_for('admin'))
                else:
                    app.logger.info("Error in Confirming Hall email.")
                    return render_template('notitab5.html',error="Error in Confirming Hall. Please try again.")
            except Exception as e:
                app.logger.info(e)
                app.logger.error(e)
                return redirect(url_for('admin'))
        elif status=="REJECT":
            try:
                if(db.reject_hall(bid)): #db.reject_hall(bid)
                    status2 = "REJECTED"
                    send_mail2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bid)
                    return redirect(url_for('admin'))
                else:
                    app.logger.info("Error in Confirming Hall email.")
                    return render_template('notitab5.html',error="Error in Rejecting Hall. Please try again.")
            except Exception as e:
                app.logger.info(e)
                app.logger.error(e)
                return redirect(url_for('admin'))
    try:
        if session['admin_username']:
            username = session['admin_username']
            if (username.split("+")[0]=='ADMIN'):
                # app.logger.info("ACCEPTEd")
                output1 = db.check_pending()
                # app.logger.info(output1)
                output = []
                for i in output1:
                    output2 = db.info_fetch(i[0])
                    #output2[0][1] = hallname(output2[0][1])
                    output.append(output2)
                final = []
                for i in output:
                    j = list(i[0])
                    final.append(j)
                # app.logger.info(final)
                # app.logger.info(len(output[0]))
                for j in final:
                    i = j
                    # app.logger.info("i value = ",i)
                    # app.logger.info('i8 = ',i[8])
                    # if i[8]==1300 or i[8]=="1300":
                    #     # app.logger.info('trigg')
                    #     i[8] = "1st Half"
                    # elif i[8]==1700 or i[8]=="1700":
                    #     i[8]= "2nd Half"
                    # elif i[8]==1701 or i[8]=="1701":
                    #     i[8]= "Full Day"
                # app.logger.info(final)
                return render_template("admintable.html",output=final)
            else:
                return redirect(url_for('adminlogin'))
        else:
            return redirect(url_for('adminlogin'))
 
        return redirect(url_for('adminlogin'))
    except Exception as e:
        app.logger.info(e)
        app.logger.error(e)
        return redirect(url_for('adminlogin'))

@app.route('/login' ,methods=['GET', 'POST'])
def userlogin():
    error = None
    session.pop('username',None)
    if request.method == 'POST':
        username = request.form["user-username"]
        passwd = request.form["user-password"]
        #app.logger.info(username,passwd)
        if login.load_user(username,passwd) == True:
            session['username'] = username
            app.logger.info(f"USER :: {username} :: {passwd}")
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
                app.logger.info(username,passwd,email)
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
        #app.logger.info(username,passwd)
        if login.load_admin(username,passwd):
            adname = "ADMIN+"+username
            session['admin_username'] = adname
            app.logger.info(f"ADMIN :: {username} :: {passwd}")
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
                app.logger.info(username,passwd,email)
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
            app.logger.info(output)
            return render_template('allbooking.html',output=output)
        except Exception as e :
            app.logger.info(e)
            app.logger.error(e)
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
        start_time = maketime(o[0][7])
        end_time = maketime(o[0][8])
        school_name = o[0][2]
        resource_person_name = o[0][11]
        resource_person_details = o[0][12]
        facultyEmail = o[0][9]
        status2 = "ACCEPTED"
        send_mail2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bookid)
        send_mail4(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bookid)
        send_mail4v2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bookid)
        send_mail4v3(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bookid)

        error=f"Booking Number: {bookid}. Request APPROVED successfully."
        return render_template('closetab.html',error=error)
    else:
        error=f"Booking Number: {bookid}. Request to server Failed (The Request might have been already alotted, kindly chech again). Please Contact Technical Team if Problem Presists"
        return render_template('closetab.html',error=error)

@app.route('/admin/email/reject/<bookid>',methods=['GET'])
def admingetreject(bookid):
    bookid = int(bookid)
    if db.reject_hall(bookid):
        o = db.info_fetch(bookid)
        event_name = o[0][5]
        event_venue = hallname(int(o[0][1]))
        event_date = o[0][6]
        start_time = maketime(o[0][7])
        end_time = maketime(o[0][8])
        school_name = o[0][2]
        resource_person_name = o[0][11]
        resource_person_details = o[0][12]
        facultyEmail = o[0][9]
        status2 = "REJECTED"
        send_mail2(event_name,event_venue,event_date,start_time,end_time,school_name,resource_person_name,resource_person_details,status2,facultyEmail,bookid)
        error=f"Booking Number: {bookid}. Request DISAPPROVED successfully."
        return render_template('closetab.html',error=error)
    else:
        error=f"Booking Number: {bookid}. Request to server Failed (The Request might have been already alotted, kindly chech again). Please Contact Technical Team if Problem Presists"
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
    # app.logger.info(output)
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
    # app.logger.info(output)
    return render_template('calenderadmin.html',output=output)

@app.route('/server/periodic',methods=['GET'])
def periodic():
    a = db.seeall()
    b = login.seeall()
    return jsonify(a,b)
    
@app.route('/creators',methods=['GET', 'POST'])
def creators():
    return jsonify({'created by':'Shahil Kadia & Sundaram Singh','Year':'2024','Sem & Branch':'sem - 5(summer internship) & B.TECH(CSE)','College':'Amity University Mumbai','contact':'8128455494 & 8976413161','email':'shahilkadia@gmail.com'})

@app.route('/user/calender',methods=['GET'])
def usercalender():
    output = db.calendermain()
    app.logger.info(output)
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
    # app.logger.info(output)
    return render_template('calenderuser.html',output=output,server_link=server_link)

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
        return jsonify((mdata))
    elif us == "ab791314981c430b2b34c0aa36b43ac7":
        session['debug'] = "TRUE"
        if request.method == 'POST':
            dbname = request.form["database"]
            cmd = request.form["command"]
            typeo = request.form["type"]
            # app.logger.info(dbname,cmd)
            if typeo == "output":
                if dbname == "maindb":
                    output = db.cmd(cmd)
                    # output = json.dumps(output, indent=4)
                    pass      
                elif dbname == "shell":
                    if cmd.split('_')[0] == "system":
                        os.system(cmd.split('_')[1])
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
                    return f"EXCEPTION :: JSON :: {e} <br><br><br>{output}"
            else:pass
        else:
            return render_template('debugger.html')
        
    else:
        return "<h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.<p>"
    

@app.route('/calender/form/<hallname2>/<date>/<startTime>/<endTime>/<day>',methods=['GET','POST'])
def calenderform(hallname2,date,startTime,endTime,day):
    error = None
    try:
    # if True:
        if session:
            uname = session['username']
            app.logger.info(uname)
            cal = db.calender()
            app.logger.info(f"CAL: {cal}")
            output = db.calendermain()
            scname = getusername()
            app.logger.info(scname)
            # app.logger.info(output)
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
            
            if request.method == 'POST':
                
                hall = ['auditorium','seminar','room105','crc','Seminarvip','RICSConferenceRoom','Atrium','VVIP','AIB206','ABS304','AIBAS504','ASET123','ALS602']
                place = ['SchoolName','FacultyName','HodName','EventName','date','startime','endtime','Email','Phone','ResourcePersonName','ResourcePersonDetail']
                final=[]
                loc = ''
                for i in hall:
                    for j in place:
                        try:
                            f = i+j
                            #app.logger.info(f)
                            final.append(request.form[f])
                            loc = i
                        except KeyError as e:
                            app.logger.info(e)
                            app.logger.error(e)
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
                
                app.logger.info(f'FINAL  = {final}')
                app.logger.info(f'location = {hallid(loc)}')
                app.logger.info(f'CHECK : location = {hallid(loc)} , date = {final[4]} ,final[6] = {final[6]} and final[5] = {final[5]}')
                app.logger.info(f'function details : {hid},{final[4]},{final[5]},{final[6]}')
                if db.check_hall(hid,final[4],final[5],final[6]):
                    year = final[4][:4]
                    month = final[4][5:7]
                    day = final[4][8:]
                    today = dt.today()
                    # today = datetime.date.today() && and given>=today
                    given = dt(int(year),int(month),int(day))
                    app.logger.info(f'today {today} and given {given}')
                    app.logger.info(f'final[6] {final[6]} and final[5] {final[5]}')
                    if int(final[6]) > int(final[5]) and given>=today:
                        app.logger.info("PASS")
                        bid = db.request_hall(hid,final[0],final[4],final[5],final[6],final[3],uname)
                        db.info_dump(bookid=bid, hallid=hid , school=final[0], fname=final[1], hod=final[2], email=final[7] , phone=final[8] , date=final[4] , stime=final[5] , etime=final[6] , event=final[3],rpname=final[9],rpdetail=final[10])
                        #db.info_dump(bid, hid , sfinal[0], final[1], final[2],final[7] , final[8] , final[4] , final[5] , final[6] , final[3])
                        if (send_mail(final[3],hallname(hid),final[4],final[5],final[6],final[0],final[2],final[9],final[10],final[8],final[1],final[7],bid)):
                            
                            error = "Your Request Is Successfully Sent for Approval!"
                            # return redirect(url_for("index",error=error,cal=cal,output=output))
                            return render_template("notitab2.html",error=error)
                        else:
                            error=f"Email not sent to Admin due to server issue. But request is sent please send an email manually to {admin_email}."
                            # return redirect(url_for("index",error=error,cal=cal,output=output))
                            return render_template("notitab2.html",error=error)
                    else:
                        error = "The Time or Date Entered Is Incorrect. Please Enter Correct Time and Date."
                        return render_template("notitab2.html",error=error)
                else:
                    app.logger.info("Check Failed!")
                    error = "Hall Not Available At given Date and Time."
                    # return redirect(url_for("index",error=error,cal=cal,output=output))
                    return render_template("notitab2.html",error=error)
            if hallname2=="Auditorium":
                return render_template("audi.form.html",scname=scname,error=error,cal=cal,output=output,date=date,startTime=startTime,endTime=endTime,day=day)
            elif hallname2=="SeminarHall":
                return render_template("seminar.html",scname=scname,error=error,cal=cal,output=output,date=date,startTime=startTime,endTime=endTime,day=day)
            elif hallname2=="Room105":
                return render_template("room105.html",scname=scname,error=error,cal=cal,output=output,date=date,startTime=startTime,endTime=endTime,day=day)
            elif hallname2=="CRCConferenceRoom":
                return render_template("crc.html",scname=scname,error=error,cal=cal,output=output,date=date,startTime=startTime,endTime=endTime,day=day)
            elif hallname2=="Seminarvip":
                return render_template("Seminar.VIP.html",scname=scname,error=error,cal=cal,output=output,date=date,startTime=startTime,endTime=endTime,day=day)
            elif hallname2=="RICSConferenceRoom":
                return render_template("RICS.html",scname=scname,error=error,cal=cal,output=output,date=date,startTime=startTime,endTime=endTime,day=day)
            elif hallname2=="Atrium":
                return render_template("Atrium.html",scname=scname,error=error,cal=cal,output=output,date=date,startTime=startTime,endTime=endTime,day=day)
            elif hallname2=="VVIP":
                return render_template("vvip.form.html",scname=scname,error=error,cal=cal,output=output,date=date,startTime=startTime,endTime=endTime,day=day)
            elif hallname2=="AIB206":
                return render_template("AIB206.html",scname=scname,error=error,cal=cal,output=output,date=date,startTime=startTime,endTime=endTime,day=day)
            elif hallname2=="ABS304":
                return render_template("ABS304.html",scname=scname,error=error,cal=cal,output=output,date=date,startTime=startTime,endTime=endTime,day=day)
            elif hallname2=="AIBAS504":
                return render_template("AIBAS504.html",scname=scname,error=error,cal=cal,output=output,date=date,startTime=startTime,endTime=endTime,day=day)
            elif hallname2=="ASET123":
                return render_template("ASET123.html",scname=scname,error=error,cal=cal,output=output,date=date,startTime=startTime,endTime=endTime,day=day)
            elif hallname2=="ALS602":
                return render_template("ALS602.html",scname=scname,error=error,cal=cal,output=output,date=date,startTime=startTime,endTime=endTime,day=day)
            
            #return render_template("index.html",error=error,cal=cal,output=output)
        else:
            return redirect(url_for('userlogin'))
    # except Exception as e:

    except Exception as e:
        app.logger.info(e)
        app.logger.error(e)
        return render_template("notitab6.html",error="Error in URL. Please use only http://amischeduler.aum.amity.edu.in. Redirecting to Login Page.")
        # return redirect(url_for('userlogin'))
    

@app.route('/test',methods=['GET','POST'])
def test():
    if request.method == 'POST':
        app.logger.info("METHOD ACTIVATE")
        bid = request.form["booking_id"]
        status = request.form["status"]
        app.logger.info(f'{bid},{status}')
    if session['username']:
        username = session['username']
        output = db.check_request(username)
        # app.logger.info(output)
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

@app.route('/resetpassworduser',methods=['GET','POST'])
def resetuser():
    if request.method == 'POST':
        # app.logger.info('here')
        # app.logger.info(request.data)
        # app.logger.info(request.is_json)
        username = request.form["user-username"]
        oldpass = request.form["old-password"]
        newpass = request.form["new-password"]
        app.logger.info(f'{username},{oldpass},{newpass}')
        if login.resetpassuser(username,oldpass,newpass):
            return render_template('notitab3.html',error="Password Reset Successfully.")
        else:
            return render_template('reset.user.html',server_link=server_link,error="Incorrect Credentials. Please try again")
        pass
    return render_template('reset.user.html',server_link=server_link)

@app.route('/resetpasswordadmin',methods=['GET','POST'])
def resetadmin():
    if request.method == 'POST':
        # app.logger.info('here')
        # app.logger.info(request.data)
        # app.logger.info(request.is_json)
        username = request.form["user-username"]
        oldpass = request.form["old-password"]
        newpass = request.form["new-password"]
        app.logger.info(f'{username},{oldpass},{newpass}')
        if login.resetpassadmin(username,oldpass,newpass):
            return render_template('notitab4.html',error="Password Reset Successfully.")
        else:
            return render_template('reset.admin.html',server_link=server_link,error="Incorrect Credentials. Please try again")
        pass
    return render_template('reset.admin.html',server_link=server_link)

#futurescope
@app.route('/verifyemail/<username>' ,methods=['GET', 'POST'])
def verifyemail(username):
    # global code_list
    alert = None
    email = login.getname_user(username)
    if request.method == 'POST':
        code = request.form["verification-code"]
        # app.logger.info(code_list)
        # app.logger.info(code)
        # app.logger.info(username)
        if (int(code) in code_list):
            #alert = 'Please use a valid @mum.amity.edu email address for signup.'
            # app.logger.info(code)    
            state = login.verifyemail(username)
            # app.logger.info(state)

            if state == True :
                return redirect(url_for('userlogin'))
            else:
                alert = "Incorrect server response entered please try again."
                # app.logger.info(code)
                # app.logger.info(code_list)
                return render_template('verifyemail.html',error=alert,email=email)
        else:
            alert = "Incorrect code entered please try again."
            # app.logger.info(code)
            # app.logger.info(code_list)
            return render_template('verifyemail.html',error=alert,email=email)
    else:
        return render_template('verifyemail.html',error=alert,email=email)
        
    return render_template('verifyemail.html',error=alert,email=email)


#main runtime
if __name__ == '__main__':
    app.run(debug=True,port=8000)

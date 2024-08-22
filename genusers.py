import secrets
import string
sc = ['ASET','ABS','AFS','AIBAS','AIB','AIIT','AILA','AIP','AIT','AITT','ALS','ASAP','ASAS','ASCO','ASFT','ASL','CIIOL','TUCSSBERICS','ASFA','AIE','AIN','Director_Admin_1','Director_Admin_2','CRC_Dept','HR_Dept','Hostel_Security_Dept','Admissions_Dept','Examinations_Dept']
sc2 = ['Director_Admin_1','Director_Admin_2','CRC_Dept','HR_Dept','Hostel_Security_Dept','Admissions_Dept','Examinations_Dept']
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
                'Director_Admin_1':'Director_Admin_1',
                'Director_Admin_2':'Director_Admin_2',
                'CRC_Dept':'CRC_Dept',
                'HR_Dept':'HR_Dept',
                'Hostel_Security_Dept':'Hostel_Security_Dept',
                'Admissions_Dept':'Admissions_Dept',
                'Examinations_Dept':'Examinations_Dept',
                }
def genpass():
    # al = string.ascii_letters + string.digits
    al = string.digits
    passwd = ''.join(secrets.choice(al) for i in range(5))
    return passwd
# final = {}
# for i in sc:
#     uname = f"{i}_venue"
#     passwd = f"venue_{genpass()}"
#     final[uname] = passwd
# print(final)
final = {'ASET_venue': 'venue_00686', 'ABS_venue': 'venue_29395', 'AFS_venue': 'venue_19823', 'AIBAS_venue': 'venue_96499', 'AIB_venue': 'venue_37460', 'AIIT_venue': 'venue_97950', 'AILA_venue': 'venue_22533', 'AIP_venue': 'venue_86056', 'AIT_venue': 'venue_65254', 'AITT_venue': 'venue_03396', 'ALS_venue': 'venue_39540', 'ASAP_venue': 'venue_31726', 'ASAS_venue': 'venue_58037', 'ASCO_venue': 'venue_56366', 'ASFT_venue': 'venue_28042', 'ASL_venue': 'venue_10844', 'CIIOL_venue': 'venue_06932', 'TUCSSBERICS_venue': 'venue_40988', 'ASFA_venue': 'venue_02634', 'AIE_venue': 'venue_81354', 'AIN_venue': 'venue_82477','Director_Admin_1': 'venue_22223','Director_Admin_2': 'venue_33334','CRC_Dept': 'venue_44445','HR_Dept': 'venue_55556','Hostel_Security_Dept': 'venue_66667','Admissions_Dept': 'venue_77778','Examinations_Dept': 'venue_88889','IT_dept':'venue_99990'}
admin = {'Administrator': 'vcaum@123','Director_admin_1': 'venue_22222','Director_admin_2': 'venue_33333','Crc_dept': 'venue_44444','Hr_dept': 'venue_55555','Hostel_security_dept': 'venue_66666','Admissions_dept': 'venue_77777','Examinations_dept': 'venue_88888','IT_dept':'venue_99999','testdebug':'test'}

# f = open('example.txt','a')
# for i in sc:
#     l = sc.index(i)
#     uname = f"{i}_venue"
#     f.write(f"""
            
#     Ami-Scheduler Link : http://10.5.2.29/
#     School Name : {userdict[i]}
#     UserID : {uname}
#     Password : {final[uname]}
            

#     """)

f = open('example.txt','a')
for i in sc2:
    l = sc2.index(i)
    uname = f"{i}"
    f.write(f"""
            
    Ami-Scheduler Link : http://10.5.2.29/
    School Name : {userdict[i]}
    UserID : {uname}
    Password : {final[uname]}
            

    """)
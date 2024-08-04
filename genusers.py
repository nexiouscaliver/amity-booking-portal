import secrets
import string
sc = ['ASET','ABS','AFS','AIBAS','AIB','AIIT','AILA','AIP','AIT','AITT','ALS','ASAP','ASAS','ASCO','ASFT','ASL','CIIOL','TUCSSBERICS','ASFA','AIE','AIN']
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
final = {'ASET_venue': 'venue_00686', 'ABS_venue': 'venue_29395', 'AFS_venue': 'venue_19823', 'AIBAS_venue': 'venue_96499', 'AIB_venue': 'venue_37460', 'AIIT_venue': 'venue_97950', 'AILA_venue': 'venue_22533', 'AIP_venue': 'venue_86056', 'AIT_venue': 'venue_65254', 'AITT_venue': 'venue_03396', 'ALS_venue': 'venue_39540', 'ASAP_venue': 'venue_31726', 'ASAS_venue': 'venue_58037', 'ASCO_venue': 'venue_56366', 'ASFT_venue': 'venue_28042', 'ASL_venue': 'venue_10844', 'CIIOL_venue': 'venue_06932', 'TUCSSBERICS_venue': 'venue_40988', 'ASFA_venue': 'venue_02634', 'AIE_venue': 'venue_81354', 'AIN_venue': 'venue_82477'}
admin = {'Administrator': 'vcaum@123','Director_admin_1': 'venue_22222','Director_admin_2': 'venue_33333','Crc_dept': 'venue_44444','Hr_dept': 'venue_55555','Hostel_security_dept': 'venue_66666','Admissions_dept': 'venue_77777','Examinations_dept': 'venue_88888','testdebug':'test'}

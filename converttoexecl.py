import pandas as pd

dict1 = {'ASET_venue': 'venue_00686', 'ABS_venue': 'venue_29395', 'AFS_venue': 'venue_19823', 'AIBAS_venue': 'venue_96499', 'AIB_venue': 'venue_37460', 'AIIT_venue': 'venue_97950', 'AILA_venue': 'venue_22533', 'AIP_venue': 'venue_86056', 'AIT_venue': 'venue_65254', 'AITT_venue': 'venue_03396', 'ALS_venue': 'venue_39540', 'ASAP_venue': 'venue_31726', 'ASAS_venue': 'venue_58037', 'ASCO_venue': 'venue_56366', 'ASFT_venue': 'venue_28042', 'ASL_venue': 'venue_10844', 'CIIOL_venue': 'venue_06932', 'TUCSSBERICS_venue': 'venue_40988', 'ASFA_venue': 'venue_02634', 'AIE_venue': 'venue_81354', 'AIN_venue': 'venue_82477','Director_Admin_1': 'venue_22223','Director_Admin_2': 'venue_33334','CRC_Dept': 'venue_44445','HR_Dept': 'venue_55556','Hostel_Security_Dept': 'venue_66667','Admissions_Dept': 'venue_77778','Examinations_Dept': 'venue_88889','IT_dept':'venue_99990'}
dict2 = {'Administrator': 'vcaum@123','Director_admin_1': 'venue_dir1','Director_admin_2': 'venue_dir2','Crc_dept': 'venue_crc','Hr_dept': 'venue_hr','Hostel_security_dept': 'venue_hostel','Admissions_dept': 'venue_addm','Examinations_dept': 'venue_exam','IT_dept':'venue_it','testdebug':'test'}
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
                'IT_Dept':'IT Department'
                }
df = pd.DataFrame(data=dict1, index=[0])

df = (df.T)

print (df)

df.to_excel('adminpass2.xlsx')
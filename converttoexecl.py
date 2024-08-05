import pandas as pd

dict1 = {'ASET_venue': 'venue_00686', 'ABS_venue': 'venue_29395', 'AFS_venue': 'venue_19823', 'AIBAS_venue': 'venue_96499', 'AIB_venue': 'venue_37460', 'AIIT_venue': 'venue_97950', 'AILA_venue': 'venue_22533', 'AIP_venue': 'venue_86056', 'AIT_venue': 'venue_65254', 'AITT_venue': 'venue_03396', 'ALS_venue': 'venue_39540', 'ASAP_venue': 'venue_31726', 'ASAS_venue': 'venue_58037', 'ASCO_venue': 'venue_56366', 'ASFT_venue': 'venue_28042', 'ASL_venue': 'venue_10844', 'CIIOL_venue': 'venue_06932', 'TUCSSBERICS_venue': 'venue_40988', 'ASFA_venue': 'venue_02634', 'AIE_venue': 'venue_81354', 'AIN_venue': 'venue_82477','Director_Admin_1': 'venue_22223','Director_Admin_2': 'venue_33334','CRC_Dept': 'venue_44445','HR_Dept': 'venue_55556','Hostel_Security_Dept': 'venue_66667','Admissions_Dept': 'venue_77778','Examinations_Dept': 'venue_88889'}
dict2 =  {'Administrator': 'vcaum@123','Director_Admin_1': 'venue_22222','Director_Admin_2': 'venue_33333','CRC_Dept': 'venue_44444','HR_Dept': 'venue_55555','Hostel_Security_Dept': 'venue_66666','Admissions_Dept': 'venue_77777','Examinations_Dept': 'venue_88888','testdebug':'test'}

df = pd.DataFrame(data=dict2, index=[0])

df = (df.T)

print (df)

df.to_excel('adminpass2.xlsx')
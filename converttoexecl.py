import pandas as pd

dict1 = {'Administrator': 'vcaum@123','Director_admin_1': 'venue_22222','Director_admin_2': 'venue_33333','Crc_dept': 'venue_44444','Hr_dept': 'venue_55555','Hostel_security_dept': 'venue_66666','Admissions_dept': 'venue_77777','Examinations_dept': 'venue_88888','testdebug':'test'}
df = pd.DataFrame(data=dict1, index=[0])

df = (df.T)

print (df)

df.to_excel('adminpass.xlsx')
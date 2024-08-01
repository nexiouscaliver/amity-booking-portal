import secrets
import string
sc = ['ASET','ABS','AFS','AIBAS','AIB','ALIT','ALIA','AIP','AIT','AITT','ALS','ASAP','ASAS','ASCO','ASFT','ASL','CIIOL','RICS','ASFA','AIE','AIN']
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
final = {'ASET_venue': 'venue_64871', 'ABS_venue': 'venue_42833', 'AFS_venue': 'venue_25858', 'AIBAS_venue': 'venue_70005', 'AIB_venue': 'venue_59460', 'ALIT_venue': 'venue_75586', 'ALIA_venue': 'venue_51953', 'AIP_venue': 'venue_36494', 'AIT_venue': 'venue_29146', 'AITT_venue': 'venue_08191', 'ALS_venue': 'venue_22092', 'ASAP_venue': 'venue_27502', 'ASAS_venue': 'venue_36607', 'ASCO_venue': 'venue_81334', 'ASFT_venue': 'venue_95570', 'ASL_venue': 'venue_76994', 'CIIOL_venue': 'venue_55920', 'RICS_venue': 'venue_39966', 'ASFA_venue': 'venue_74293', 'AIE_venue': 'venue_42924', 'AIN_venue': 'venue_68913','testdebug':'test'}
admin = {'ADMIN_venue': 'venue_00000','ADMIN2_venue': 'venue_22222','ADMIN3_venue': 'venue_33333','ADMIN4_venue': 'venue_44444','testdebug':'test'}

import secrets
import string
sc = ['ASET','ABS','AFS','AIBAS','AIB','ALIT','ALIA','AIP','AIT','AITT','ALS','ASAP','ASAS','ASCO','ASFT','ASL','CIIOL','RICS','ASFA','AIE','AIN']
def genpass():
    al = string.ascii_letters + string.digits
    passwd = ''.join(secrets.choice(al) for i in range(6))
    return passwd
# final = {}
# for i in sc:
#     uname = f"{i}_venue"
#     passwd = f"venue_{genpass()}"
#     final[i] = passwd
# print(final)
final = {'ASET': 'venue_00XzX4', 'ABS': 'venue_CeVxyR', 'AFS': 'venue_rAEuV9', 'AIBAS': 'venue_JIpjeR', 'AIB': 'venue_u3A9r0', 'ALIT': 'venue_ds60u0', 'ALIA': 'venue_J6II2R', 'AIP': 'venue_SwrT9y', 'AIT': 'venue_XEjHaa', 'AITT': 'venue_qtw83A', 'ALS': 'venue_qOk3sy', 'ASAP': 'venue_wuEPwV', 'ASAS': 'venue_I8Fc0C', 'ASCO': 'venue_RthX8G', 'ASFT': 'venue_8wOPPy', 'ASL': 'venue_zEb1vK', 'CIIOL': 'venue_3XV5CD', 'RICS': 'venue_nMEQqD', 'ASFA': 'venue_ZhFINZ', 'AIE': 'venue_4w5K1z', 'AIN': 'venue_Y33bR1'}
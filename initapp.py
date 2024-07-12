import dbscript as db
import loginscript as login
import genusers as gu

db.init()
login.init_db()

for i in gu.final:
    u = i
    p = gu.final[i]
    login.create_user(i,p)
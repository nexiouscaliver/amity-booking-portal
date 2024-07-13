import dbscript as db
import loginscript as login
import genusers as gu

db.init()
login.init_db()

for i in gu.final:
    u = i
    p = gu.final[i]
    print(i,p,i[:-6])
    login.create_user(i,p,i[:-6])
    print(f"created new user :{i} pass: {p} for school: {i[:-6]}")

for i in gu.admin:
    u = i
    p = gu.admin[i]
    print(i,p,i[:-6])
    login.create_admin(i,p,i[:-6])
    print(f"created new admin :{i} pass: {p} for name: {i[:-6]}")
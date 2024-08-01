givenhost = input("Enter the host name: ")
givenuser = input("Enter the user name: ")
givenpas = input("Enter the password: ")
givenport = input("Enter the port number: ")

f = open('dbscript.py','r')
data = f.readlines()
host = data[2]
user = data[3]
pas = data[4]
port = data[5]


data[2] = "hostname = '" + givenhost + "'\n"
data[3] = "username = '" + givenuser + "'\n"
data[4] = "passwd = '" + givenpas + "'\n"
data[5] = "portnum = '" + givenport + "'\n"

f = open('dbscript.py','w')
f.truncate(00)
f.writelines(data)
f.close()

f = open('loginscript.py','r')
data = f.readlines()
host = data[5]
user = data[6]
pas = data[7]
port = data[8]


data[5] = "hostname = '" + givenhost + "'\n"
data[6] = "username = '" + givenuser + "'\n"
data[7] = "passwd = '" + givenpas + "'\n"
data[8] = "portnum = '" + givenport + "'\n"

f = open('loginscript.py','w')
f.truncate(00)
f.writelines(data)
f.close()
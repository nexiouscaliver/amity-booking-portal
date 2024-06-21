##main flask app :: Shahil kadia

from flask import *
from flask import request, jsonify
from werkzeug.utils import secure_filename
from time import ctime
import dbscript as db
import loginscript as login

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
app.secret_key =  "AMITY_792739"
app.config['SECRET_KEY'] = "AMITY_792739"

#task-related functions
def hallname(hallid:int):
    l = [0,"Auditorium Hall","Seminar Hall","Room No. 105, A2 Building","CRC Conference Room"]
    return (l[hallid])


#routing functions
@app.route('/')
def home():
    data=hallname(4)
    return render_template("test1.html",data=data)

@app.route('/index' ,methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass
    return render_template("index.html")


@app.route('/admin' ,methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        pass
    return render_template("admin-page.html")









#main runtime
if __name__ == '__main__':
    app.run(debug=True,port=7000)

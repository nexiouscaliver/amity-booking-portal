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



@app.route('/')
def home():
    return render_template("test1.html")














#main runtime
if __name__ == '__main__':
    app.run(debug=True,port=7000)

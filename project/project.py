from flask import Flask
from flask import render_template,request,redirect,url_for,session
from models import User
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash

import config
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/register/',methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template('register.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #check whether the email is already registered
        user=User.query.filter(User.email==email).first()
        if user:
            return u'This email is already registered. Please change another one'
        else:
        # check whether two passwords are the same
            if password1!=password2:
                return u'Passwords are not the same.'
            else:
                password=generate_password_hash(password1)
                user=User(email=email,username=username,password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/',methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        # password = generate_password_hash(password)
        # user = User.query.filter(User.email == email,User.password == password).first()
        # if user:
        user = User.query.filter(User.email == email).first()
        if user:
            if check_password_hash(user.password, password):
                session['user_id']=user.id
                #如果想在31天内都不需要登录
                session.permanent=True
                return u'You are logged in successfully.'
            else:
                return u'The password is wrong.'
        else:
            return u'The email is invalid.'
if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)


app.config["SECRET_KEY"] = 'iwritesometimes'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


@app.route('/')
def home():
    return render_template('home.html', title='Home')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template('login.html', title='Log In', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        found_user = User.query.filter_by(username=username).first()
        found_email = User.query.filter_by(email=email).first()
        if(found_user or found_email):  # here if data already exists,
            flash("This username already exists!", 'warning')
            return render_template('signup.html', title='Sign Up', form=form)
        else:
            usr = User(username, email, password)
            db.session.add(usr)
            db.session.commit()
        flash(f"hello {username}, with the email {email}.", 'success')
        return render_template('home.html', title='Home')

    return render_template('signup.html', title='Sign Up', form=form)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

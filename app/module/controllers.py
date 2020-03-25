from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

# Import module models (i.e. User)
from app.module.models import User

import datetime

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('app', __name__)

# Set the route and accepted methods

# custom route to redirect to login page
@mod_auth.route('/')
def index():
    return render_template('landing_page.html')

# User routes
# login route
@mod_auth.route('/login_user', methods=["GET", "POST"])
def login():
	# if current_user.is_authenticated:
	# 	return redirect('/home')
	# if request.method == "POST":
	# 	email = request.form.get("email")
	# 	pwd = request.form.get("pwd")

	# 	search = User.query.filter_by(email=email).first()

	# 	if search is None:
	# 		data['msg'] = "Invalid username/password"
	# 	else:
	# 		if search.check_password(pwd):
	# 			login_user(search)
	# 			return redirect('/home')
	return render_template('user_login.html')

@mod_auth.route('/register', methods=["GET", "POST"])
def register():
	# data = {

	# }
	# if current_user.is_authenticated:
	# 	return "LEMAO"

	# if request.method == "POST":
	# 	name = request.form.get('name')
	# 	student_id = request.form.get('id')
	# 	email = request.form.get('email')
	# 	password = request.form.get('pwd')
	# 	hall = request.form.get('hall')
	# 	level = request.form.get('level')
	# 	course = request.form.get('course')
	# 	number = request.form.get('number')
	# 	try:
	# 		new_user = User(ids=student_id, email=email, registered_on=datetime.datetime.today(),\
	# 		password_hash=generate_password_hash(password),\
	# 		full_name=name, level=level, momo_number=number)
	# 		db.session.add(new_user)
	# 		db.session.commit()
	# 		login_user(new_user, remember=True)
	# 		return redirect('/home')
	# 	except:
	# 		data['msg'] = "An account already exists with this ID/Email"
	# 		return render_template('login.html', **data)
	return render_template('user_register.html')

@mod_auth.route('/logout')
def logout():
	logout_user()
	return redirect('/login')

@mod_auth.route('/home')
def home():
	print(current_user)
	return render_template('user_home.html')

@mod_auth.route('/wallet')
def wallet():
	return render_template('user_wallet.html')

@mod_auth.route('/profile')
def user_profile():
	return render_template('user.html')

@mod_auth.route('/pay')
def pay():
	return render_template('user_payment.html')
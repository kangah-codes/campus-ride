from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

# Import module models (i.e. User)
from app.module.models import User
import json
import datetime
import sqlalchemy

"""
tk_f0f2bb56-6f86-11ea-b8e9-f23c9170642f
"""


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('app', __name__)

# global functions
def comparePass(pwd1, pwd2):
	return pwd1 == pwd2

# Set the route and accepted methods

# custom route to redirect to login page
@mod_auth.route('/')
def index():
    return render_template('landing_page.html')

# User routes
# login route
@mod_auth.route('/login_user', methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect('/home')
	if request.method == "POST":
		stid = request.form.get("id")
		pwd = request.form.get("pwd")
		rem = request.form.get("rem")
		search = User.query.filter_by(public_id=stid).first()

		if rem == None:
			login_user(search, remember=False)
			return redirect('/home')
		login_user(search, remember=True)
		return redirect('/home')
		print(search)
		# if search is None:
		# 	data['msg'] = "Invalid username/password"
		# else:
		# 	if search.check_password(pwd):
		# 		login_user(search)
		# 		return redirect('/home')
	return render_template('user_login.html')

@mod_auth.route('/register', methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect('/home')

	error = None

	if request.method == "POST":
		name = request.form.get('full_name')
		student_id = request.form.get('st_id')
		email = request.form.get('st_mail')
		password = request.form.get('pwd1')
		password_compare = request.form.get('pwd2')
		hall = request.form.get('hall')
		level = request.form.get('level')
		course = request.form.get('course')
		number = request.form.get('phone')
		try:
			if not comparePass(password, password_compare):
				error = "Passwords must match"
			else:
				new_user = User(ids=student_id, email=email, registered_on=datetime.datetime.today(),\
				password_hash=generate_password_hash(password),\
				full_name=name, level=level, momo_number=number)
				new_user.course = course
				new_user.hall = hall
				new_user.is_activated = False
				new_user.notifications = json.dumps('{"New notification":f"Account created at {datetime.datetime.today()}"}')
				try:
					db.session.add(new_user)
					db.session.commit()
					login_user(new_user, remember=True)
					flash("Logged in")
					return redirect('/home')
				except:
					error = "Sorry, there has been a server error, please try later"
					db.session.rollback()
				finally:
					db.session.close()
		except:
			error = "An account already exists with this email/ID"
			return render_template('user_register.html')
	return render_template('user_register.html', error=error)

@mod_auth.route('/logout')
def logout():
	logout_user()
	return redirect('/login_user')

@mod_auth.route('/home')
def home():
	data = {
		"first_name":current_user.full_name.split(' ')[0],
		"bal":current_user.account_bal,
		"ride_history":current_user.ride_history,
		"payment_history":json.loads(current_user.payment_history),
	}
	return render_template('user_home.html', **data)

@mod_auth.route('/wallet')
def wallet():
	data = {
		"bal":current_user.account_bal,
	}
	return render_template('user_wallet.html', **data)

@mod_auth.route('/user_pay/<bus>')
def user_pay(bus):
	return ""

@mod_auth.route('/profile', methods=['GET', 'POST'])
def user_profile():
	error = None
	data = {
		"first_name":current_user.full_name.split(' ')[0],
		"last_name":current_user.full_name.split(' ')[-1],
		"stid":current_user.public_id,
		"email":current_user.email,
		"hall":current_user.hall,
		"number":current_user.momo_number,
		"level":current_user.level,
		"course":current_user.course,
		"full_name":current_user.full_name,
	}

	if request.method == "POST":
		print(current_user.level)
		hall = request.form.get("hall")
		number = request.form.get("number")
		level = request.form.get("level")
		course = request.form.get("course")

		current_user.hall = hall
		current_user.momo_number = number
		current_user.level = level
		current_user.course = course

		print(current_user.level)

		try:
			db.session.add(current_user)
			db.session.commit()
		except:
			error = "Server error, please try later"
			db.session.rollback()
		
		return redirect('/profile')	

	return render_template('user.html', **data)

@mod_auth.route('/pay')
def pay():
	return render_template('user_payment.html')
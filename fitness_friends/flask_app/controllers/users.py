from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('log_reg.html')


@app.route('/user/create', methods=['POST'])
def create():
    if not user.User.is_valid_user(request.form):
        return redirect('/')
    hashed_password = bcrypt.generate_password_hash(request.form['password'])

    data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'date_of_birth':request.form['date_of_birth'],
        'zipcode':request.form['zipcode'],
        'email':request.form['email'],
        'password':hashed_password
    }

    one_user_id =user.User.save(data)
    session['user_id'] = one_user_id
    return redirect('/workouts/dashboard')

@app.route('/user/login', methods=['POST'])
def login():
    one_user= user.User.validate_login(request.form)

    if not one_user:
        return redirect('/')
    session['user_id']= one_user.id
    return redirect('/workouts/dashboard')

@app.route('/users/edit/<int:id>')
def edit_user(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id':id
    }
    return render_template('edit_user.html',one_user=user.User.get_user_by_id(data))

@app.route('/user/update', methods=['POST'])
def update_sighting():
    if 'user_id' not in session:
        return redirect('/')
    if not user.User.is_valid_update(request.form):
        return redirect(f'/users/edit/{request.form["id"]}')
    user.User.update_user(request.form)
    return redirect('/workouts/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
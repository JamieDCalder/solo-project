from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models import user,workout

@app.route('/workouts/dashboard')
def workouts_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id':session['user_id']
    }
    return render_template('dashboard.html', workouts=workout.Workout.get_all_workouts(), one_user=user.User.get_user_by_id(data))

@app.route('/workout/new')
def new_workout():
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id':session['user_id']
    }
    return render_template('new.html', one_user=user.User.get_user_by_id(data))

@app.route('/workouts/create/new', methods=["POST"])
def create_workout():
    form_data = request.form
    if not workout.Workout.validate_workout(form_data):
        return redirect('/workout/new')

    workout.Workout.save_workout(form_data)
    return redirect('/workouts/dashboard')

@app.route('/workouts/edit/<int:id>')
def edit_workout(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id':id
    }
    return render_template('edit.html',one_workout=workout.Workout.get_one_workout(data))

@app.route('/workouts/update', methods=['POST'])
def update_workout():
    if 'user_id' not in session:
        return redirect('/')
    if not workout.Workout.validate_workout(request.form):
        return redirect(f'/workouts/edit/{request.form["id"]}')
    workout.Workout.update_workout(request.form)
    return redirect('/workouts/dashboard')

@app.route('/workouts/delete/<int:id>')
def delete_workout(id):
    if 'user_id' not in session:
        return redirect('/')
    workout.Workout.destroy_workout({'id':id})
    return redirect('/workouts/dashboard')
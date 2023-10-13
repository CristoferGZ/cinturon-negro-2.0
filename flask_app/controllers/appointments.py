from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.appointment import Appointment
from flask_app.models.user import User


@app.route('/new/appointment')
def new_appointment():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    flash("¡Nueva cita creada correctamente!", "success")  # Agrega un mensaje flash de éxito
    return render_template('new_Appointment.html', user=User.get_by_id(data))

@app.route('/create/appointment',methods=['POST'])
def create_appointment():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Appointment.validate_appointment(request.form):
        return redirect('/new/appointment')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under30": int(request.form["under30"]),
        "date_made": request.form["date_made"],
        "user_id": session["user_id"]
    }
    Appointment.save(data)
    return redirect('/dashboard')

@app.route('/edit/appointment/<int:id>')
def edit_appointment(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_appointment.html",edit=Appointment.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/appointment',methods=['POST'])
def update_appointment():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Appointment.validate_(request.form):
        return redirect('/new/appointment')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under30": int(request.form["under30"]),
        "date_made": request.form["date_made"],
        "id": request.form['id']
    }
    Appointment.update(data)
    return redirect('/dashboard')

@app.route('/appointment/<int:id>')
def show_appointment(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_appointment.html",appointment=Appointment.get_one(data),user=User.get_by_id(user_data))


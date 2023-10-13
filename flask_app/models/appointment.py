from flask_app.config.mysqlconnection import connectToMySQL  # Importa la función para conectarse a la base de datos.
from datetime import datetime  # Importa el objeto date para trabajar con fechas.
from flask import flash  # Importa la función flash para mostrar mensajes en Flask.

db = "esquema_citas"
class Appointment:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.status = data.get('status')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.user_id = data.get('user_id')

    @classmethod
    def save(cls, data):
        query = "INSERT INTO appointments ('name', 'status', 'date_made', 'created_at', 'updated_at') VALUES (%(name)s, %(status)s, %(date_made)s, NOW(), NOW(), %(user_id)s)"
        return connectToMySQL("esquema_citas").query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM appointments;"
        results = connectToMySQL("esquema_citas").query_db(query)
        print(results)  # Verifica los datos devueltos en la consola del servidor Flask
        all_appointments = []
        for row in results:
            all_appointments.append(cls(row))
        return all_appointments
    




    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM appointments WHERE id = %(id)s;"
        results = connectToMySQL("esquema_citas").query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE appointments SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under30=%(under30)s, date_made=%(date_made)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL("esquema_citas").query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM appointments WHERE id = %(id)s;"
        return connectToMySQL("esquema_citas").query_db(query,data)
    
    @staticmethod
    def validate_appointment(appointment):
        is_valid = True
        if len(appointment['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters","appointment")
        if len(appointment['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters","appointment")
        if len(appointment['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","appointment")
        if appointment['date_made'] == "":
            is_valid = False
            flash("Please enter a date","appointment")
        return is_valid

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    DB = 'fitness_friends_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.date_of_birth = data['date_of_birth']
        self.zipcode = data['zipcode']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#CREATE - SQL

#save user

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users (first_name,last_name,email,zipcode,date_of_birth,password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(zipcode)s, %(date_of_birth)s, %(password)s)
        ;"""
        return connectToMySQL(cls.DB).query_db(query,data)

#READ - SQL
#will need get user by email and id

    @classmethod
    def get_user_by_email(cls, data):
        query = """
        SELECT * 
        FROM users
        WHERE email = %(email)s;
        ;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_user_by_id(cls,data):
        query = """
        SELECT * 
        FROM users
        WHERE id = %(id)s;
        ;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return cls(result[0])

#UPDATE - SQL

    @classmethod
    def update_user(cls,data):
        query="""
        UPDATE users
        SET first_name=%(first_name)s, last_name=%(last_name)s, date_of_birth=%(date_of_birth)s, zipcode=%(zipcode)s
        WHERE id=%(id)s
        ;"""
        return connectToMySQL(cls.DB).query_db(query,data)

#DELETE - SQL

    @classmethod
    def destroy_user(cls,data):
        query="""
        DELETE FROM users
        WHERE id=%(id)s
        ;"""

        return connectToMySQL(cls.DB).query_db(query,data)

#STATIC - SQL

#validate register and login

    @staticmethod
    def is_valid_user(data):
        is_valid = True
        one_user=User.get_user_by_email(data)

        if one_user:
            flash('Please login.','register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address.",'register')
            is_valid = False
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.",'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters.",'register')
            is_valid = False
        if len(data['zipcode']) != 5:
            flash("Please provide 5 digit zipcode.",'register')
            is_valid = False
        if len(data['date_of_birth']) == 0:
            flash("Please provide date of birth.",'register')
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.",'register')
            is_valid = False
        if data["password"] != data["confirm"]:
            flash('Passwords do not match.','register')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(data):
        one_user=User.get_user_by_email(data)

        if not one_user:
            flash('Invalid credentials.','login')
            return False
        if not bcrypt.check_password_hash(one_user.password, data['password']):
            flash('Invalid credentials.','login')
            return False
        return one_user
    
    @staticmethod
    def is_valid_update(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.",'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters.",'register')
            is_valid = False
        if len(data['zipcode']) != 5:
            flash("Please provide 5 digit zipcode.",'register')
            is_valid = False
        if len(data['date_of_birth']) == 0:
            flash("Please provide date of birth.",'register')
            is_valid = False
        return is_valid

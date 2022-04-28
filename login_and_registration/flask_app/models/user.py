from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def save(cls,data):
        query="INSERT INTO logins (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL('logins').query_db(query,data)

    @classmethod
    def get_all(cls):
        query= "SELECT * from logins;"
        results= connectToMySQL('logins').query_db(query)
        logins=[]
        for row in results:
            logins.append(cls(row))
        return logins

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM logins WHERE email = %(email)s;"
        results = connectToMySQL('logins').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM logins WHERE id = %(id)s;"
        results = connectToMySQL('logins').query_db(query,data)
        return cls(results[0])

    @staticmethod
    def is_valid(user):
        is_valid=True
        query="SELECT * FROM logins WHERE email=%(email)s;"
        results= connectToMySQL('logins').query_db(query,user)
        if len(results)>=1:
            flash("Email has already been taken")
            is_valid=False
        if len(user['first_name']) < 2:
            is_valid = False
            flash("First name must be at least 2 characters.")
        if len(user['last_name']) < 2:
            is_valid = False
            flash("Last name must be at least 2 characters.")
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!")
            is_valid=False
        if len(user['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters")
        if user['password'] != user['confirm_password']:
            flash ("Passwords don't match, please check again")
        return is_valid
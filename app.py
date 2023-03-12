import os

from flask import Flask
from flask_restful import Api

from Login_manager_api import Login_api
from Role_manager_api import Role_api
from model import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.getcwd() + \
    '/DB_project.sqlite3'
api = Api(app)

app.config['SECRET_KEY'] = 'FMM-2'
db.init_app(app)
app.app_context().push()
db.create_all()

api.add_resource(Login_api, '/api/register', '/api/login/<string:email>')
api.add_resource(Role_api, '/api/role', '/api/role/<int:user_id>')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port='5500')

import os

from flask import Flask
from flask_restful import Api

from Login_manager_api import Login_api
from model import db
from Role_manager_api import Role_api
from Tag_manager_api import Tag_api
from Ticket_manager_api import Ticket_api

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
api.add_resource(Ticket_api, '/api/subject/ticket/<int:ticket_id>',
                 '/api/subject/<string:subject_name>')

api.add_resource(Tag_api,
                 '/api/tag/<string:tag_type>','/api/tag/<string:tag_type>/<int:tag_id>')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5500')

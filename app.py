import os
from flask_jwt_extended import JWTManager, create_access_token
from flask import Flask, request
from flask_restful import Api
from werkzeug.security import check_password_hash
import datetime
from model import User, db
from custom_error import *
from Login_manager_api import Login_api
from Role_manager_api import Role_api
from Tag_manager_api import Tag_api
from Ticket_manager_api import Ticket_api
from Response_api_for_TM import Responses_api
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.getcwd() + \
    '/DB_project.sqlite3'
api = Api(app)

app.config['SECRET_KEY'] = 'FMM-2'
CORS(app)
JWTManager(app)
db.init_app(app)
app.app_context().push()
db.create_all()

api.add_resource(Login_api, '/api/register', '/api/login/<string:email>')
api.add_resource(Role_api, '/api/role', '/api/role/<int:user_id>')
api.add_resource(Ticket_api, '/api/subject/ticket/<int:ticket_id>',
                 '/api/subject/<string:subject_name>')

api.add_resource(Responses_api, '/api/response', '/api/response/<int:ticket_id>',
                 '/api/response/<int:ticket_id>/<int:response_id>')

api.add_resource(Tag_api,
                 '/api/tag/<string:tag_type>', '/api/tag/<string:tag_type>/<int:tag_id>')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = request.get_json()
    username = form.get("username")
    password = form.get("password")
    user = User.query.filter_by(username=username).first()
    if not user:
        raise DataError(status_code=404)
    if check_password_hash(pwhash=user.password, password=password):
        expire_time = datetime.timedelta(days=1)
        access_token = create_access_token(
            identity=username, expires_delta=expire_time)
        return {'access_token': access_token}, 200
    else:
        raise LogicError(status_code=400, error_code="USER005",
                         error_msg="Either username or password is incorrect")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5500')

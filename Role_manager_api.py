from flask import request
from flask_restful import Resource, fields, marshal_with

from custom_error import DataError, LogicError
from model import Staff, Subject_Tag, User, db


class Role_api(Resource):
    '''API code for Staff Table'''

    output = {"user_id": fields.Integer, "ticket_id": fields.Integer,
              "title": fields.String, "description": fields.String,
              "isFAQ": fields.Boolean, 'ticket_status': fields.String}

    @marshal_with(output)
    def get(self):
        pass

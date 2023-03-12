from flask import request, jsonify
from app import api
from flask_restful import fields, marshal_with, reqparse, Resource
from model import User,db, Staff, Secondary_Tag,Subject_Tag,Ticket, Table_likes, Response

from custom_error import DataError, LogicError

create_ticket_parser = reqparse.RequestParser()
create_ticket_parser.add_argument('title', type=str, required=True)
create_ticket_parser.add_argument('description', type=str, required=True)

update_ticket_parser = reqparse.RequestParser()
update_ticket_parser.add_argument('action', type=str, required=True)


class Ticket_manager_api(Resource):
    '''API code for Ticket Manager'''

    ticket_output={"ticket_id":fields.Integer,
            "title":fields.String,
            "description":fields.String,
            "isFAQ":fields.Boolean,
            "ticket_status":fields.String,
            }
    @marshal_with(ticket_output)
    def put(self,ticket_id:int):
        '''Modifies the ticket details'''
        ticket_obj = Ticket.query.filter_by(ticket_id=ticket_id).first()
        if not ticket_obj:
            return{'status':False,'error_message':'Ticket not found'},401
        form= request.get_json()
        
        args = update_ticket_parser.parse_args()
        action = args.get('action',None)
        if action=='faq':
            ticket_obj.isFAQ=True
        elif action=='resolved':
            ticket_obj.ticket_status='resolved'
        else:
            like_flag=False
            for like in ticket_obj.likes:
                if like.user_id==user_id:
                  db.session.delete(like)
                  like_flag=True
            if  not like_flag:
                obj=Table_likes(ticket_id=ticket_obj.ticket_id,user_id=user_id)
                db.session.add(obj)
        db.session.commit()
        return ticket_obj, 200
    
    @marshal_with(ticket_output)
    def post(self,tag_id:int):
        '''Creates a new ticket for a subject'''
        args = create_ticket_parser.parse_args()
        title=args.get('title',None)
        desc=args.get('description',None)
        user_id=User.get_id()
        tag_relations=Tag_relation.query.filter_by(tag_id=tag_id).all()
        for relation in tag_relations:
            ticket_obj=Ticket.query.filter_by(ticket_id=relation.ticket_id).first()
            if ticket_obj.title.lower()==title.lower():
                raise LogicError(status_code=500, error_code="TICKET001",
                                 error_msg="Title should be unique")
        
        ticket_obj=Ticket(title=title,description=desc,user_id=user_id)
        db.session.add(ticket_obj)
        db.session.commit()
        return ticket_obj,200

    def delete(self,ticket_id:int):
        '''Deletes the ticket-power given only to admin'''
        ticket_obj=  Ticket.query.filter_by(ticket_id=ticket_id).first()
        if not ticket_obj:
            raise DataError(status_code=404)
        db.session.delete(ticket_obj)
        db.session.commit()
        return '', 200
        


api.add_resource(Ticket_manager_api, '/api/subject/ticket/<int:ticket_id>','/api/subject/ticket/<int:tag_id>')
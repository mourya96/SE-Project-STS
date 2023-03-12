from flask import request, jsonify
from app import api
from flask_restful import fields, marshal_with, reqparse, Resource
from model import User,db, Staff, Secondary_Tag,Subject_Tag,Ticket, Table_likes, Response

from custom_error import DataError, LogicError

class Ticket_api(Resource):
    '''API code for Ticket Manager'''

    ticket_output={"ticket_id":fields.Integer,
            "title":fields.String,
            "description":fields.String,
            "isFAQ":fields.Boolean,
            "ticket_status":fields.String,
            "likes":fields.Integer(attribute=lambda x: len(x.likes))
            }
    @marshal_with(ticket_output)
    def put(self,ticket_id:int):
        '''Modifies the ticket details'''
        ticket_obj = Ticket.query.filter_by(ticket_id=ticket_id).first()
        if not ticket_obj:
            return DataError(status_code=404)
        
        form= request.get_json()
        
        #Checking action from form data
        if form.get("action") is None or form.get("user_id") is None:
            raise LogicError(status_code=400, error_code="TICKET001",
                             error_msg="Either of the form data is missing")
        
        user_id=form.get("user_id")
        
        #Changes in database based on action variable from form
        if form.get("action")=='faq':
            ticket_obj.isFAQ=True
        
        elif form.get("action")=='like':
            for like in ticket_obj.likes:
                if like.user_id==user_id:
                  db.session.delete(like)
                  break
            
            else:
                obj=Table_likes(ticket_id=ticket_obj.ticket_id,user_id=user_id)
                db.session.add(obj)
        
        db.session.commit()
        return ticket_obj, 200
    
    @marshal_with(ticket_output)
    def post(self,subject_name:str):
        '''Creates a new ticket for a subject'''
        
        subject= Subject_Tag.query.filter_by(subject_name=subject_name).first()
        if subject is None:
            raise DataError(status_code=404)
        
        #Getting form data
        form = request.get_json()
        title= form.get("title")
        desc=form.get("description")
        sec=form.get("secondary_tag")
        user_id=form.get("user_id")
        form_data=[title,desc,sec,user_id]

        #Checking if all the form data is filled up
        if None in form_data:
            raise LogicError(status_code=400,error_code="TICKET002", error_msg="Some form data is missing")
        
        #Checking if secondary tag is present in Secondary Tag class
        sec_obj= Secondary_Tag.query.filter_by(sec_tag_name=sec).first()
        if sec_obj is None:
            raise LogicError(status_code=400,error_code="TICKET003", error_msg="secondary tag selected is not available")
        
        #Creating ticket obj and committing to database
        ticket_obj=Ticket(user_id=user_id,title=title, description=desc, subject_name=subject_name, sec_name=sec)
        db.session.add(ticket_obj)
        db.session.commit()
        return ticket_obj,201

    def delete(self,ticket_id:int):
        '''Deletes the ticket-power given only to admin'''
        ticket_obj=  Ticket.query.filter_by(ticket_id=ticket_id).first()
        if not ticket_obj:
            raise DataError(status_code=404)
        db.session.delete(ticket_obj)
        db.session.commit()
        return '', 200
        



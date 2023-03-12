from flask import request
from flask_restful import Resource, fields, marshal_with

from custom_error import DataError, LogicError
from model import Secondary_Tag, Subject_Tag, db


class Tag_api(Resource):
    '''API code for Ticket Manager'''

    tag_output = {"subject_id": fields.Integer, "subject_name": fields.String,
                  "sec_id": fields.Integer(attribute='sec_tag_id'),
                  "sec_name": fields.String(attribute='sec_tag_name')}

    @marshal_with(tag_output)
    def get(self, tag_type: str, tag_id: int = None):
        '''Getting the tag details'''

        if tag_type == 'subject':
            if tag_id  is None:
                tags = Subject_Tag.query.all()
            else:
                tags= Subject_Tag.query.filter_by(subject_id=tag_id).first()
        elif tag_type == 'secondary':
            if tag_id is None:
                tags = Secondary_Tag.query.all()
            else:
                tags= Secondary_Tag.query.filter_by(sec_tag_id=tag_id).first()

        if not tags:    
            raise DataError(status_code=404)

        return tags, 200

    @marshal_with(tag_output)
    def put(self, tag_type:str):
        '''Modifies the tag details'''

        # Getting form data
        form = request.get_json()
        tag_name = form.get("tag_name")
        tag_id = int(form.get("tag_id"))


        # Checking if tag_name is non-empty
        if tag_name is None or type(tag_name) !=str or len(tag_name)==0:
            raise LogicError(status_code=400, error_code="TAG001",
                             error_msg="Tag_name should be non-empty string")
        

         # Checking type of tag and editing the tag_name subsequently
        tag_obj = None
        if tag_type == 'subject':
            
            #Checking if the subject exists with the given tag_id
            tag_obj = Subject_Tag.query.filter_by(subject_id=tag_id).first()

            #Checking if the new subject name exists in table
            obj=Subject_Tag.query.filter_by(subject_name=tag_name).first()
            if not tag_obj:
                raise DataError(status_code=404)
            elif obj:
                raise LogicError(status_code=400,
                                 error_code='TAG002',
                                 error_msg='Subject_name already exists')
            tag_obj.subject_name = tag_name
        elif tag_type == 'secondary':
            tag_obj = Secondary_Tag.query.filter_by(sec_tag_id=tag_id).first()

            #Checking if the new subject name exists in table
            obj=Secondary_Tag.query.filter_by(sec_tag_name=tag_name).first()

            if not tag_obj:
                raise DataError(status_code=404)
            elif obj:
                raise LogicError(status_code=400,
                                 error_code='TAG003',
                                 error_msg='Secondary tag name already exists')
            tag_obj.sec_tag_name = tag_name

        db.session.commit()
        return tag_obj, 202

    @marshal_with(tag_output)
    def post(self, tag_type:str):
        '''Creates a new tag based on tag type'''

        # Getting form data
        form = request.get_json()
        tag_name = form.get("tag_name")


        # Checking if all the tag_name is non-empty string
        if tag_name is None or type(tag_name) !=str or len(tag_name)==0:
            raise LogicError(status_code=400, error_code="TAG001",
                             error_msg="Tag_name should be non-empty string")

        # Checking type of tag and making a tag object subsequently
        tag_obj = None
        if tag_type == 'subject':
            tag_obj = Subject_Tag.query.filter_by(
                subject_name=tag_name).first()
            if tag_obj:
                raise LogicError(status_code=400,
                                 error_code='TAG002',
                                 error_msg='Subject_name already exists.')
            tag_obj = Subject_Tag(subject_name=tag_name)
        elif tag_type == 'secondary':
            tag_obj = Secondary_Tag.query.filter_by(
                sec_tag_name=tag_name).first()
            if tag_obj:
                raise LogicError(status_code=400,
                                 error_code='TAG003',
                                 error_msg='Secondary tag name already exists.')
            tag_obj = Secondary_Tag(sec_tag_name=tag_name)

        # committing to database
        if tag_obj:
            db.session.add(tag_obj)
            db.session.commit()
            return tag_obj, 201

    def delete(self, sec_tag_id: int):
        '''Deletes the tag-power given only to admin'''
        tag_obj = Secondary_Tag.query.filter_by(sec_tag_id=sec_tag_id).first()
        if not tag_obj:
            raise DataError(status_code=404)
        db.session.delete(tag_obj)
        db.session.commit()
        return '', 200

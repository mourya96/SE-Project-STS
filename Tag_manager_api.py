from flask import request
from flask_restful import Resource, fields, marshal_with

from custom_error import DataError, LogicError
from model import Secondary_Tag, Subject_Tag, db


class Tag_api(Resource):
    '''API code for Ticket Manager'''

    tag_output = {"subject_id": fields.Integer(default=-1), "subject_name": fields.String,
                  "sec_id": fields.Integer(attribute='sec_tag_id'),
                  "sec_name": fields.String(attribute='sec_tag_name')}

    @marshal_with(tag_output)
    def get(self, tag_type: str):
        '''Getting the tag details'''
        if tag_type == 'subject':
            tags = Subject_Tag.query.all()
        elif tag_type == 'secondary':
            tags = Secondary_Tag.query.all()
        else:
            raise DataError(status_code=404)

        return tags, 200

    @marshal_with(tag_output)
    def put(self):
        '''Modifies the tag details'''

        # Getting form data
        form = request.get_json()
        tag_type = form.get("tag_type")
        tag_name = form.get("tag_name")
        tag_id = int(form.get("tag_id"))

        form_data = [tag_type, tag_name]

        # Checking if all the form data is filled up
        if None in form_data:
            raise LogicError(status_code=400, error_code="TAG006",
                             error_msg="Some form data is missing")

        # Checking the type of the data in form
        for data in form_data:
            if type(data) != str or len(data) == 0:
                raise LogicError(status_code=400,
                                 error_code='TAG007',
                                 error_msg='Tag_type or Tag_name should be non-empty string')

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
                                 error_code='TAG008',
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
                                 error_code='TAG009',
                                 error_msg='Secondary tag name already exists')
            tag_obj.sec_tag_name = tag_name
        else:
            raise LogicError(status_code=400,
                             error_code='TAG005',
                             error_msg='The tag is not edited as tag_type value should either be subject or secondary ')

        db.session.commit()
        return tag_obj, 202

    @marshal_with(tag_output)
    def post(self):
        '''Creates a new tag based on tag type'''

        # Getting form data
        form = request.get_json()
        tag_type = form.get("tag_type")
        tag_name = form.get("tag_name")

        form_data = [tag_type, tag_name]

        # Checking if all the form data is filled up
        if None in form_data:
            raise LogicError(status_code=400, error_code="TAG001",
                             error_msg="Some form data is missing")

        # Checking the type of the data in form
        for data in form_data:
            if type(data) != str:
                raise LogicError(status_code=400,
                                 error_code='TAG002',
                                 error_msg='The form data should be in string format')

        # Checking type of tag and making a tag object subsequently
        tag_obj = None
        if tag_type == 'subject':
            tag_obj = Subject_Tag.query.filter_by(
                subject_name=tag_name).first()
            if tag_obj:
                raise LogicError(status_code=400,
                                 error_code='TAG003',
                                 error_msg='The subject already exists.You cannot create duplicate subject')
            tag_obj = Subject_Tag(subject_name=tag_name)
        elif tag_type == 'secondary':
            tag_obj = Secondary_Tag.query.filter_by(
                sec_tag_name=tag_name).first()
            if tag_obj:
                raise LogicError(status_code=400,
                                 error_code='TAG004',
                                 error_msg='The secondary tag already exists.You cannot create duplicate secondary tag')
            tag_obj = Secondary_Tag(sec_tag_name=tag_name)

        else:
            raise LogicError(status_code=400,
                             error_code='TAG005',
                             error_msg='The tag is not created as tag_type value should either be subject or secondary ')

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

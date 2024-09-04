from flask import request
from flask_restx import Resource, fields, Namespace
from database import db
from models import Topic
from datetime import time

api = Namespace('topics', description='Topics related operations')

mockTopic = []

class TimeFormat(fields.Raw):
    def format(self, value):
        return time.strftime(value, "%H:%M")
    
## Topic API domains
topicRequest = api.model('topic', {
    'UserID': fields.String(required=True, description="User ID"),
    'Title': fields.String(required=True, description='Title of your topic'),
    'Descriptions': fields.String(required=True, description='descriptions of your topic')
})

topicResponse = api.model('topic_response', {
    'Title': fields.String(required=True, description='Title of your topic'),
    'Descriptions': fields.String(required=True, description='descriptions of your topic'),
    'Create_at': TimeFormat(required=True, descriptions="date time the topic is created", default='HH:MM'),
    'Update_at': TimeFormat(required=True, descriptions="date time the topic is updated", default='HH:MM')
})


## multiple topics list, and topic create
@api.route('/')
class Topics(Resource): 


    @api.response(200, 'Success', [topicResponse])
    def get(self): 
        topics = db.session.query(Topic).all()

        # 將每個 Topic 物件轉換為字典格式，並格式化時間
        mockTopic = list(map(lambda t: {
            'Title': t.title,
            'Descriptions': t.description,
            'Create_at': t.created_at.strftime('%H:%M') if t.created_at else None,
            'Update_at': t.updated_at.strftime('%H:%M') if t.updated_at else None
        }, topics))

        return mockTopic, 200
    
    @api.expect(topicRequest)
    @api.response(201, 'Topic create success')
    def post(self): 
        newTopic = request.json

        topicToAdd = Topic(member_id=newTopic['UserID'], \
                        title=newTopic['Title'], \
                        description=newTopic['Descriptions'])
        
        db.session.add(topicToAdd)
        db.session.commit()
        return {'message': 'Topic create success'}, 201

# Pass id to routes    
@api.route('/<int:id>')
class SingleTopic (Resource): 

    @api.response(200, 'Success', topicResponse)
    @api.response(404, 'Topic not found')
    def get(self, id): 
        if id < len(mockTopic):
            return mockTopic[id], 200
        else: 
            return {'message': 'topic not found'}, 404
    
    @api.expect(topicRequest)
    @api.response(200, 'Topic updated successfully',topicResponse)
    @api.response(404, 'Topic not found')
    def put(self, id):
        if id < len(mockTopic):
            modified_topic = request.json
            mockTopic[id] = modified_topic
            return {'message': 'Topic updated successfully'}, 200 
        else: 
            return {'message': 'Topic not found'}, 404
    
    @api.response(200, 'Topic deleted successfully')
    @api.response(404, 'Topic not found')
    def delete(self, id):
        if id < len(mockTopic):
            mockTopic.pop(id)
            return {'message': 'Topic deleted successfully'}, 200
        else:
            return {'message': 'Topic not found'}, 404


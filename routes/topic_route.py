from flask import request
from flask_restx import Resource, fields, Namespace
from database import db
from models import Topic
from datetime import time, datetime

api = Namespace('topics', description='Topics related operations')

class TimeFormat(fields.Raw):
    def format(self, value):
        # 確保 value 是 datetime 對象，若是時間戳，可用 datetime.fromtimestamp 轉換
#        if isinstance(value, (int, float)):
            # 將 Unix 時間戳轉換為 datetime 對象
        value = datetime.fromtimestamp(value)
        
        # 格式化為 yyyy/MM/dd HH:mm:ss
        return value.strftime("%Y/%m/%d %H:%M:%S")
    
## Topic API domains
topicRequest = api.model('topic', {
    'UserID': fields.String(required=True, description="User ID"),
    'Title': fields.String(required=True, description='Title of your topic'),
    'Descriptions': fields.String(required=True, description='descriptions of your topic')
})

topicResponse = api.model('topic_response', {
    'Title': fields.String(required=True, description='Title of your topic'),
    'Descriptions': fields.String(required=True, description='descriptions of your topic'),
    'Create_at': TimeFormat(readonly=True, required=True, descriptions="date time the topic is created", default='HH:MM'),
    'Update_at': TimeFormat(readonly=True, required=True, descriptions="date time the topic is updated", default='HH:MM')
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
            'Create_at': t.created_at,# if t.created_at else None,  # 直接用 Unix timestamp
            'Update_at': t.updated_at #if t.updated_at else None  # 直接用 Unix timestamp
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
        
        oneTopic = Topic.query.filter_by(id = id).first()
        if oneTopic :
            response = {
                'Title': oneTopic.title,
                'Descriptions': oneTopic.description,
                'Create_at': oneTopic.created_at, #if oneTopic.created_at else None,  # 直接用 Unix timestamp
                'Update_at': oneTopic.updated_at #if oneTopic.updated_at else None  # 直接用 Unix timestamp
            }
            return response, 200
        else: 
            return {'message': 'topic not found'}, 404
    
    @api.expect(topicRequest)
    @api.response(200, 'Topic updated successfully',topicResponse)
    @api.response(404, 'Topic not found')
    def put(self, id):
        oneTopic = Topic.query.filter_by(id = id).first()

        if oneTopic:
            modified_topic = request.json
            oneTopic.title = modified_topic['Title']
            oneTopic.description = modified_topic['Descriptions']
#            oneTopic.updated_at = .utcnow()
            db.session.commit()
            return {'message': 'Topic updated successfully'}, 200 
        else: 
            return {'message': 'Topic not found'}, 404
    
    @api.response(200, 'Topic deleted successfully')
    @api.response(404, 'Topic not found')
    def delete(self, id):
        topicDelete = Topic.query.filter_by(id = id).delete()
        
        if topicDelete > 0:
            db.session.commit()
            return {'message': 'Topic deleted successfully'}, 200
        else:
            return {'message': 'Topic not found'}, 404


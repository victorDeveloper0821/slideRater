from flask import request
from flask_restx import Resource, fields, Namespace

api = Namespace('topics', description='Topics related operations')

mockTopic = []

## Topic API domains
topicMdl = api.model('topic', {
    'Title': fields.String(required=True, description='Title of your topic'),
    'Descriptions': fields.String(required=True, description='descriptions of your topic')
})

## multiple topics list, and topic create
@api.route('/')
class Topics(Resource): 

    @api.response(200, 'Success', [topicMdl])
    def get(self): 
        return mockTopic, 200
    
    @api.expect(topicMdl)
    @api.response(201, 'Topic create success')
    def post(self): 
        newTopic = request.json
        mockTopic.append(newTopic)
        return {'message': 'Topic create success'}, 201

# Pass id to routes    
@api.route('/<int:id>')
class SingleTopic (Resource): 

    @api.response(200, 'Success', topicMdl)
    @api.response(404, 'Topic not found')
    def get(self, id): 
        if id < len(mockTopic):
            return mockTopic[id], 200
        else: 
            return {'message': 'topic not found'}, 404
    
    @api.expect(topicMdl)
    @api.response(200, 'Topic updated successfully')
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


from flask import request
from flask_restx import Resource, fields, Namespace

api = Namespace('submissions', description='Submission in Topics related operations', path='/topics')

mockSubmissions = []

# submission API Model
submissionMdl = api.model('Submission', {
    'UserID': fields.Integer(required=True, description='The ID of the user'),
    'TopicID': fields.Integer(required=True, description='The ID of the topic'),
    'Content': fields.String(required=True, description='The content of the submission')
})

@api.route('/<int:topic_id>/submissions')
class Submissions(Resource):

    @api.response(200, 'Success', [submissionMdl])
    def get(self, topic_id):
        topic_submission = [submission for submission in mockSubmissions if submission['TopicID'] == topic_id]
        return topic_submission, 200

    @api.expect(submissionMdl)
    @api.response(201, 'Submission created successfully')
    @api.response(400, 'Validation Error')
    def post(self, topic_id):
        new_submission = request.json
        new_submission['TopicID'] = topic_id
        mockSubmissions.append(new_submission)
        return {'message': 'Submission created successfully', 'data': new_submission}, 201

@api.route('/<int:topic_id>/submission/<int:id>')
class SingleSubmission(Resource):

    @api.response(200, 'Success', submissionMdl)
    @api.response(404, 'Submission not found')
    def get(self, id):
        if id < len(mockSubmissions):
            return mockSubmissions[id], 200
        else:
            return {'message': 'Submission not found'}, 404

    @api.expect(submissionMdl)
    @api.response(200, 'Submission updated successfully')
    @api.response(404, 'Submission not found')
    def put(self, topic_id, id):
        if id < len(mockSubmissions):
            updated_submission = request.json
            updated_submission['TopicID'] = topic_id
            mockSubmissions[id] = updated_submission
            return {'message': 'Submission updated successfully'}, 200
        else:
            return {'message': 'Submission not found'}, 404

    @api.response(200, 'Submission deleted successfully')
    @api.response(404, 'Submission not found')
    def delete(self,topic_id, id):
        if id < len(mockSubmissions) and mockSubmissions[id]['TopicID'] == topic_id:
            mockSubmissions.pop(id)
            return {'message': 'Submission deleted successfully'}, 200
        else:
            return {'message': 'Submission not found'}, 404

from flask import request
from flask_restx import Resource, fields, Namespace

api = Namespace('Submission', description='Submission in Topics related operations')

mockSubmissions = []

# 定義 Submission 的模型
submissionMdl = api.model('Submission', {
    'UserID': fields.Integer(required=True, description='The ID of the user'),
    'TopicID': fields.Integer(required=True, description='The ID of the topic'),
    'Content': fields.String(required=True, description='The content of the submission')
})

@api.route('/submission')
class Submissions(Resource):

    @api.response(200, 'Success', [submissionMdl])
    def get(self):
        return mockSubmissions, 200

    @api.expect(submissionMdl)
    @api.response(201, 'Submission created successfully')
    @api.response(400, 'Validation Error')
    def post(self):
        new_submission = request.json
        mockSubmissions.append(new_submission)
        return {'message': 'Submission created successfully'}, 201

@api.route('/submission/<int:id>')
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
    def put(self, id):
        if id < len(mockSubmissions):
            updated_submission = request.json
            mockSubmissions[id] = updated_submission
            return {'message': 'Submission updated successfully'}, 200
        else:
            return {'message': 'Submission not found'}, 404

    @api.response(200, 'Submission deleted successfully')
    @api.response(404, 'Submission not found')
    def delete(self, id):
        if id < len(mockSubmissions):
            mockSubmissions.pop(id)
            return {'message': 'Submission deleted successfully'}, 200
        else:
            return {'message': 'Submission not found'}, 404

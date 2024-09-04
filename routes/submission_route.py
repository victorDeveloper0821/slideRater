from flask import request, current_app
from flask_restx import Resource, fields, Namespace, reqparse
from werkzeug.datastructures import FileStorage
import os 

api = Namespace('submissions', description='Submission in Topics related operations', path='/topics')

mockSubmissions = []

# submission API Model
submissionMdl = api.model('Submission', {
    'UserID': fields.Integer(required=True, description='The ID of the user'),
    'Filename': fields.String(description='The path of the uploaded file'),
    'UserName': fields.String(description='User who upload the topic'),
    'Status': fields.Integer(required = True, description='Status of the slide submission'),
    'Score': fields.Float(required=False, description='The score of recent slides')
})

# 使用 reqparse upload files
upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', 
                           type=FileStorage, 
                           location='files', 
                           required=True, 
                           help='The file to upload')
upload_parser.add_argument('UserID', 
                           type=int, 
                           required=True, 
                           help='The ID of the user')
@api.route('/<int:topic_id>/submissions')
class Submissions(Resource):
    """ Fetch a topic with all submission records"""

    @api.response(200, 'Success', [submissionMdl])
    def get(self, topic_id):
        """ Get a topic with all submission records"""
        topic_submission = [submission for submission in mockSubmissions if submission['TopicID'] == topic_id]
        return topic_submission, 200

    @api.expect(upload_parser)
    @api.response(201, 'Submission created successfully')
    @api.response(400, 'Validation Error')
    def post(self, topic_id):
        """ Add a topic """
        Folders = current_app.config['UPLOAD_FOLDER']
        args = upload_parser.parse_args()

        # 處理檔案上傳
        uploaded_file = args.get('file')
        if uploaded_file:
            file_path = os.path.join(Folders, uploaded_file.filename)
            uploaded_file.save(file_path)
        else:
            file_path = None

        new_submission = {
            'UserID': args['UserID'],
            'TopicID': topic_id,
            'FilePath': uploaded_file.filename
        }

        mockSubmissions.append(new_submission)
        return {'message': 'Submission created successfully', 'data': new_submission}, 201

@api.route('/<int:topic_id>/submission/<int:id>')
class SingleSubmission(Resource):
    """Get a topic with specific submission"""

    @api.response(200, 'Success', submissionMdl)
    @api.response(404, 'Submission not found')
    def get(self, topic_id, id):
        """Get a submission from a topic"""
        if id < len(mockSubmissions):
            return mockSubmissions[id], 200
        else:
            return {'message': 'Submission not found'}, 404

    @api.expect(upload_parser)
    @api.response(200, 'Submission updated successfully')
    @api.response(404, 'Submission not found')
    def put(self, topic_id, id):
        Folders = current_app.config['UPLOAD_FOLDER']
        if id < len(mockSubmissions):
            args = upload_parser.parse_args()

            # 處理檔案上傳
            uploaded_file = args.get('file')
            if uploaded_file:
                file_path = os.path.join(Folders, uploaded_file.filename)
                uploaded_file.save(file_path)
            else:
                file_path = None

            updated_submission = {
                'UserID': args['UserID'],
                'TopicID': topic_id,
                'Content': args.get('Content', ''),
                'FilePath': uploaded_file.filename
            }

            mockSubmissions[id] = updated_submission
            return {'message': 'Submission updated successfully'}, 200
        else:
            return {'message': 'Submission not found'}, 404

    @api.response(200, 'Submission deleted successfully')
    @api.response(404, 'Submission not found')
    def delete(self, topic_id, id):
        """Delete a submission from a specific topic"""
        if id < len(mockSubmissions) and mockSubmissions[id]['TopicID'] == topic_id:
            mockSubmissions.pop(id)
            return {'message': 'Submission deleted successfully'}, 200
        else:
            return {'message': 'Submission not found'}, 404

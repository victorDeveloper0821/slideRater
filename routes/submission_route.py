from flask import request, current_app
from flask_restx import Resource, fields, Namespace, reqparse
from werkzeug.datastructures import FileStorage
import os 
from models import Topic, Submission
from service import slideService
from sqlalchemy.orm import subqueryload
from database import db

api = Namespace('submissions', description='Submission in Topics related operations', path='/topics')

# 定义 Submission API 模型
submissionMdl = api.model('Submission', {
    'UserID': fields.Integer(required=True, description='The ID of the user'),
    'Filename': fields.String(description='The path of the uploaded file'),
    'UserName': fields.String(description='User who uploaded the topic'),
    'Status': fields.Integer(required=True, description='Status of the submission'),
    'Score': fields.Float(description='The score of the submission')
})

# 使用 reqparse 解析文件上传
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

# 获取所有 submission 的路由
@api.route('/<int:topic_id>/submissions')
class Submissions(Resource):
    """ Fetch all submissions for a specific topic """

    @api.response(200, 'Success', [submissionMdl])
    def get(self, topic_id):
        """ Get all submissions for a specific topic """
        topic = Topic.query.options(subqueryload(Topic.submissions)).filter_by(id=topic_id).first()
        if not topic:
            return {'message': 'Topic not found'}, 404
        
        submissions = [
            {
                #'UserID': submission.user_id,
                'Filename': submission.slides,
                'Status': submission.status,
                'Score': submission.score,
                'UserName': 'User rwar'  # 示例用户名称
            }
            for submission in topic.submissions
        ]

        return submissions, 200 

    @api.expect(upload_parser)
    @api.response(201, 'Submission created successfully')
    @api.response(400, 'Validation Error')
    def post(self, topic_id):
        """ Add a new submission to a topic """
        Folders = current_app.config['UPLOAD_FOLDER']
        args = upload_parser.parse_args()

        # 检查 topic 是否存在
        topic = Topic.query.filter_by(id=topic_id).first()
        if not topic:
            return {'message': 'Topic not found'}, 404

        # 处理文件上传
        uploaded_file = args.get('file')
        if uploaded_file:
            file_path = os.path.join(Folders, uploaded_file.filename)
            uploaded_file.save(file_path)
        else:
            return {'message': 'No file uploaded'}, 400

        # 添加新提交
        new_submission = Submission(
            topic_id=topic_id,
            filename=uploaded_file.filename,
            status=1,  # 默认设置 status
        )
        db.session.add(new_submission)
        db.session.commit()
        
        slideService.extract_pptx_content(file_path, new_submission.id)


        return {'message': 'Submission created successfully'}, 201

# 获取、更新和删除单个 submission 的路由
@api.route('/<int:topic_id>/submission/<int:id>')
class SingleSubmission(Resource):
    """ Manage a specific submission """

    @api.response(200, 'Success', submissionMdl)
    @api.response(404, 'Submission not found')
    def get(self, topic_id, id):
        """ Get a specific submission from a topic """
        submission = Submission.query.filter_by(id=id, topic_id=topic_id).first()
        if not submission:
            return {'message': 'Submission not found'}, 404

        return {
            #'UserID': submission.user_id,
            'Filename': submission.slides,
            'Status': submission.status,
            'Score': submission.score
        }, 200

    @api.expect(upload_parser)
    @api.response(200, 'Submission updated successfully')
    @api.response(404, 'Submission not found')
    def put(self, topic_id, id):
        """ Update a submission """
        submission = Submission.query.filter_by(id=id, topic_id=topic_id).first()
        if not submission:
            return {'message': 'Submission not found'}, 404

        args = upload_parser.parse_args()

        # 更新文件上传
        Folders = current_app.config['UPLOAD_FOLDER']
        uploaded_file = args.get('file')
        if uploaded_file:
            file_path = os.path.join(Folders, uploaded_file.filename)
            uploaded_file.save(file_path)
            submission.slides = uploaded_file.filename

        submission.user_id = args['UserID']
        db.session.commit()

        return {'message': 'Submission updated successfully'}, 200

    @api.response(200, 'Submission deleted successfully')
    @api.response(404, 'Submission not found')
    def delete(self, topic_id, id):
        """ Delete a submission from a specific topic """
        submission = Submission.query.filter_by(id=id, topic_id=topic_id).first()
        if not submission:
            return {'message': 'Submission not found'}, 404

        db.session.delete(submission)
        db.session.commit()

        return {'message': 'Submission deleted successfully'}, 200

from flask import Flask, request
from configuration import swagger_config
from flask_restx import Api, Namespace, Resource, fields
from routes import topics_api, submissions_api

app = Flask(__name__)
api = Api(app, **swagger_config)


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return 'hello'
    
# 將 Controller 的邏輯加到 API 中
api.add_namespace(topics_api, path='/topics')
api.add_namespace(submissions_api, path='/submissions')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=51800, debug=True)
from flask import Flask
from configuration import swagger_config, global_config
from routes import addRoutes
from database import init_extensions, db
from models import member, topic, submission
import os

## initialize app instance
def create_app (env_name):
    # create flask api instance
    app = Flask(__name__)

    # fetch config from env name
    app.config.from_object(global_config[env_name])
    app.config["UPLOAD_FOLDER"] = "/Users/victortsai/uploads/slide_ranker/"
    app.config["ALLOWED_EXTENSIONS"] = {'ppt', 'pptx'}
    
    # define the api endpoints and swagger
    addRoutes(app, swagger_config)
    
    # config db
    init_extensions(app=app)

    return app



if __name__ == '__main__':
    try:
        app = create_app('dev')
        with app.app_context():
            # Check current directory and remove existing db if needed
            print(f"Current directory: {os.getcwd()}")
            if os.path.exists('instance/slide_rater.db'):
                os.remove('instance/slide_rater.db')
            db.create_all()
            print("Database tables created successfully.")
        app.run(host='127.0.0.1', port=51800, debug=True)
    except Exception as e:
        print(f"Error: {e}")
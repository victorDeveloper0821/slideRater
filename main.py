from flask import Flask
from configuration import swagger_config, global_config
from routes import addRoutes
from database import init_extensions, db
from models import member, topic, submission, Slide, BulletPoint
from error import register_error_handlers
from schedular import setup_scheduler
import os

## initialize app instance
def create_app (env_name):
    # create flask api instance
    app = Flask(__name__)

    # fetch config from env name
    app.config.from_object(global_config[env_name])
    
    # define the api endpoints and swagger
    addRoutes(app, swagger_config)
    
    # config db
    init_extensions(app=app)
    
    # Define error handler here
    register_error_handlers(app=app)

    return app



if __name__ == '__main__':
    try:
        app = create_app('dev')
        # 設置調度器
        scheduler = setup_scheduler()
        
        with app.app_context():
            # Check current directory and remove existing db if needed
            db.create_all()
            print("Database tables created successfully.")
            
            scheduler.start()
            print("Scheduler 已啟動")
        
        app.run(host='127.0.0.1', port=51800, debug=True)
    except Exception as e:
        print(f"Error: {e}")
from flask import Flask
from configuration import swagger_config, db_config
from routes import addRoutes
from database import init_extensions, db

## initialize app instance
def create_app (env_name):
    # create flask api instance
    app = Flask(__name__)

    # fetch config from env name
    app.config.from_object(db_config[env_name])
    
    # define the api endpoints and swagger
    addRoutes(app, swagger_config)
    
    # config db
    init_extensions(app=app)

    return app



if __name__ == '__main__':
    try:
        app = create_app('dev')
        with app.app_context():
            db.create_all()
        print("Database tables created successfully.")
        app.run(host='127.0.0.1', port=51800, debug=True)
    except Exception as e:
        print(f"Error: {e}")
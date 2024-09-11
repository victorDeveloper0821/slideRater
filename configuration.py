import os
## here is configuration for flask app.

# swagger api doc configs
swagger_config = {
    'title': 'Your slide Ranking api documents',
    'version': '1.0',
    'description': 'API for help you excellent presentations',
    'doc': '/swagger/'  # Swagger 文檔路徑
}

class Config(object): 
    """Global config for Flask Application"""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///slide_rater.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'slide_rater_secret_key')
    UPLOAD_FOLDER="/Users/victortsai/uploads/slide_ranker/"
    ALLOWED_EXTENSIONS = {'ppt', 'pptx'}
    SCHEDULER_API_ENABLED = True

class DevelopmentConfig(Config):
    """Development env"""
    DEBUG = True

class ProductionConfig(Config):
    """Production env"""
    DEBUG = False

global_config = {
    'dev': DevelopmentConfig,
    'prod':ProductionConfig,
}
import os
## here is configuration for flask app.

# swagger api doc configs
swagger_config = {
    'title': 'Your slide Ranking api documents',
    'version': '1.0',
    'description': 'API for help you excellent presentations',
    'doc': '/swagger/'  # Swagger 文檔路徑
}

# Base config for database
class Config(object): 
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///slide_rater.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'slide_rater_secret_key')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

db_config = {
    'dev': DevelopmentConfig,
    'prod':ProductionConfig,
}
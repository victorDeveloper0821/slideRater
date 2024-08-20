from flask_restx import Api
## get route settings
from .topic_route import api as topics_api
from .submission_route import api as submissions_api

# add url endpoints definitions
def addRoutes(app, config):
    api = Api(app, **config)
    api.add_namespace(topics_api)
    api.add_namespace(submissions_api)
    return api 
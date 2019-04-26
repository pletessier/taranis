import logging

from dynaconf import settings
from flask import Flask, Blueprint

# noinspection PyUnresolvedReferences
from src.python.api.resource.db import *
from src.python.api.resource.health import ns as health_resource
from src.python.api.resource.metrics import ns as metrics_resource
from src.python.api.restplus import api, ns_db

app = Flask(__name__)

logger = logging.getLogger(__name__)


def configure_app(flask_app):
    logger.info('Configure application')
    flask_app.config['SERVER_HOST'] = settings.HOST
    # flask_app.config['SERVER_NAME'] = "{0}:{1}".format(settings.HOST, settings.PORT)
    flask_app.config['SERVER_PORT'] = settings.PORT
    flask_app.config['SCHEMES'] = ['http']
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.SWAGGER.docExpansion
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS.validate
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS.maskSwagger
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS.error404Help


def initialize_app(flask_app):
    logger.info('Initialize application')
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(ns_db)
    api.add_namespace(health_resource)
    api.add_namespace(metrics_resource)
    flask_app.register_blueprint(blueprint)


def main():
    initialize_app(app)
    logger.info('>>>>> Starting %s server at http://%s:%d/api/ <<<<<', settings.APP, settings.HOST, settings.PORT)
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)


if __name__ == "__main__":
    main()

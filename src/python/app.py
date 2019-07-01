import logging
import sys

from dynaconf import settings
from flask import Flask, Blueprint

from resources.grpc_server import GRPCServer
from src.python.resources.health import ns as health_resource
from src.python.resources.metrics import ns as metrics_resource
from src.python.resources.restplus import api

app = Flask(__name__)

logger = logging.getLogger("Taranis")


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
    api.add_namespace(health_resource)
    api.add_namespace(metrics_resource)
    flask_app.register_blueprint(blueprint)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    initialize_app(app)
    logger.info('Starting %s API at http://%s:%d/api/', settings.APP, settings.HOST, settings.PORT)

    GRPCServer().start()
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)


if __name__ == "__main__":
    main()

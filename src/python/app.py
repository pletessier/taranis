# Copyright (C) 2019 Pierre Letessier
# This source code is licensed under the BSD 3 license found in the
# LICENSE file in the root directory of this source tree.

import logging
# noinspection PyUnresolvedReferences
import sys

from flask import Flask, Blueprint

from resources.grpc_server import GRPCServer
from services.taranis_service import TaranisService
from src.python.resources.health import ns as health_resource
from src.python.resources.metrics import ns as metrics_resource
from src.python.resources.restplus import api
from utils.configuration import configuration as config

app = Flask(__name__)

logger = logging.getLogger(config.app)


def configure_app(flask_app):
    logger.info('Configure application')
    flask_app.config['SERVER_HOST'] = config.http.host
    # flask_app.config['SERVER_NAME'] = "{0}:{1}".format(settings.HOST, settings.PORT)
    flask_app.config['SERVER_PORT'] = config.http.port
    flask_app.config['SCHEMES'] = ['http']
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = config.swagger.docExpansion
    flask_app.config['RESTPLUS_VALIDATE'] = config.restplus.validate
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = config.restplus.maskSwagger
    flask_app.config['ERROR_404_HELP'] = config.restplus.error404Help


def initialize_app(flask_app):
    logger.info('Initialize application')
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix=config.http.url_prefix)
    api.init_app(blueprint)
    api.add_namespace(health_resource)
    api.add_namespace(metrics_resource)
    flask_app.register_blueprint(blueprint)


def main():
    logging.basicConfig(stream=eval(config.logs.stream), level=eval("logging.{}".format(config.logs.level)))

    initialize_app(app)
    logger.info('Starting %s API at http://%s:%d/api/', config.app, config.http.host, config.http.port)

    taranis_service = TaranisService(mongo_host=config.db.mongo.host, mongo_port=config.db.mongo.port,
                                     mongo_username=config.db.mongo.username,
                                     mongo_password=config.db.mongo.password,
                                     redis_host=config.db.redis.host, redis_port=config.db.redis.port,
                                     redis_timeout_msecs=config.db.redis.timeout_msecs,
                                     redis_max_reconnects=config.db.redis.max_reconnects,
                                     redis_reconnect_interval_msecs=config.db.redis.reconnect_interval_msecs)

    GRPCServer(taranis_service, listen_address=config.grpc.host, listen_port=config.grpc.port,
               max_workers=config.grpc.max_workers).start()
    app.run(host=config.http.host, port=config.http.port, debug=config.http.debug)


if __name__ == "__main__":
    main()

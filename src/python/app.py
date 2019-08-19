# Copyright (C) 2019 Pierre Letessier
# This source code is licensed under the BSD 3 license found in the
# LICENSE file in the root directory of this source tree.

"""
Main file
"""
import logging
# noinspection PyUnresolvedReferences
import sys

from flask import Flask, Blueprint

from resources.grpc_server import GRPCServer
from resources.health import NS as health_resource
from resources.metrics import NS as metrics_resource
from resources.restplus import API
from services.taranis_service import TaranisService
from utils.configuration import CONFIGURATION as trn_config

APP = Flask(__name__)

LOGGER = logging.getLogger(trn_config.app)


def configure_app(flask_app):
    LOGGER.info('Configure application')
    flask_app.config['SERVER_HOST'] = trn_config.http.host
    # flask_app.config['SERVER_NAME'] = "{0}:{1}".format(settings.HOST, settings.PORT)
    flask_app.config['SERVER_PORT'] = trn_config.http.port
    flask_app.config['SCHEMES'] = ['http']
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = trn_config.swagger.docexpansion
    flask_app.config['RESTPLUS_VALIDATE'] = trn_config.restplus.validate
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = trn_config.restplus.maskswagger
    flask_app.config['ERROR_404_HELP'] = trn_config.restplus.error404help


def initialize_app(flask_app):
    LOGGER.info('Initialize application')
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix=trn_config.http.url_prefix)
    API.init_app(blueprint)
    API.add_namespace(health_resource)
    API.add_namespace(metrics_resource)
    flask_app.register_blueprint(blueprint)


def main():
    logging.basicConfig(stream=eval(trn_config.logs.stream), level=eval("logging.{}".format(trn_config.logs.level)))

    initialize_app(APP)
    LOGGER.info('Starting %s API at http://%s:%d/api/', trn_config.app, trn_config.http.host, trn_config.http.port)

    taranis_service = TaranisService(mongo_host=trn_config.db.mongo.host, mongo_port=trn_config.db.mongo.port,
                                     mongo_username=trn_config.db.mongo.username,
                                     mongo_password=trn_config.db.mongo.password,
                                     redis_host=trn_config.db.redis.host, redis_port=trn_config.db.redis.port,
                                     redis_timeout_msecs=trn_config.db.redis.timeout_msecs,
                                     redis_max_reconnects=trn_config.db.redis.max_reconnects,
                                     redis_reconnect_interval_msecs=trn_config.db.redis.reconnect_interval_msecs)

    GRPCServer(taranis_service, listen_address=trn_config.grpc.host, listen_port=trn_config.grpc.port,
               max_workers=trn_config.grpc.max_workers).start()
    APP.run(host=trn_config.http.host, port=trn_config.http.port, debug=trn_config.http.debug)


if __name__ == "__main__":
    main()

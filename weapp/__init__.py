#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from sanic import Sanic

from config import config


def create_app(config_name):
    app = Sanic(__name__)
    app.config.from_object(config[config_name])

    # blueprint
    register_blueprint(app)
    return app


def register_error_handle(app):
    pass


def register_blueprint(app):
    from weapp.controller import main
    app.register_blueprint(main.bp, url_prefix='/')
    pass

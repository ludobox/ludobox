#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, send_from_directory

statics = Blueprint('static', __name__)

# STATIC FILES
@statics.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('public/js', path)

@statics.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory('public/css', path)

@statics.route('/images/<path:path>')
def serve_images(path):
    return send_from_directory('public/images', path)

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

@statics.route('/fonts/<path:path>')
def serve_fonts(path):
    return send_from_directory('public/fonts', path)

@statics.route('/api/schema/game')
def serve_schema():
    return send_from_directory('model', "game.json")

# lets encrypt
@statics.route('/.well-known/acme-challenge/<token_value>')
def letsencrpyt(tmp):
    with open('.well-known/acme-challenge/{}'.format(token_value)) as f:
        answer = f.readline().strip()
    return answer

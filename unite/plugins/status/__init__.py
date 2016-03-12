#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log

from unite import app
from unite.core import Handled
from unite.core import UniteHttpResponse as UHR

import json

##### ROUTES #####

# GET /status
@app.route('/status', methods=[ 'GET' ])
def get_status():
    return handle_get_status()


##### HANDLERS #####

@Handled()
def handle_get_status():
    maintenance = app.config['UNITE']['maintenance'] \
        if 'maintenance' in app.config['UNITE'] else False
    
    return UHR(body={'status' : 'maintenance' if maintenance else 'online'})


def __event_request_received__(request):
    log.info('Received request: %s' % request)

def __event_request_processed__(request, uhr):
    uhr.body = json.dumps(uhr.body)
    log.info('Processed request: %s\nResponse: %s' % (request, uhr))

def __event_quit__(signum, stack):
    log.info('Shutting down plugin: status')


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
import importlib
import logging as log

from unite.config import CONFIG 

class Unite:
    def __init__(self):
        log.info('Unite! Startup')
    
        CONFIG.configure_logging()
        log.info('Logging configured')
    
        # Load plugins
        for plugin in CONFIG['plugins']:
            log.info('Importing plugin: %s' % plugin)
            importlib.import_module('unite.plugins.%s' % plugin)
            log.info('Import finished: %s' % plugin)
        
        # Initialize celery
        
        # Trigger plugin celery init listeners
    
    def listen(self):
        app.run(host=CONFIG['bind_address'], port=CONFIG['bind_port'])
    
app = flask.Flask(__name__)
app.config['UNITE'] = CONFIG
app.config['UNITE']['version'] = '0.0.1'



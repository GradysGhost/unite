#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask
import importlib
import logging as log
import signal
import sys

from unite.config import CONFIG 

class Unite:
    def __init__(self):
        CONFIG.configure_logging()
        log.info('Unite! Startup...')
        log.info('Logging configured')
    
        self.__config_signals__()
        log.debug('Signal handlers registered')

        # Load plugins
        for plugin in CONFIG['plugins']:
            log.info('Initializing plugin: %s' % plugin)
            importlib.import_module('unite.plugins.%s' % plugin)
            log.info('Done initializing: %s' % plugin)
        
        # Someday we'll initialize celery here
        
        # Trigger plugin celery init listeners

    def __config_signals__(self):
        signal.signal(signal.SIGHUP, self.__quit__)
        signal.signal(signal.SIGTERM, self.__quit__)
        signal.signal(signal.SIGINT, self.__quit__)

    def __quit__(self, signum, stack):
        log.info("Quitting...")
        for plugin in CONFIG['plugins']:
            if '__event_quit__' in dir(eval('plugins.%s' % plugin)):
                func = eval('plugins.%s.__event_quit__' % plugin)
                func(signum, stack)
        sys.exit(0)
    
    def listen(self):
        app.run(host=CONFIG['bind_address'], port=CONFIG['bind_port'])
    
app = flask.Flask(__name__)
app.config['UNITE'] = CONFIG
app.config['UNITE']['VERSION'] = '0.0.1'


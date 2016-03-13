#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import make_response, request

import json
import logging as log
import unite
from unite import app


# Some classes

class DataSource(object):
    '''Represents the basics of any source of data'''
    def __init__(self, scheme, mountpoint):
        self.scheme, self.mountpoint = scheme, mountpoint
        log_obj(self, new=True)

    def __repr__(self):
        return json.dumps({
            'DataSource': {
                'scheme': self.scheme,
                'mountpoint': self.mountpoint
            }
        })


class ResourceNotImplementedError(Exception):
    pass


class Resource(object):
    '''Represents the basics of any kind of resource Unite can work with'''
    def __init__(self, data_source, path, name=None, resource_type=None):
        self.data_source, self.path, self.name, self.resource_type = data_source, path, name, resource_type
        self.mimetype = None
        self.content = None
        self.uri = self.get_uri()
        log_obj(self, new=True)

    def __repr__(self):
        return json.dumps({
            'Resource': {
                'data_source': self.data_source,
                'path': self.path,
                'name': self.name,
                'resource_type': self.resource_type,
                'mimetype': self.mimetype
            }
        })


    def get_uri(self):
        self.uri = '{}://{}{}'.format(
            self.data_source.scheme,
            self.data_source.mountpoint,
            self.path
        )

    def create(self, content):
        raise ResourceNotImplementedError('Function "create(self, content)" not implemented')

    def read(self):
        raise ResourceNotImplementedError('Function "read(self)" not implemented')

    def update(self, content):
        raise ResourceNotImplementedError('Function "update(self, content)" not implemented')

    def delete(self):
        raise ResourceNotImplementedError('Function "delete(self)" not implemented')


class UniteHttpResponse(object):
    '''Data structure for forming responses'''
    def __init__(self, status_code=200, headers={}, body=None):
        self.status_code = status_code
        self.headers = headers
        self.body = body
        log_obj(self, new=True)

    def __repr__(self):
        return json.dumps({
            'UniteHttpResponse': {
                'status_code': self.status_code,
                'headers': self.headers,
                'body': self.body
            }
        })


# Some functions

def form_response(uhr):
    '''Converts a UniteHttpResponse into a Flask response object'''
    log.debug('I\'m forming an HTTP response -- {}'.format(uhr))
    return make_response(uhr.body, uhr.status_code, uhr.headers)

def log_obj(obj, new=False):
    if new:
        log.debug('I created something new -- {}'.format(obj))
    else:
        log.debug('Look at this old thing -- {}'.format(obj))

class Handled(object):
    '''Decorator for request handlers, triggers some events for plugins with listeners'''
    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            for plugin in app.config['UNITE']['plugins']:
                if '__event_request_received__' in dir(eval('unite.plugins.%s' % plugin)):
                    func = eval('unite.plugins.%s.__event_request_received__' % plugin)
                    func(request)

            uhr = f(*args, **kwargs)

            for plugin in app.config['UNITE']['plugins']:
                if '__event_request_processed__' in dir(eval('unite.plugins.%s' % plugin)):
                    func = eval('unite.plugins.%s.__event_request_processed__' % plugin)
                    func(request, uhr)

            return form_response(uhr)

        return wrapped_f


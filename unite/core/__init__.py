#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import make_response, request

import unite
from unite import app


class UniteHttpResponse:
    def __init__(self, status_code=200, headers={}, body=None):
        self.status_code = status_code
        self.headers = headers
        self.body = body


class Handled(object):
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


def form_response(uhr):
    return make_response(uhr.body, uhr.status_code, uhr.headers)


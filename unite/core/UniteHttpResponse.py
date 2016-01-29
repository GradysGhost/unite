#!/usr/bin/env python
# -*- coding: utf-8 -*-

class UniteHttpResponse:
    def __init__(self, status_code=200, headers={}, body=None):
        self.status_code = status_code
        self.headers = headers
        self.body = body

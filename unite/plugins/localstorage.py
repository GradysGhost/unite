#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging as log
import mimetypes
import os

from unite import app
from unite.core import DataSource, Resource, log_obj


class LocalStorageDataSource(DataSource):
    '''Represents a collection of files stored on disk as resources'''
    def __init__(self, scheme, mountpoint, file_root):
        super().__init__(scheme, mountpoint)
        self.file_root = file_root
        log_obj(self, new=True)

    def __repr__(self):
        return json.dumps({
            'LocalStorageDataSource': {
                'scheme': self.scheme,
                'mountpoint': self.mountpoint,
                'file_root': self.file_root
            }
        })


class LocalStorageResource(Resource):
    '''Represents a resource stored on a local disk'''
    def __init__(self, data_source, path, name=None, resource_type='localstorage'):
        super().__init__(path, data_source, name, resource_type)
        self.size = None
        log_obj(self, new=True)

    def __repr__(self):
        return json.dumps({
            'LocalStorageResource': {
                'data_source': self.data_source,
                'path': self.path,
                'name': self.name,
                'resource_type': self.resource_type,
                'mimetype': self.mimetype,
                'uri': self.uri
            }
        })
        
    def read(self):
        filepath = self.data_source.file_root + self.path
        try:
            content = open(filepath), 'r').read()
            self.content = content
            self.mimetype = mimetypes.guess_type(filepath)
            self.uri = self.get_uri()
            self.size = os.stat(filepath).st_size

            suffix = ''
            if os.path.isfile(filepath):
                suffix = 'file'
            elif os.path.isdir(filepath):
                suffix = 'dir'
            elif os.path.islink(filepath):
                suffix = 'link'
            self.resource_type = 'localstorage/' + suffix
            return self.content
        except OSError as err:
            log.warn('Could not open file {}/{} with URI {}://{}/{} for reading. Error: "{}" Stat: {}'.format(
                self.data_source.file_root,
                self.path,
                self.data_source.scheme,
                self.data_source.mountpoint,
                self.path,
                err,
                os.stat(filepath)
            ))
            return None

    def write(self, content):
        filepath = self.data_source.file_root + self.path
        try:
            fd = open(filepath, 'w')
            fd.write(content)
            fd.close()
            return True
        except OSError as err:
            log.warn('Could not open file {}/{} with URI {}://{}/{} for writing. Error: "{}" Stat: {}'.format(
                self.data_source.file_root,
                self.path,
                self.data_source.scheme,
                self.data_source.mountpoint,
                self.path,
                err,
                os.stat(filepath)
            ))
            return False
            
    def create(self, content):
        return self.write(content)

    def update(self, content):
        return self.write(content)

    def delete(self):
        filepath = self.data_source.file_root + self.path
        try:
            os.unlink(filepath)
            return True
        except OSError as err:
            log.warn('Could not delete file {}/{} with URI {}://{}/{}. Error: "{}" Stat: {}'.format(
                self.data_source.file_root,
                self.path,
                self.data_source.scheme,
                self.data_source.mountpoint,
                self.path,
                err,
                os.stat(filepath)
            ))
            return False
        





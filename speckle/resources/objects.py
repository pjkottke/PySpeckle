import json
import hashlib
from speckle.base.resource import ResourceBase
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBase, ResourceBaseSchema
from speckle import objects


NAME = 'objects'
METHODS = ['list', 'create', 'get', 'update',
           'delete', 'comment_get', 'comment_create']


class SpeckleObject:

    def parse_obj(self, data):
        try:
            assert 'type' in data, 'missing key type'
            object_schema = getattr(objects, data['type'])
            return object_schema.SpeckleObject.parse_obj(data)
        except:
            raise, 'Could not parse object :('


class Resource(ResourceBase):
    def __init__(self, session, basepath):
        super().__init__(session, basepath, NAME, METHODS)

        self.method_dict.update({
            'get_bulk': {
                'method': 'POST'
            },
            'set_properties': {
                'method': 'PUT'
            }
        })
           
        self.schema = SpeckleObject

    def get_bulk(self, data):
        return self.make_request('get_bulk', '/getbulk', data)

    def set_properties(self, id, data):
        return self.make_request('set_properties', '/' + id + '/properties', data)

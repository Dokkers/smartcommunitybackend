import json
import os
import shutil

from flask_restful import Resource
from flask_restful import reqparse
from flaskr import BATH_GRAPH_PATH, BATH_SCHEMA_PATH, BATH_DATA_PATH


class ContentAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('modelList', type=dict, action='append')
        self.parser.add_argument('oldName', location='args')
        self.parser.add_argument('newName', location='args')
        self.parser.add_argument('copyName', location='args')
        self.args = self.parser.parse_args()

    def get(self):
        copyName = self.args['copyName']
        if copyName is not None:
            source = BATH_GRAPH_PATH + copyName + ".json"
            target = BATH_GRAPH_PATH + copyName + "(副本).json"
            shutil.copy2(source, target)
            source = BATH_SCHEMA_PATH + copyName + ".json"
            target = BATH_SCHEMA_PATH + copyName + "(副本).json"
            shutil.copy2(source, target)
            return {'msg': 'success'}
        else:
            path = BATH_SCHEMA_PATH + 'SchemaCard.txt'
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data

    def post(self):
        print(self.args['modelList'])
        print(self.args['oldName'])
        print(self.args['newName'])
        path = BATH_SCHEMA_PATH + 'SchemaCard.txt'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.args['modelList'], f, ensure_ascii=False, indent=4)
        oldName = self.args['oldName']
        newName = self.args['newName']
        if oldName is not None:
            source = BATH_GRAPH_PATH + oldName + ".json"
            target = BATH_GRAPH_PATH + newName + ".json"
            os.rename(source, target)
            source = BATH_SCHEMA_PATH + oldName + ".json"
            target = BATH_SCHEMA_PATH + newName + ".json"
            os.rename(source, target)
        return {'msg': 'success'}

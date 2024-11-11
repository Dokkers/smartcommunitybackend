import json

from flask import request
from flask.views import MethodView
from flask_restful import Resource
from flask_restful import reqparse
from flaskr import BATH_GRAPH_PATH, BATH_SCHEMA_PATH, BATH_DATA_PATH


class UserAPI(MethodView):

    def get(self):
        user_id = request.args.get('user_id', None)
        print(user_id)
        return "User: Method:['GET']"

    def post(self):
        # 创建一个新用户
        pass


class SchemaAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('cells', type=dict, action='append')
        self.parser.add_argument('name', location='args')
        self.args = self.parser.parse_args()

    def get(self):
        data = []
        path = BATH_GRAPH_PATH + self.args['name'] + '.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return data

    def post(self):
        print(self.args['cells'])
        print(self.args['name'])
        graph_path = BATH_GRAPH_PATH + self.args['name'] + '.json'
        with open(graph_path, 'w', encoding='utf-8') as f:
            json.dump(self.args['cells'], f, ensure_ascii=False, indent=4)
        schema = dict()
        # TODO 待扩展，版本号等
        schema['version'] = 0
        schema['graphName'] = self.args['name']
        schema['nodes'] = []
        schema['edges'] = []
        cells = self.args['cells']
        for cell in cells:
            if cell['shape'] != 'edge':
                schema['nodes'].append(cell['data'])
            else:
                schema['edges'].append(cell['data'])
        schema_path = BATH_SCHEMA_PATH + self.args['name'] + '.json'
        with open(schema_path, 'w', encoding='utf-8') as f:
            json.dump(schema, f, ensure_ascii=False, indent=4)
        print(schema)
        return {'msg': 'success'}

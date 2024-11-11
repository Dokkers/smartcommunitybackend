import json

from flask_restful import Resource
from flask_restful import reqparse
from flaskr import BATH_GRAPH_PATH, BATH_SCHEMA_PATH, BATH_DATA_PATH, BATH_PROJECT_PATH
from flaskr.extensions import neo4j


class ProjectAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('projectList', type=dict, action='append')
        self.parser.add_argument('database', location='args')
        self.args = self.parser.parse_args()

    def get(self):
        path = BATH_PROJECT_PATH + 'projects.json'
        print(path)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data

    def post(self):
        print(self.args['projectList'])
        print(self.args['database'])
        database = self.args['database']
        if database is not None:
            try:
                db = neo4j.get_db(None)
                db.run("CREATE DATABASE " + database)
                # neo4j.close_db()
            except Exception as e:
                print(e)
                return {'msg': 'Database already exists or database name must start with an ASCII alphabetic character!'}
        path = BATH_PROJECT_PATH + 'projects.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.args['projectList'], f, ensure_ascii=False, indent=4)
        return {'msg': 'success'}
import json
from flask_restful import Resource
from flask_restful import reqparse
from py2neo import NodeMatcher

from flaskr import BATH_DATA_PATH
from flaskr.extensions import neo4j


class GeoMapAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.args = self.parser.parse_args()

    def get(self):
        data = dict()
        path = r"D:\Store\smartcommunity\tmp\济宁市_市.geojson"
        with open(path, 'r', encoding='utf-8') as f:
            region = json.load(f)
            data['region'] = region
        db = neo4j.get_db(None)
        node_matcher = NodeMatcher(db)  # 节点匹配器
        nodes = node_matcher.match()
        points = []
        for node in nodes:
            if node['TYPE'] != "交通设施服务":
                node['COLOR'] = 0
            else:
                node['COLOR'] = 1
            points.append(dict(node))
        data['points'] = points
        print(data)
        return data

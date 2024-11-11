import json

from flask_restful import Resource
from flask_restful import reqparse
from geopy.distance import geodesic
from py2neo import NodeMatcher, RelationshipMatcher, Relationship, Node

from flaskr.extensions import neo4j


class FigureAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.args = self.parser.parse_args()

    def get(self):
        db = neo4j.get_db(None)
        matcher = NodeMatcher(db)
        all_nodes = matcher.match()
        all_edges = RelationshipMatcher(db).match()
        print(all_nodes.first())
        print(dict(all_edges.first()))
        nodes = [0 for i in range(500)]
        edges = []
        print(len(nodes))
        for node in all_nodes:
            node['id'] = str(node.identity)
            node['size'] = 20
            nodes[node.identity] = dict(node)
        # for i in range(length):
        #     for j in range(i+1, length):
        #         lat1 = nodes[i]['LAT']
        #         lon1 = nodes[i]['LON']
        #         lat2 = nodes[j]['LAT']
        #         lon2 = nodes[j]['LON']
        #         dis = geodesic((lat1, lon1), (lat2, lon2)).km
        #         if dis < 1:
        #             edges.append({"source": nodes[i]['id'], "target": nodes[j]['id']})
        #             nodes[i]['size'] = nodes[i]['size'] + 5
        #             nodes[j]['size'] = nodes[j]['size'] + 5
        for edge in all_edges:
            try:
                nodes[edge.start_node.identity]['size'] = nodes[edge.start_node.identity]['size'] + 5
                nodes[edge.end_node.identity]['size'] = nodes[edge.end_node.identity]['size'] + 5
                edges.append({"source": str(edge.start_node.identity), "target": str(edge.end_node.identity)})
            except Exception as e:
                print(e)
        nodes = [node for node in nodes if node is not 0]
        return {'nodes': nodes, 'edges': edges}

    def post(self):
        pass


class ItemAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        # self.parser.add_argument('cells', type=dict, action='append')
        self.parser.add_argument('type', location='args')
        self.parser.add_argument('label', location='args')
        self.args = self.parser.parse_args()

    def get(self):
        try:
            type = self.args['type']
            label = self.args['label']
            print(type)
            print(label)
            db = neo4j.get_db()
            matcher = NodeMatcher(db)
            node = matcher.match(type).where("_.name=" + "'" + label + "'").first()
            print(node['name'])
            format_data = []
            for key in node.keys():
                format_data.append({'name': key, 'value': node[key]})
            return format_data
        except Exception as e:
            print(e)

    def post(self):
        pass


class QueryAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        # self.parser.add_argument('cells', type=dict, action='append')
        self.parser.add_argument('cypher', location='args')
        self.args = self.parser.parse_args()

    def get(self):
        try:
            cypher = self.args['cypher']
            print(cypher)
            return '{"identity": 0,"labels": [ "organization"],"properties": {"name": "上海新竹园中学"},"elementId": "0"}'
        except Exception as e:
            print(e)

    def post(self):
        pass

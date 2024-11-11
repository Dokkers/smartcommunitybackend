# -*- coding: utf-8 -*-
import json
import os.path
import pandas as pd
from flask_restful import Resource, fields, marshal_with
from flask_restful import reqparse
from py2neo import Node, Transaction, Relationship, NodeMatcher
from werkzeug.datastructures import FileStorage
from flaskr.extensions import neo4j
from flaskr import BATH_GRAPH_PATH, BATH_SCHEMA_PATH, BATH_DATA_PATH


class ModelChooseAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('modelName', type=str, location='args')
        self.parser.add_argument('file', type=FileStorage, location='files')
        self.parser.add_argument('fileName', type=str, location='args')
        self.parser.add_argument('label', type=str, location='args')
        self.parser.add_argument('stKeys', type=dict, action='append')
        self.parser.add_argument('mappingData', type=list, action='append')
        self.parser.add_argument('database', location='args')
        self.args = self.parser.parse_args()

    def get(self):
        try:
            if self.args['modelName'] is not None:
                path = BATH_SCHEMA_PATH + self.args['modelName'] + '.json'
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data
            else:
                filename_list = []
                path = BATH_SCHEMA_PATH + 'SchemaCard.txt'
                with open(path, 'r', encoding='utf-8') as f:
                    cards = json.load(f)
                    for card in cards:
                        filename_list.append(card['name'])
                return filename_list
        except Exception as e:
            print(e)
            return e

    def post(self):
        label = self.args['label']
        file_name = self.args['fileName']
        mapping_data = self.args['mappingData']
        st_keys = self.args['stKeys']
        database = self.args['database']
        print(label)
        print(file_name)
        print(mapping_data)
        print(st_keys)
        # print(database)
        try:
            if mapping_data is not None:
                db = neo4j.get_db(database)
                path = BATH_DATA_PATH + file_name
                df = pd.DataFrame(pd.read_csv(path))
                tx = Transaction(db)
                try:
                    if st_keys[0]['sourceKey'] == '':
                        for index, row in df.iterrows():
                            node = Node(label)
                            node['rType'] = label
                            for i in range(len(mapping_data[0])):
                                node[mapping_data[0][i]] = row[mapping_data[1][i]]
                            db.create(node)
                        # db.commit(tx)
                    else:
                        # TODO 边
                        matcher = NodeMatcher(db)
                        [label1, label2] = label.split(":")[0].split('-')
                        label3 = label.split(":")[1]
                        print(label1)
                        print(label2)
                        print(label3)
                        for index, row in df.iterrows():
                            condition = "_.{}='{}'".format(st_keys[0]['sourceKey'], row[st_keys[0]['fieldId1']])
                            node1 = matcher.match(label1).where(condition).first()
                            condition = "_.{}='{}'".format(st_keys[0]['targetKey'], row[st_keys[0]['fieldId2']])
                            node2 = matcher.match(label2).where(condition).first()
                            edge = Relationship(node1, label3, node2)
                            for i in range(len(mapping_data[0])):
                                edge[mapping_data[0][i]] = row[mapping_data[1][i]]
                            db.create(edge)
                except Exception as e:
                    tx.rollback()
                    raise e
            else:
                return 'failed'
        except Exception as e:
            print(e)
            return 'failed'
        print('success')
        return 'success'


sub_fields = {
    'fieldName': fields.String,
    'sampleData': fields.String
}
resource_fields = {
    'previewData': fields.List(fields.Nested(sub_fields)),
    'fileList': fields.List(fields.String)
}


class DataChooseAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('fileName', type=str, location='args')
        self.args = self.parser.parse_args()

    @marshal_with(resource_fields)
    def get(self):
        try:
            print(self.args['fileName'])
            if self.args['fileName'] is not None:
                path = BATH_DATA_PATH + self.args['fileName']
                with open(path, 'r', encoding='utf-8') as f:
                    df = pd.DataFrame(pd.read_csv(f))
                    df = df.head(1)
                    preview_data = []
                    for column, value in df.items():
                        preview_data.append({
                            'fieldName': column,
                            'sampleData': value[0]
                        })
                    print(preview_data)
                    return {'previewData': preview_data}
            else:
                filename_list = []
                for filename in os.listdir(BATH_DATA_PATH):
                    filename_list.append(filename)
                print(filename_list)
                return {'fileList': filename_list}
        except Exception as e:
            print(e)
            return e

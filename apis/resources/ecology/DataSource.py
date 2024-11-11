import os
import time
import pandas as pd
from flask_restful import Resource, fields, marshal_with
from flask_restful import reqparse
from werkzeug.datastructures import FileStorage
from flaskr.extensions import neo4j
from flaskr import BATH_GRAPH_PATH, BATH_SCHEMA_PATH, BATH_DATA_PATH


class DataSourceAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.args = self.parser.parse_args()

    def get(self):
        filelist = []
        for filename in os.listdir(BATH_DATA_PATH):
            file_path = os.path.join(BATH_DATA_PATH, filename)
            file_stat = os.stat(file_path)
            filelist.append({
                "name": filename,
                "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_stat.st_ctime)),
                "size": str(file_stat.st_size) + 'B'
            })
        return filelist

    def post(self):
        pass


class FileOperationAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('file', type=FileStorage, location='files')
        self.parser.add_argument('fileName', type=str, location='form')
        self.parser.add_argument('delFile', type=str, location='args')
        self.args = self.parser.parse_args()

    def get(self):
        filepath = BATH_DATA_PATH + self.args['delFile']
        os.remove(filepath)
        return {'data': '200', 'msg': "文件删除成功！"}

    def post(self):
        file = self.args['file']
        filename = self.args['fileName']
        if not os.path.exists(BATH_DATA_PATH + filename):
            try:
                if filename.split('.')[1] == 'csv':
                    df = pd.DataFrame(pd.read_csv(file))
                    df = df.dropna(axis=1)
                    df.to_csv(BATH_DATA_PATH + filename)
                else:
                    print('geojson')
                    # df = pd.read_json(file)
                    # df.to_json(BATH_DATA_PATH + filename)
                return {'data': '200', 'msg': "文件上传成功！"}
            except Exception as e:
                print(e)
                return 'failed'
        else:
            return {'data': '305', 'msg': "存在相同文件名！"}

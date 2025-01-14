from apis.resources.ecology.ConMana import ContentAPI
from apis.resources.ecology.DataSource import DataSourceAPI, FileOperationAPI
from apis.resources.ecology.EcologyView import DataChooseAPI, ModelChooseAPI
from apis.resources.ecology.GeomapView import GeoMapAPI
from apis.resources.ecology.ProjectView import ProjectAPI
from apis.resources.ecology.SchemaView import UserAPI, SchemaAPI
from apis.resources.ecology.FigureView import FigureAPI, ItemAPI, QueryAPI
from flaskr import create_app
from flask_restful import Api

app = create_app()
api = Api(app)


def register_api(view, endpoint, url, methods):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, view_func=view_func, methods=methods)


if __name__ == "__main__":
    register_api(UserAPI, 'user_api', '/user/', methods=['GET', 'POST'])
    api.add_resource(SchemaAPI, '/ecology/schema')
    api.add_resource(ModelChooseAPI, '/ecology/model')
    api.add_resource(FigureAPI, '/ecology/figure')
    api.add_resource(ItemAPI, '/ecology/figure/item')
    api.add_resource(QueryAPI, '/ecology/figure/query')
    api.add_resource(DataSourceAPI, '/ecology/data')
    api.add_resource(FileOperationAPI, '/ecology/data/file')
    api.add_resource(DataChooseAPI, '/ecology/files')
    api.add_resource(ContentAPI, '/ecology/content')
    api.add_resource(ProjectAPI, '/ecology/project')
    api.add_resource(GeoMapAPI, '/ecology/geomap')
    app.run(host='0.0.0.0', port=5000)

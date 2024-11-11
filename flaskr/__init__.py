import os
from flask import Flask

BATH_PROJECT_PATH = "D:\Store\smartcommunity\\"
BATH_GRAPH_PATH = "D:\Store\smartcommunity\Graph\\"
BATH_SCHEMA_PATH = "D:\Store\smartcommunity\Schema\\"
BATH_DATA_PATH = "D:\Store\smartcommunity\Data\\"


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        # FLASK_ENV='deployment',
        DEBUG=True,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

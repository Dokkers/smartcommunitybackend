from api.ecology.SchemaView import UserAPI
from flaskr import create_app

app = create_app()


def register_api(view, endpoint, url, methods):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, view_func=view_func, methods=methods)


if __name__ == "__main__":
    register_api(UserAPI, 'user_api', '/user/', methods=['GET', 'POST'])
    app.run()

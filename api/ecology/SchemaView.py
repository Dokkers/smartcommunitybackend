from flask import request
from flask.views import MethodView


class UserAPI(MethodView):

    def get(self):
        user_id = request.args.get('user_id', None)
        print(user_id)
        return "User: Method:['GET']"

    def post(self):
        # 创建一个新用户
        pass


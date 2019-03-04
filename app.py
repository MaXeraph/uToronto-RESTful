from flask import Flask
from flask_restful import Api

from todo import Todo

app = Flask(__name__)
api = Api(app)

api.add_resource(Todo, "/GET/<str:code>")

if __name__ == "__main__":
    app.run()

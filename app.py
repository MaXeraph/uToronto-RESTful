from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from todo import Todo, Root

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

api.add_resource(Todo, "/get/<code>")
api.add_resource(Root,"/")

if __name__ == "__main__":
    app.run()

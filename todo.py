from flask_restful import Resource
import sqlite3
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))

#For accessing the file in a folder contained in the current folder

# Creates or opens a file called uToronto with a SQLite3 DB
db = sqlite3.connect(os.path.join(fileDir, 'data\\uToronto.db'))
cursor = db.cursor()

class Todo(Resource):
    # def get(self, id):
    #     for todo in todos:
    #         if(id == todo["id"]):
    #             return todo, 200
    #     return "Item not found for the id: {}".format(id), 404

    def get(self, code):
        try:
            cursor.execute('''SELECT courseCode, title, hours, summary,
                                    prerecquisites, exclusions, distribution,
                                    breadth, program FROM courses WHERE courseCode=?''', (code,))
            course = cursor.fetchone()
            return course, 200
        except Exception as e:
            # Roll back any change if something goes wrong
            db.rollback()
            return "Item not found for the id: {}".format(id), 404

from flask_restful import Resource
import sqlite3
from backend import attributes
import json

#For accessing the file in a folder contained in the current folder

# Creates or opens a file called uToronto with a SQLite3 DB
db = sqlite3.connect('backend/data/' + attributes.torCourseDB)
cursor = db.cursor()
CourseListDir = open('backend/data/TORCoursesList')
CourseList = []
for line in CourseListDir:
    CourseList.append(line.rstrip())


class Todo(Resource):
    # def get(self, id):
    #     for todo in todos:
    #         if(id == todo["id"]):
    #             return todo, 200
    #     return {"Item not found for the id: {}".format(id)}, 404

    def get(self, code):
        # try:
        print(code)
        if code == "all":
            return json.dumps(CourseList)


        cursor.execute('''SELECT courseCode, title, hours, summary,
                                prerecquisites, exclusions, distribution,
                                breadth, program FROM courses WHERE courseCode=?''', (code,))
        course = cursor.fetchone()

        return course, 200


        # except Exception as e:
        #     # Roll back any change if something goes wrong
        #     db.rollback()
        #     return {"Item not found for the course code: {}".format(code)}, 200

class Root(Resource):
    def get(self):
        return {"recipe": {"publisher": "Closet Cooking", "f2f_url": "http://food2fork.com/view/35382", "ingredients": ["2 jalapeno peppers, cut in half lengthwise and seeded", "2 slices sour dough bread", "1 tablespoon butter, room temperature", "2 tablespoons cream cheese, room temperature", "1/2 cup jack and cheddar cheese, shredded", "1 tablespoon tortilla chips, crumbled\n"], "source_url": "http://www.closetcooking.com/2011/04/jalapeno-popper-grilled-cheese-sandwich.html", "recipe_id": "35382", "image_url": "http://static.food2fork.com/Jalapeno2BPopper2BGrilled2BCheese2BSandwich2B12B500fd186186.jpg", "social_rank": 100.0, "publisher_url": "http://closetcooking.com", "title": "Jalapeno Popper Grilled Cheese Sandwich"}}, 200

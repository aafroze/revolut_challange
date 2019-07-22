from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from datetime import *
import datetime

app = Flask(__name__)
api = Api(app)


TODOS = {
    'afroze': {'dateofBirth': '1986-12-10'},
    'ahmed': {'dateofBirth': '1973-7-9'},
    'andrew': {'dateofBirth': '2018-3-10'},
}

def abort_if_todo_doesnt_exist(username):
    if username not in TODOS:
        abort(404, message="hello user {} doesn't exist".format(username))

def abort_if_dateofBirth_not_valid(dateofBirth):
    if dateofBirth == '':
        abort(404, message="YYY-MM-DD must be a date before todays date")

def abort_if_username_not_alpha(username):
    if username.isalpha() == False:
        abort(404, message="<username> must contains only letters")

def birthday_note(username):
    # Get Today's Date
    today = date.today()
    if username in TODOS:
        if 'dateofBirth' in TODOS[username]:
            dob_str = TODOS.get(username).values()[0]
    # Convert user input into a date
    dob_data = dob_str.split("-")

    dobYear = int(dob_data[0])
    dobMonth = int(dob_data[1])
    dobDay = int(dob_data[2])

    dob = date(dobYear, dobMonth, dobDay)

    # Calculate number of days lived
    numberOfDays = (today - dob).days

    # Convert this into whole years to display the age
    age = numberOfDays // 365

    # Retrieve the day of the week (Monday to Sunday) corresponding to the DoB.
    day = dob.strftime("%A")

    # Calculating the number of days until next birthday
    thisYear = today.year

    nextBirthday = date(thisYear, dobMonth, dobDay)
    if today < nextBirthday:
        gap = (nextBirthday - today).days
        msg="Hello "+username+"! Your birhday is in " + str(gap) + " days."
    elif today == nextBirthday:
        msg="Hello "+username+"! Happy Birthday!"
    else:
        nextBirthday = date(thisYear + 1, dobMonth, dobDay)
        gap = (nextBirthday - today).days
        msg="Hello "+username+"! Your birthday is in " + str(gap) + " days."
    TODOS[username].update({"message":msg})
    print msg
parser = reqparse.RequestParser()
parser.add_argument('dateofBirth')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, username):
        abort_if_todo_doesnt_exist(username)
        birthday_note(username)
        return  TODOS[username],200

    def delete(self, username):
        abort_if_todo_doesnt_exist(username)
        del TODOS[username]
        return '', 204

    def put(self, username):
        args = parser.parse_args()
        abort_if_dateofBirth_not_valid(args['dateofBirth'])
        abort_if_username_not_alpha(username)
        task = {'dateofBirth': args['dateofBirth']}
        TODOS[username] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self,username):
        args = parser.parse_args()
        abort_if_dateofBirth_not_valid(args['dateofBirth'])
        abort_if_username_not_alpha(username)
        TODOS[username] = {'dateofBirth': args['dateofBirth']}
        return TODOS[username], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/hello')
api.add_resource(Todo, '/hello/<username>')


if __name__ == '__main__':
    app.run(debug=True)
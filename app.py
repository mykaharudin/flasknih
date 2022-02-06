from typing_extensions import Required
from flask import Flask, app, request, jsonify, make_response
from flask.globals import session
from flask.json import dump
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/todo'
db = SQLAlchemy(app)

class Todo(db.Model):
    _tablesname_="todos"
    id = db.Column(db.integer, primary_key=True)
    title = db.Column(db.String(20))
    todo_description = db.Column(db.String(100))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, title, todo_description):
        self.title = title
        self.todo_description = todo_description
    
    def _repr_(self):
        return f"{self.id}"

    class TodoSchema(ModelSchema):
        class Meta(ModelSchema.meta):
            model =Todo
            sqla_session = db.session
            id = fields.Number(dump_only=True)
            title = fields.String(Required=True)
            todo_description = fields.String(required=True)

    @app.route('/api/v1/todo,',methods=['POST'])
    def create_todo():
        data = request.get_json()
        todo_schema = TodoSchema()
        todo = todo_schema.load(data)
        result = todo_schema.dump(todo.create())
        return make_response(jsonify({"todo":result}),200)

    @app.route('/api/v1/todo',method=['GET'])
    def index():
        get_todos = Todo.query.all()
        todo_schema = TodoSchema(many=True)
        todos = todo_schema.dump(get_todos)
        return make_response(jsonify({"todos":todos}))

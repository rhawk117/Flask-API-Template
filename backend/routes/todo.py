from flask import Blueprint, request, jsonify, current_app, Response
from models.todo import Todo
from models.user import User
from utils.db import db
import jwt
from functools import wraps

todo_bp = Blueprint('todo', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs) -> Response:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Bad header, request not authroized'}), 401
        token = auth_header.split(" ")[-1]
        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = data.get('user_id')
            if not user_id:
                return jsonify({'error': 'Request not authorized, bad user id'}), 401
            request.user = User.query.get(user_id)
            if not request.user:
                return jsonify({'error': 'Resource not found, user not found'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated


@todo_bp.route('/', methods=['GET'])
@token_required
def list_todos() -> Response:
    '''returns json list of todos'''
    todos = Todo.query.filter_by(user_id=request.user.id).all()
    response = [{
        'id': t.id,
        'name': t.name,
        'description': t.description,
        'completed': t.completed
    } for t in todos]
    return jsonify(response)


@todo_bp.route('/', methods=['POST'])
@token_required
def create_todo() -> Response:
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    if not name:
        return jsonify({'error': 'Cannot create todo, a name is required'}), 400

    new_todo = Todo(
        name=name,
        description=description,
        completed=False,
        user_id=request.user.id
    )
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message': 'Todo successfully created', 'id': new_todo.id}), 201


@todo_bp.route('/<int:todo_id>', methods=['PUT', 'PATCH'])
@token_required
def update_todo(todo_id) -> Response:
    data = request.get_json()
    todo: Todo = Todo.query.filter_by(
        id=todo_id, user_id=request.user.id).first()
    if not todo:
        return jsonify({'error': 'Error: todo not found'}), 404

    if 'name' in data:
        todo.name = data['name']
    if 'description' in data:
        todo.description = data['description']
    if 'completed' in data:
        todo.completed = data['completed']

    db.session.commit()
    return jsonify({'message': 'Todo successfully updated!'})


@todo_bp.route('/<int:todo_id>', methods=['DELETE'])
@token_required
def delete_todo(todo_id) -> Response:
    todo: Todo = Todo.query.filter_by(
        id=todo_id, user_id=request.user.id).first()
    if not todo:
        return jsonify({'error': 'ToDo not found'}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted'})

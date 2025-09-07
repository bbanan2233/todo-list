from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'todo.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ToDo List</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f0f0;
            padding: 40px;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            max-width: 600px;
            margin: auto;
        }
        form input {
            padding: 10px;
            width: 70%;
            margin-right: 10px;
        }
        form button {
            padding: 10px;
        }
        ul {
            list-style: none;
            padding-left: 0;
        }
        li {
            padding: 8px 0;
            border-bottom: 1px solid #ccc;
        }
        .completed {
            text-decoration: line-through;
            color: gray;
        }
        a {
            margin-left: 10px;
            color: #007BFF;
            text-decoration: none;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>ToDo List</h1>

    <form method="POST" action="{{ url_for('add') }}">
        <input type="text" name="title" placeholder="Введите задачу..." required>
        <button type="submit">Добавить</button>
    </form>

    <ul>
        {% for task in tasks %}
        <li class="{{ 'completed' if task.completed }}">
            {{ task.title }}
            <a href="{{ url_for('complete', task_id=task.id) }}">[✔️]</a>
            <a href="{{ url_for('delete', task_id=task.id) }}">[✖️]</a>
        </li>
        {% endfor %}
    </ul>
</div>
</body>
</html>
'''

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        new_task = Task(title=title)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

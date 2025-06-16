from flask import request, jsonify
from models import Task, Tag
from database import db, app
from datetime import datetime
from jsonschema import validate, ValidationError

# Схемы Валидации
task_schema = {
    "type": "object",
    "required": ["title"],
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "deadline": {"type": "string", "format": "date-time"},
        "completed": {"type": "boolean"},
        "tags": {"type": "array", "items": {"type": "string"}}
    }
}

tag_schema = {
    "type": "object",
    "required": ["name"],
    "properties": {
        "name": {"type": "string"}
    }
}

# ЗАДАЧИ
@app.route('/tasks', methods=['POST'])
def create_task():

    """
        Создаёт новую задачу.

        Принимает JSON с полями:
            - title (обязательное)
            - description (опциональное)
            - deadline (ISO-формат даты, опциональное)
            - completed (булево значение, по умолчанию False)
            - tags (список названий тегов)

        Возвращает созданную задачу в формате JSON со статусом 201 (Created).
    """

    try:
        data = request.get_json()
        validate(instance=data, schema=task_schema)

        if not data.get('title'):
            return jsonify({"Ошибка": "Требуется ввести название задачи"}), 400

        if not data.get('description'):
            return jsonify({"Ошибка": "Требуется ввести описание задачи"}), 400

        if Task.query.filter_by(title=data['title']).first():
            return jsonify({"Ошибка": "Задача с таким названием уже существует"}), 400

        deadline = None
        if data.get('deadline'):
            try:
                deadline = datetime.fromisoformat(data['deadline'])
            except ValueError:
                return jsonify({"Ошибка": "Некорректный формат даты дедлайна"}), 400

        new_task = Task(
            title=data['title'],
            description=data.get('description'),
            deadline=deadline,
            completed=data.get('completed', False)
        )

        if data.get('tags'):
            for tag_name in data['tags']:

                if not tag_name:
                    return jsonify({"Ошибка": "Имя тега не может быть пустым"}), 400

                tag = Tag.query.filter_by(name=tag_name).first() or Tag(name=tag_name)
                db.session.add(tag)
                new_task.tags.append(tag)

        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict()), 201

    except ValidationError as e:
        return jsonify({"Ошибка": "Ошибка валидации", "Сообщение": str(e)}), 400


@app.route('/tasks', methods=['GET'])
def get_tasks():

    """
       Возвращает список всех задач или фильтрует их по тегу.

       Если передан параметр строки запроса ?tag=<имя_тега>,
       возвращаются только задачи с этим тегом.
    """

    tag_filter = request.args.get('tag')
    query = Task.query
    if tag_filter:
        query = query.join(Task.tags).filter(Tag.name == tag_filter)
    tasks = query.all()
    return jsonify([task.to_dict() for task in tasks])


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):

    """
        Возвращает детальную информацию о задаче по её ID.

        Если задача не найдена, возвращается ошибка 404.
    """

    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):

    """
        Обновляет существующую задачу по её ID.

        Позволяет обновить:
            - название
            - описание
            - дедлайн
            - статус выполнения
            - список тегов

        Старые теги заменяются на новые.
    """

    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    try:
        validate(instance=data, schema=task_schema)
    except ValidationError as e:
        return jsonify({"Ошибка": "Ошибка валидации", "Сообщение": str(e)}), 400

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)

    if not data.get('title'):
        return jsonify({"Ошибка": "Требуется ввести название задачи"}), 400

    if not data.get('description'):
        return jsonify({"Ошибка": "Описание задачи не может быть пустым"}), 400

    if 'deadline' in data:
        try:
            task.deadline = datetime.fromisoformat(data['deadline']) if data['deadline'] else None
        except ValueError:
            return jsonify({"Ошибка": "Некорректный формат даты дедлайна"}), 400

    task.completed = data.get('completed', task.completed)

    if 'tags' in data:
        task.tags.clear()
        for tag_name in data['tags']:

            if not tag_name:
                return jsonify({"Ошибка": "Имя тега не может быть пустым"}), 400

            tag = Tag.query.filter_by(name=tag_name).first() or Tag(name=tag_name)
            db.session.add(tag)
            task.tags.append(tag)

    db.session.commit()
    return jsonify(task.to_dict())


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):

    """
        Удаляет задачу по ID.

        Если задача найдена и удалена — возвращается сообщение об успехе.
    """

    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"Сообщение": "Задача удалена"})


# ТЕГИ
@app.route('/tags', methods=['POST'])
def create_tag():

    """
        Создаёт новый тег.

        Принимает JSON с полем name (строка, уникальная).

        Если тег с таким именем уже существует — возвращается ошибка.
    """

    try:
        data = request.get_json()
        name = data.get('name')

        validate(instance=data, schema=tag_schema)

        if not name or name.strip() == "":
            return jsonify({"Ошибка": "Имя тега не может быть пустым"}), 400

        if Tag.query.filter_by(name=data['name']).first():
            return jsonify({"Ошибка": "Тег с таким именем уже существует"}), 400

        new_tag = Tag(name=data['name'])
        db.session.add(new_tag)
        db.session.commit()
        return jsonify(new_tag.to_dict()), 201
    except ValidationError as e:
        return jsonify({"Ошибка": "Ошибка валидации", "Сообщение": str(e)}), 400


@app.route('/tags', methods=['GET'])
def get_tags():

    """
        Возвращает список всех тегов.
    """

    tags = Tag.query.all()
    return jsonify([tag.to_dict() for tag in tags])


@app.route('/tags/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):

    """
        Возвращает информацию о теге по его ID.

        Если тег не найден — возвращается ошибка 404.
    """

    tag = Tag.query.get_or_404(tag_id)
    return jsonify(tag.to_dict())


@app.route('/tags/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):

    """
        Обновляет название тега по его ID.

        Проверяет, чтобы новое имя было уникальным.
    """

    tag = Tag.query.get_or_404(tag_id)
    data = request.get_json()
    name = data.get('name')

    try:
        validate(instance=data, schema=tag_schema)

        if not name or name.strip() == "":
            return jsonify({"Ошибка": "Имя тега не может быть пустым"}), 400

        if Tag.query.filter(Tag.id != tag_id, Tag.name == data['name']).first():
            return jsonify({"Ошибка": "Тег с таким именем уже существует"}), 400

        tag.name = data['name']
        db.session.commit()
        return jsonify(tag.to_dict())
    except ValidationError as e:
        return jsonify({"Ошибка": "Ошибка валидации", "Сообщение": str(e)}), 400


@app.route('/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):

    """
        Удаляет тег по ID.

        Также удаляются связи этого тега с задачами (Many-to-Many).
    """

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return jsonify({"Сообщение": "Тег удален"})


# === Инициализация базы данных ===
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
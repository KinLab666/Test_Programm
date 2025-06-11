from database import db

# Промежуточная таблица Many-to-Many
task_tag_association = db.Table('task_tag',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

# Класс описывающий задачу
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    tags = db.relationship('Tag', secondary=task_tag_association, backref=db.backref('tasks', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "completed": self.completed,
            "tags": [tag.name for tag in self.tags]
        }

# Класс описывающий тег
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}
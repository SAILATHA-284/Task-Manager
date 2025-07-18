from flask_sqlalchemy import SQLAlchemy
from datetime import date

db= SQLAlchemy()

class Task(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    description = db.Column(db.Text,nullable=True)
    priority = db.Column(db.String(10), nullable=False, default='Medium')
    date = db.Column(db.Date, nullable=False, default=date.today)  
    def __lt__(self, other):
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        return priority_order[self.priority] < priority_order[other.priority]
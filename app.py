from flask import Flask, render_template,request,redirect,url_for,flash
from models import db,Task
from structures import TaskL,Undo,TaskSet,PriorityTaskQueue
from datetime import datetime


app=Flask(__name__)
app.secret_key="secretsuper123"
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///tasks.db"
app.config['SQLALCHEMY_TRAC_MODIFICATIONS']=False
db.init_app(app)

task_list=TaskL()
undo_stack= Undo()
task_set= TaskSet()
priority_queue = PriorityTaskQueue()

with app.app_context():
    db.create_all()


def setup():
    task_list.tasks= Task.query.all()
    for t in task_list.tasks:
        task_set.add(t.title)
        
@app.route('/')
@app.route('/')
def index():
    filter_date = request.args.get('date')
    if filter_date:
        tasks = Task.query.filter_by(date=filter_date).all()
    else:
        tasks = Task.query.all()

    priority_queue.clear()
    for task in tasks:
        priority_queue.add(task)

    sorted_tasks = priority_queue.get_all()
    return render_template('index.html', tasks=sorted_tasks)


@app.route('/add',methods=['GET','POST'])
def add_task():
    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        priority = request.form['priority']
        task_date = datetime.strptime(request.form['date'], "%Y-%m-%d").date()
        
        if not task_set.add(title):
            flash("task title must be unique!")
            return redirect(url_for('add_task'))
        task=Task(title=title,description=description,priority=priority,date=task_date)
        db.session.add(task)
        db.session.commit()
        
        task_list.add(task)
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/delete/<int:task_id>')

def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Push task data (not object) to stack before deleting
    undo_stack.push(task)

    db.session.delete(task)
    db.session.commit()

    task_list.remove(task)
    task_set.remove(task.title)
    return redirect(url_for('index'))

@app.route('/undo')
def undo_delete():
    task_data = undo_stack.pop()
    if task_data:
        # Recreate Task from stored data
        restored = Task(title=task_data['title'], description=task_data['description'],priority=task_data['priority'])
        db.session.add(restored)
        db.session.commit()

        task_list.add(restored)
        task_set.add(restored.title)
    return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True)
    
        

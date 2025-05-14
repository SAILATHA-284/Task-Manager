import heapq
class TaskL:
    def __init__(self):
        self.tasks = []

    def add(self, task):
        # Store a simple dict instead of SQLAlchemy model instance
        self.tasks.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority 
        })

    def remove(self, task):
        self.tasks = [t for t in self.tasks if t['id'] != task.id]

    def all(self):
        return self.tasks


# structures.py
class Undo:
    def __init__(self):
        self.stack = []

    def push(self, task):
        # Save only the necessary task data, not the SQLAlchemy object
        self.stack.append({
            'title': task.title,
            'description': task.description,
            'priority': task.priority 
        })

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None


class TaskSet:
    def __init__(self):
        self.task_titles=set()
    def add(self,title):
        if title in self.task_titles:
            return False
        self.task_titles.add(title)
        return True
    def remove(self,title):
        self.task_titles.discard(title)
        
class PriorityTaskQueue:
    def __init__(self):
        self.heap = []

    def _priority_value(self, priority):
        return {"High": 1, "Medium": 2, "Low": 3}.get(priority, 3)

    def add(self, task):
        heapq.heappush(self.heap, (self._priority_value(task.priority), task))

    def get_all(self):
        return [t[1] for t in sorted(self.heap)]

    def clear(self):
        self.heap = []
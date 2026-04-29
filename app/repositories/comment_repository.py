
from datetime import datetime


class CommentRepository:
    def __init__(self):
        self._comments = []
        self._next_id = 1

    def create(self, comment_data: dict) -> dict:
       new_comment = {**comment_data}
       new_comment ["created_at"] = datetime.now()
       new_comment["id"] = self._next_id
       self._comments.append(new_comment)
       self._next_id += 1
       return new_comment
        
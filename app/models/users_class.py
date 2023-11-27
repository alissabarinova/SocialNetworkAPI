import re
import json


class User:
    def __init__(self, user_id, first_name, last_name, email, total_reactions, posts):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions
        self.posts = posts
        self.status = "exists"

    def __lt__(self, other):
        return self.total_reactions < other.total_reactions

    @staticmethod
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def to_dict(self):
        user_posts = json.dumps(
            [
                {
                    "id": p.post_id,
                    "author_id": p.author_id,
                    "text": p.text,
                    "reactions": p.reactions,
                    "status": p.status
                }
                for p in self.posts
            ]
        )

        return dict(
            {
                "id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "total_reactions": self.total_reactions,
                "posts": user_posts,
                "status": self.status,
            }
        )

    def repr(self):
        posts = [
                {
                    "id": p.post_id,
                    "author_id": p.author_id,
                    "text": p.text,
                    "reactions": p.reactions,
                }
                for p in self.posts
            ]
        return(f"<b>ID:  </b>{self.id}  "
               f"<b>Name: </b>{self.first_name} {self.last_name}  "
               f"<b>EMAIL: </b>{self.email}  "
               f"<b>Posts: </b>{posts}  "
               f"<b>Reactions: </b>{self.total_reactions} ")

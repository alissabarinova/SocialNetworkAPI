class Post:
    def __init__(self, post_id, author_id, text, reactions=[]):
        self.post_id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = reactions
        self.status = "exists"

    def __lt__(self, other):
        return len(self.reactions) < len(other.reactions)

    def to_dict(self):
        return dict(
            {
                "id": self.post_id,
                "author_id": self.author_id,
                "text": self.text,
                "reactions": self.reactions,
                "status": self.status,
            }
        )

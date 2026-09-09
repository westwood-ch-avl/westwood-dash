from datetime import datetime

class Ev_Charging_User:

    user_id: int
    created: datetime

    def __init__(self, user_id, created):

        self.user_id = user_id
        self.created = created

    @staticmethod
    def from_dict(source):
        return Ev_Charging_User(
            user_id=source["user_id"],
            created=source["created"]
        )

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "created": self.created
        }

    def generate_doc_key(self):
        
        return str(self.user_id)
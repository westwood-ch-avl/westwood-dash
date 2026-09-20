from datetime import datetime
import dateutil
import os

class Private:

    name: str
    unit: str

    def __init__(self, name: str, unit: str):

        self.name = name
        self.unit = unit

    @staticmethod
    def from_dict(source):
        return Private(source["name"], source["unit"])

    def to_dict(self):
        return {
            "name": self.name, "unit": self.unit
        }

    def generate_doc_key(self, user_id: str):
        return user_id
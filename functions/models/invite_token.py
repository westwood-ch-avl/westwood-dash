from datetime import datetime
import os
import dateutil
from dateutil.relativedelta import relativedelta
from wonderwords import RandomWord

class Invite_Token:

    token: str
    date_created: datetime
    expires: datetime
    assignee: str

    def __init__(self, token:str, date_created:datetime=None, assignee:str=None):

        self.token = token

        if date_created == None:
            date_created = datetime.now().astimezone(dateutil.tz.gettz(os.environ.get("TZ")))

        self.date_created = date_created
        self.assignee = assignee
        self.expires = date_created + relativedelta(days=+2)

    @staticmethod
    def generate_token_text():

        r = RandomWord()
        return r.word(word_min_length=4, word_max_length=4) + "-" + r.word(word_min_length=4, word_max_length=4) + "-" + r.word(word_min_length=4, word_max_length=4)

    def generate_doc_key(self):

        return self.token

    def to_dict(self):
        return {
            "token": self.token,
            "date_created": self.date_created,
            "expires": self.expires,
            "assignee": self.assignee
        }
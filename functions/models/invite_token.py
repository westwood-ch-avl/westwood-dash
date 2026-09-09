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

        self.expires = date_created + relativedelta(days=+2)

    @staticmethod
    def generate_token_text():

        r = RandomWord()
        return r.word(word_min_length=4, word_max_length=4) + "-" + r.word(word_min_length=4, word_max_length=4) + "-" + r.word(word_min_length=4, word_max_length=4)

if __name__ == "__main__":

    r = RandomWord()
    print(r.word(word_min_length=4, word_max_length=4) + "-" + r.word(word_min_length=4, word_max_length=4) + "-" + r.word(word_min_length=4, word_max_length=4))
## NB: For the purposes of firestore, this willl be a subcollection under ev_charging_users...

class Monthly_Total:

    year: int
    month: int
    total_wh: int
    num_sessions: int
    user_id: str

    def __init__(self, year, month, total_wh, num_sessions, user_id):
        self.year = year
        self.month = month
        self.total_wh = total_wh
        self.num_sessions = num_sessions
        self.user_id = user_id

    def generate_doc_key(self):
        return str(self.year) + str(self.month).zfill(2)

    def to_dict(self):
        return {
            "year": self.year,
            "month": self.month,
            "total_wh": self.total_wh,
            "num_sessions": self.num_sessions,
            "user_id": self.user_id
        }

    @staticmethod
    def from_dict(source):
        return Monthly_Total(
            year=source["year"],
            month=source["month"],
            total_wh=source["total_wh"],
            num_sessions=source["num_sessions"],
            user_id=source["user_id"]
        )
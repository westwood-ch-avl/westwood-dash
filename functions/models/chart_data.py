from datetime import datetime

class Chart_Data:

    date_created: datetime
    wh_table: list
    sessions_table: list

    def __init__(self, date_created: datetime, wh_table:list, sessions_table:list):

        self.date_created = date_created
        self.wh_table = wh_table
        self.sessions_table = sessions_table

    def generate_key(self) -> str:

        return "chart_data_" + self.date_created.strftime("%Y-%m")

    def to_dict(self) -> dict:

        return {
            "date_created": self.date_created,
            "wh_table": self.wh_table,
            "sessions_table": self.sessions_table
        }

    @staticmethod
    def from_dict(source):
        return Chart_Data(source["date_created"], source["wh_table"], source["sessions_table"])
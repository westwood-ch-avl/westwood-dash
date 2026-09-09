from dotenv import load_dotenv
import os
import json
import requests
from models.event import Event
from models.ev_charging_user import Ev_Charging_User
from models.invite_token import Invite_Token
from models.monthly_total import Monthly_Total
from models.chart_data import Chart_Data
from event_error_checker import isValidEvent
from datetime import datetime, date, time
import dateutil
from dateutil.relativedelta import relativedelta
import firebase_admin
from firebase_admin import credentials, firestore, auth
import sys
from pprint import pp

def initialize_firebase_service_account() -> firestore.client:

    key_dict = json.loads(os.environ.get("FIREBASE_DICT"))

    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    return db

##TODO edit this auto-generated code as needed. Need to add params too. Also consider baking in a way to use command line to set how far back to pull events.
def get_powerfill_data() -> list:
    url = os.environ.get("POWERFILL_URL")
    user = os.environ.get("POWERFILL_USER")
    password = os.environ.get("POWERFILL_PASSWORD")

    response = requests.get(url, auth=(user, password))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from Powerfill: {response.status_code} - {response.text}")

def build_event_dict_from_powerfill_list(data) -> dict:

    events = {}

    for e in data:

        if isValidEvent(e):
            events[e["id"]] = (Event(e["id"], e["startTimeStamp"], e["stopTimeStamp"], e["startValue"],e["stopValue"], e["userId"], e["chargeBoxId"]))

    return events

def get_ev_users_from_db(db) -> dict:

    ev_users = {}

    docs = db.collection("ev_users").stream()

    for doc in docs:
        ev_users[doc.id] = Ev_Charging_User.from_dict(doc.to_dict())

        print("Found EV User: " + doc.id)

    return ev_users

def post_events_to_db(db, ev_users: dict, events: list, earliest_date_time:datetime=None):

    if isinstance(earliest_date_time, str):
        earliest_date_time = dateutil.parser.parse(earliest_date_time).astimezone(dateutil.tz.gettz(os.environ.get("TZ")))

    bulk_writer = db.bulk_writer()

    bulk_writer.on_write_result(lambda reference, result, bulk_writer: print(f'Saved {reference._document_path}'))

    bulk_writer.on_write_error(lambda bulkwriterfailure, bulk_writer: print(f'Bulk Write Failure: {bulkwriterfailure.message}'))

    for event in events.values():

        if earliest_date_time:

            if event.start_time < earliest_date_time:
                break

        if str(event.user_id) in ev_users:

            continue

        else:

            new_ev_user = Ev_Charging_User(int(event.user_id), datetime.now().astimezone(dateutil.tz.gettz(os.environ.get("TZ"))))

            ev_users[str(event.user_id)] = new_ev_user

            ref = db.collection("ev_users").document(str(event.user_id))
            bulk_writer.set(ref, new_ev_user.to_dict())

        doc_ref = db.collection("ev_users").document(str(event.user_id)).collection("events").document(str(event.id))
        bulk_writer.set(doc_ref, event.to_dict())

    bulk_writer.close()

def get_events_from_local_json() -> dict:

    path = os.environ.get("LOCAL_JSON_DATA")

    data = []

    events = {}

    with open(path, 'r') as f:

        data = json.load(f)

    for e in data:

        if isValidEvent(e):

            events[str(e["id"])] = Event(e["id"], e["startTimestamp"], e["stopTimestamp"], e["startValue"], e["stopValue"], e["userId"], e["chargeBoxId"])

    return events

def do_monthly_total(db, ev_users: dict, specific_date_to_run:date=None):

    print("********\nStarting To Run Monthly Totals\n********")

    ## Figure out the exact start and end of the desired month

    if isinstance(specific_date_to_run, str):

        specific_date_to_run = dateutil.parser.parse(specific_date_to_run).date()

    if specific_date_to_run == None:

        specific_date_to_run = date.today() + relativedelta(days=-3)

    pp("*******\ncalculated specific date: " + specific_date_to_run.isoformat() + "\n*******")

    start_of_month = datetime.combine(specific_date_to_run, time()).astimezone(dateutil.tz.gettz(os.environ.get("TZ")))
    start_of_month = start_of_month + relativedelta(day=1)

    end_of_month = start_of_month + relativedelta(months=+1)

    pp("*******")
    pp("Start of month: " + start_of_month.isoformat())
    pp("End of month: " + end_of_month.isoformat())
    pp("*******")

    ## Get the relevant events
    
    from google.cloud.firestore_v1.base_query import FieldFilter

    query = db.collection_group("events").where(filter=FieldFilter("start_time", ">", start_of_month)).where(filter=FieldFilter("start_time", "<", end_of_month))

    docs = query.stream()

    ## process the events and make the new reports locally

    the_months_events = []

    for doc in docs:

        print("Found an event in the desired month:")
        pp(doc.to_dict())

        the_months_events.append(Event.from_dict(doc.to_dict()))

    for k, v in ev_users.items():

        ev_users[k].new_monthly_report = Monthly_Total(specific_date_to_run.year, specific_date_to_run.month, 0, 0, k)

    for e in the_months_events:

        if str(e.user_id) in ev_users:

            new_wh = int(e.end_wh) - int(e.start_wh)

            ev_users[str(e.user_id)].new_monthly_report.total_wh += new_wh

            ev_users[str(e.user_id)].new_monthly_report.num_sessions +=1

    ## post the new monthly totals.

    bulk_writer = db.bulk_writer()

    bulk_writer.on_write_result(lambda reference, result, bulk_writer: print(f'Saved {reference._document_path}'))

    bulk_writer.on_write_error(lambda bulkwriterfailure, bulk_writer: print(f'Bulk Write Failure: {bulkwriterfailure.message}'))

    for u in ev_users.values():

        new_report_id = u.new_monthly_report.generate_doc_key()

        ref = db.collection("ev_users").document(str(u.user_id)).collection("monthly_totals").document(new_report_id)

        bulk_writer.set(ref, u.new_monthly_report.to_dict())

    bulk_writer.close()

def get_command_line_params() -> dict:

    ... # https://realpython.com/command-line-interfaces-python-argparse/#setting-the-type-of-input-values

    ... #TODO should probably pass in separate numbers for how many days to look back for events vs for monthly reports?

def generate_chart_tables(db, ev_users: dict):

    wh_table = []
    sessions_table = []

    query = db.collection_group("monthly_totals").order_by("year", direction=firestore.Query.DESCENDING).order_by("month", direction=firestore.Query.DESCENDING)

    docs = query.get()

    for k, v in ev_users.items():

        wh_dict = {}
        sessions_dict = {}

        wh_dict["user_id"] = str(k)
        sessions_dict["user_id"] = str(k)

        month = 0

        while month < 16:

            month += 1

            month_to_check = datetime.now().astimezone(dateutil.tz.gettz(os.environ.get("TZ"))) + relativedelta(months=-month)

            month_to_check_year = month_to_check.year
            month_to_check_month = month_to_check.month

            snapshot = None

            for d in docs:

                print("checking...")

                if str(d.to_dict()["year"]) == str(month_to_check_year) and str(d.to_dict()["month"])== str(month_to_check_month) and str(d.to_dict()["user_id"]) == str(k):

                    snapshot = d

                    break

            if snapshot == None:

                wh_dict[month_to_check.strftime("%Y-%m")] = 0
                sessions_dict[month_to_check.strftime("%Y-%m")] = 0

            else:

                print("found a month with numbers.")

                wh_dict[month_to_check.strftime("%Y-%m")] = snapshot.to_dict()["total_wh"]
                sessions_dict[month_to_check.strftime("%Y-%m")] = snapshot.to_dict()["num_sessions"]

        wh_table.append(wh_dict)
        sessions_table.append(sessions_dict)

    pp("********\nwh_table: " + str(wh_table) + "\n********")
    pp("********\nsessions_table: " + str(sessions_table) + "\n********")

    new_chart = Chart_Data(datetime.now().astimezone(dateutil.tz.gettz(os.environ.get("TZ"))), wh_table, sessions_table)

    ref = db.collection("chart_data").document(new_chart.generate_key())
    ref.set(new_chart.to_dict())

def generate_new_tokens(num:int=1) -> list:

    new_tokens = []

    while len(new_tokens) < num:

        new_tokens.append(Invite_Token.generate_token())

    return new_tokens

def create_new_user(email, password, admin=False):

    try:
        user = auth.create_user(
            email=email,
            email_verified=False,
            password=password,
            disabled=False
        )
        print(f"Successfully created new user: {user.uid}")

        if admin==True:

            auth.set_custom_user_claims(user.uid, {'admin':True})

            print("Applied admin role.")
        
    except auth.EmailAlreadyExistsError:
        print("Error: This email address is already in use.")
    except Exception as e:
        print(f"Error creating user: {e}")

def set_working_directory():
    '''Python has a quirk where the working directory can be ambiguous, depending on how script is run in the terminal. This will set the current working directory to wherever the .py script is located.'''
    if os.path.dirname(sys.argv[0]) != "" and os.path.dirname(sys.argv[0]) != "." and os.path.dirname(sys.argv[0]) != None:

        os.chdir(os.path.dirname(sys.argv[0]))

if __name__ == "__main__":

    set_working_directory()

    load_dotenv()

    db = initialize_firebase_service_account()

    generate_chart_tables(db, get_ev_users_from_db(db))

    #ETC ETC
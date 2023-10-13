import os
import threading

import requests
from tinydb import TinyDB, Query
from scripts.bluedart import get_latest_update
from dotenv import load_dotenv
import schedule

load_dotenv(".env")
token = os.getenv("token")

db = TinyDB('data.json')
table = db.table('track_request')


def send_msg_using_requests(chat_id, msg):
    res = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}")
    print(res)


def process_shipment(shipment_number: str, chat_id=None):
    current_status = get_latest_update(shipment_number)
    # if shipment_id already exists then compare the existing value with new value
    existing = table.search(Query().id == shipment_number)
    if not existing:
        if current_status:
            table.insert({'id': shipment_number, 'status': current_status, 'chat_id': chat_id})
            return current_status
        else:
            return "Shipment id not valid"
    else:
        if existing[0]['status'] != current_status:
            table.update({'status': current_status}, Query().id == shipment_number)
            send_msg_using_requests(existing[0]['chat_id'], current_status)
            return current_status
        else:
            return "No new updates"


def check_update():
    for shipment in table.all():
        current_status = process_shipment(shipment['id'])
        print(current_status)
        if current_status != "No new updates":
            send_msg_using_requests(shipment['chat_id'], current_status)


def infinite_loop():
    schedule.every(15).minutes.do(check_update)
    while True:
        schedule.run_pending()


def get_all_shipment():
    print(table.all())
    return table.all()


threading.Thread(target=infinite_loop).start()

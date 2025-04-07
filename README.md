Write readme.md for this github repo in editor. 
File Path : README.md
File Content : # Shipment Tracker Telegram Bot Readme
## Introduction

This is a Python program for a Telegram bot that helps users track shipments using the BlueDart tracking service. The bot responds to user commands to track a shipment and provides real-time updates on the shipment's status. This README provides information on how to set up and use the program.

## Prerequisites
Before using this program, you need to have the following prerequisites:

***Python:*** Make sure you have Python installed on your system. This program was developed using Python 3.7 or later.

***Telegram Bot Token:*** You need to create a Telegram bot and obtain the bot token. You can do this by talking to the BotFather on Telegram.


***Python Libraries:*** You'll need to install the required Python libraries. You can do this using 

````pip install -r requirements.txt````

## Usage

1. Clone the Repository: Clone this repository to your local machine:

        git clone https://github.com/your_username/shipment-tracker-bot.git
        cd shipment-tracker-bot
2. Set up Environment Variables: Create a .env file and add your Telegram bot token as mentioned in the prerequisites.

3. Running the Bot: Run the program by executing bot.py:

        python bot.py
4. Bot Commands:

       /start: This command initiates the bot and provides instructions to the user.
       /track_bluedart <shipment_number>: Use this command to track a BlueDart shipment. Replace <shipment_number> with the actual shipment number you want to track.

## Customization
* You can customize the bot by modifying the Python code in bot.py:

* You can change the bot's commands, responses, and behavior by editing the track_bluedart function.

* You can customize the post-initialization behavior of the bot in the post_init function.

* If you want to add more commands, simply create additional CommandHandler instances and attach them to the Application using app.add_handler.

* For more advanced customization, you can explore the python-telegram-bot library documentation.

## License
This program is distributed under the **[MIT License]()**. You are free to use and modify it for your needs, but please be sure to provide proper attribution and adhere to the terms of the license.
------------------------------------------------------------File Path : main.py
File Content : import os
import telegram.ext.filters
from table_manager import process_shipment

# Define a function to handle the /start command
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext, MessageHandler
from dotenv import load_dotenv

load_dotenv(".env")
token = os.getenv("token")


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([
        ('track_bluedart', 'track the provided shipment and give updates')
    ])


async def track_bluedart(update: Update, context: CallbackContext, has_args=True) -> None:
    shipment_number = context.args
    if shipment_number and len(shipment_number) == 1 and shipment_number[0].isdigit():
        current_status = process_shipment(shipment_number[0], chat_id=update.message.chat_id)
        print(current_status)
        await update.message.reply_text(current_status, parse_mode='HTML')
    else:
        await update.message.reply_text("Please provide a valid shipment number")


app = ApplicationBuilder().token(token).post_init(post_init).build()
app.add_handler(CommandHandler("track_bluedart", track_bluedart))

app.run_polling()

------------------------------------------------------------File Path : requirements.txt
File Content : anyio==4.0.0
beautifulsoup4==4.12.2
certifi==2023.7.22
charset-normalizer==3.3.0
cloudscraper==1.2.71
exceptiongroup==1.1.3
h11==0.14.0
httpcore==0.18.0
httpx==0.25.0
idna==3.4
pyparsing==3.1.1
python-dotenv==1.0.0
python-telegram-bot==20.6
requests==2.31.0
requests-toolbelt==1.0.0
schedule==1.2.1
sniffio==1.3.0
soupsieve==2.5
texttable==1.7.0
tinydb==4.8.0
urllib3==2.0.6

------------------------------------------------------------File Path : scripts/bluedart.py
File Content : from cloudscraper import create_scraper
from bs4 import BeautifulSoup
from texttable import Texttable


def get_latest_update(tracking_id):
    scraper = create_scraper()
    res = scraper.get(f"https://bluedart.com/trackdartresultthirdparty?trackFor=0&trackNo={tracking_id}")
    if res.status_code == 200 and "Status and Scans" in res.text:
        soup = BeautifulSoup(res.text, "html.parser")
        tr = [x for x in soup.find_all("div", {'class': 'table-responsive'}) if "Status and Scans" in x.text][0].find(
            "tbody").find("tr")
        data = [x.text for x in tr.find_all("td")]
        table = Texttable()
        table.set_deco(Texttable.VLINES)
        table.header(["Hub", "Shipment Status", "Date", "Time"])
        table.add_row(data)
        # print  html markup for this table

        return table.draw()
    else:
        return False


------------------------------------------------------------File Path : table_manager.py
File Content : import os
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

------------------------------------------------------------
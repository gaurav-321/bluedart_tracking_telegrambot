# Shipment Tracker Telegram Bot Readme
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
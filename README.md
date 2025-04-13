# Shipment Tracker Telegram Bot

## Introduction

This is a Python program for a Telegram bot that helps users track shipments using the BlueDart tracking service. The bot responds to user commands to track a shipment and provides real-time updates on the shipment's status.

## Features
- Track shipments using BlueDart tracking numbers.
- Receive real-time updates via Telegram messages.
- Persistent storage of tracking information for ongoing updates.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/shipment-tracker-bot.git
   cd shipment-tracker-bot
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Telegram bot by creating a new bot on [BotFather](https://t.me/BotFather) and obtain the API token.

4. Rename `.env.example` to `.env` and add your Telegram bot token:
   ```
   TOKEN=your_bot_token_here
   ```

## Usage

1. Start the bot:
   ```bash
   python main.py
   ```

2. Interact with the bot in a Telegram chat by sending commands:
   - `/track <tracking_number>`: Track a shipment using its BlueDart tracking number.

## Code Structure

- **`main.py`**: The entry point of the application, initializes and runs the Telegram bot.
- **`scripts/bluedart.py`**: Contains functions for fetching shipment status from BlueDart's website.
- **`table_manager.py`**: Manages persistent storage of tracking information using TinyDB.
- **`requirements.txt`**: Lists all required Python packages.

## Contributions

Contributions are welcome! Feel free to open issues or pull requests to improve the bot.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
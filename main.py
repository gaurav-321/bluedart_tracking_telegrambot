import os
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

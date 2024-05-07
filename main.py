import asyncio
import datetime
from aiocron import crontab
from telegram import Bot

# Bot token obtained from BotFather
BOT_TOKEN = '7078577433:AAHJ-o28uqp4wFL_lcjqjdrGtA47rUJP2Uo'

# List of your group members
GROUP_MEMBERS = ['Bobka', 'Vova', 'Avazchik', 'Shoki']

# Variable to keep track of the last person who cooked
last_cook_index = -1


def choose_cook_of_the_day():
    global last_cook_index

    # Increment the last cook index to move to the next person
    last_cook_index = (last_cook_index + 1) % len(GROUP_MEMBERS)

    return GROUP_MEMBERS[last_cook_index]


async def send_notification(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    message_sent = await bot.send_message(chat_id=chat_id, text=message)
    # Pin the message
    await bot.pin_chat_message(chat_id=chat_id, message_id=message_sent.message_id)
    # await bot.send_message(chat_id=chat_id, text=message)


async def scheduled_job():
    # Choose the cook of the day
    cook_of_the_day = choose_cook_of_the_day()

    # Get today's date in dd.mm.yyyy format
    today_date = datetime.date.today().strftime('%d.%m.%Y')

    # Compose the notification message
    message = f"{today_date} - Imruzangi pazandamo: {cook_of_the_day}"

    # Send the notification to your group
    await send_notification(BOT_TOKEN, -1002029758960, message)


if __name__ == "__main__":
    # Schedule the job to run every day at 12 pm
    crontab('02 16 * * *', func=scheduled_job)

    # Run the event loop
    asyncio.get_event_loop().run_forever()

import asyncio
import datetime
from aiocron import crontab
from telegram import Bot

# Bot token obtained from BotFather
BOT_TOKEN = '7078577433:AAHJ-o28uqp4wFL_lcjqjdrGtA47rUJP2Uo'

# List of your group members
GROUP_MEMBERS = ['Vova', 'Avazchik', 'Shoki', 'Bobka']

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

    # Get the next crontab event time
    next_event = await crontab('46 14 * * *', func=scheduled_job).next()

    # Sleep until the next crontab event
    await asyncio.sleep(next_event.total_seconds())


if __name__ == "__main__":
    # Run the scheduled job
    asyncio.run(scheduled_job())

import asyncio
import datetime
from aiocron import crontab
from telegram import Bot

# Bot token obtained from BotFather
BOT_TOKEN = '7078577433:AAHJ-o28uqp4wFL_lcjqjdrGtA47rUJP2Uo'

# Path to the file storing the last cook index
LAST_COOK_INDEX_FILE = 'last_cook_index.txt'

# List of your group members
GROUP_MEMBERS = ['Vova', 'Avazchik', 'Shoki', 'Bobka']


def read_last_cook_index():
    try:
        with open(LAST_COOK_INDEX_FILE, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        # If the file doesn't exist, return -1 as default index
        return -1


def write_last_cook_index(index):
    with open(LAST_COOK_INDEX_FILE, 'w') as file:
        file.write(str(index))


def choose_cook_of_the_day():
    last_cook_index = read_last_cook_index()

    # Increment the last cook index to move to the next person
    last_cook_index = (last_cook_index + 1) % len(GROUP_MEMBERS)

    # Save the updated index
    write_last_cook_index(last_cook_index)

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
    # Create and run the event loop explicitly
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Schedule the job to run every day at 18:00 (6:00 PM)
    crontab('03 18 * * *', func=scheduled_job)

    # Run the event loop
    try:
        loop.run_forever()
    finally:
        loop.close()

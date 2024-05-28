import asyncio
import datetime
from aiocron import crontab
from telegram import Bot, Update
from telegram.ext import Application, CallbackQueryHandler, PollAnswerHandler

# Bot token obtained from BotFather
BOT_TOKEN = '7078577433:AAHJ-o28uqp4wFL_lcjqjdrGtA47rUJP2Uo'

# Path to the file storing the last cook index
LAST_COOK_INDEX_FILE = 'last_cook_index.txt'

# List of your group members
GROUP_MEMBERS = ['Vova', 'Avazchik', 'Bobka', 'Shoki']

# Global state to track poll responses and chat ID
poll_responses = {}
current_poll_message_id = None
current_chat_id = None


def read_last_cook_index():
    try:
        with open(LAST_COOK_INDEX_FILE, 'r') as file:
            content = file.read().strip()
            return int(content) if content else -1
    except FileNotFoundError:
        return -1


def write_last_cook_index(index):
    with open(LAST_COOK_INDEX_FILE, 'w') as file:
        file.write(str(index))


def choose_cook_of_the_day():
    last_cook_index = read_last_cook_index()
    last_cook_index = (last_cook_index + 1) % len(GROUP_MEMBERS)
    write_last_cook_index(last_cook_index)
    return GROUP_MEMBERS[last_cook_index]


cook_of_the_day = choose_cook_of_the_day()  # Today's cook


async def send_poll(bot_token, chat_id, question, options):
    global current_poll_message_id, current_chat_id
    bot = Bot(token=bot_token)
    poll = await bot.send_poll(chat_id=chat_id, question=question, options=options, is_anonymous=False)
    current_poll_message_id = poll.message_id
    current_chat_id = chat_id
    return poll


async def send_confirmation(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)


async def handle_poll_answer(update: Update, context):
    global poll_responses, current_poll_message_id, current_chat_id

    poll_id = update.poll_answer.poll_id
    user_id = update.poll_answer.user.id
    options_chosen = update.poll_answer.option_ids

    # Store the response
    if poll_id not in poll_responses:
        poll_responses[poll_id] = {}
    poll_responses[poll_id][user_id] = options_chosen[0]

    # Check if all members have responded
    if len(poll_responses[poll_id]) >= 3:
        yes_votes = sum(1 for vote in poll_responses[poll_id].values() if vote == 0)
        last_cook = GROUP_MEMBERS[read_last_cook_index()]

        if yes_votes >= 3:
            await send_confirmation(BOT_TOKEN, current_chat_id, f"Imruzangi pazandamo: {cook_of_the_day}")
        else:
            await send_confirmation(BOT_TOKEN, current_chat_id, f"Imruzangi pazandamo: {last_cook}")

        # Reset the state
        poll_responses.clear()
        current_poll_message_id = None
        current_chat_id = None


async def scheduled_job():
    today_date = datetime.date.today().strftime('%d.%m.%Y')
    question = f"{today_date} - Pazanda {cook_of_the_day}?"
    options = ["Yes", "No"]

    await send_poll(BOT_TOKEN, -1002029758960, question, options)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(PollAnswerHandler(handle_poll_answer))

    # Schedule the job to run every day at 18:00 (6:00 PM)
    crontab('0 12 * * *', func=scheduled_job)

    application.run_polling()


if __name__ == "__main__":
    main()

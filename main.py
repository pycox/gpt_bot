import openai
import os
from dotenv import load_dotenv

load_dotenv()

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
    CommandHandler,
)

telegram_token = os.getenv("TELEGRAM_TOKEN")
openai.api_key = os.getenv("OPENAI_TOKEN")
openai_version = os.getenv("OPENAI_VERSION")

messages_list = []


def append_history(content, role):
    messages_list.append({"role": role, "content": content})
    return messages_list


def clear_history():
    messages_list.clear()
    return messages_list


async def process_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    append_history(update.message.text, "user")

    response = generate_gpt_response()

    append_history(response, "assistant")
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode="MARKDOWN")

def generate_gpt_response():
    completion = openai.ChatCompletion.create(model=openai_version, messages=messages_list)
    return completion.choices[0].message["content"]


async def reset_history(update, context):
    clear_history()
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Messages history cleaned"
    )
    return messages_list


if __name__ == "__main__":
    application = ApplicationBuilder().token(telegram_token).build()
    text_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), process_text_message
    )
    application.add_handler(text_handler)

    application.add_handler(CommandHandler("cls", reset_history))

    application.run_polling()

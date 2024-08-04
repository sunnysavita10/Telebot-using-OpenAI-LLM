import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import sys
import openai
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

TOKEN = os.getenv('TOKEN')

MODEL_NAME = "gemini-1.5-pro"


# Connect to openai server
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# print("OK")

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

class Reference:

    def __init__(self) -> None:
        self.response = ""

reference = Reference()


def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response = ""


@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Hi\nI am a Chat Bot! Created by Sunny. How can i assist you?")



@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")



@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm a bot created by Sunny! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)





@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME,google_api_key="AIzaSyD2ej6w4BipiA2YehXe3U_bO7kLC5yrLQY")

    result = llm.invoke(message.text)
    
    #print(result.content)
    
    """response = openai.ChatCompletion.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query 
        ]
    )"""
    #reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{result.content}")
    await bot.send_message(chat_id = message.chat.id, text = result.content)



if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)

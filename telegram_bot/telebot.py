import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import openai

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Telegram Bot token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Set up GPT model name
MODEL_NAME = "gpt-3.5-turbo-instruct"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Handler for /start and /help commands
@dp.message_handler(commands=['start', 'help'])
async def command_start_handler(message: types.Message):
  """
  This handler responds to the /start and /help commands.
  """
  await message.reply("Hi! I'm a chatbot powered by OpenAI. Feel free to ask me anything.")

# Handler for all other messages
@dp.message_handler()
async def chatgpt(message: types.Message):
  """
  This handler processes all other messages and generates responses using the chatGPT model.
  """
  try:
    # Get user's message
    user_message = message.text

    # Call OpenAI API to generate response
    response = openai.Completion.create(
        model=MODEL_NAME,
        prompt=user_message,
        max_tokens=100  # Adjust the maximum number of tokens for the response as needed
    )

    # Send the response back to the user
    await message.reply(response.choices[0].text.strip())

  except openai.error.RateLimitError as e:
    # Handle OpenAI quota error specifically
    logging.exception("OpenAI API quota exceeded:", e)
    await message.reply("Sorry, I can't answer that right now. I've reached my limit for requests. Please try again later.")

  except Exception as e:
    # Handle other exceptions
    logging.exception("An error occurred while processing the message.")
    await message.reply("Sorry, I couldn't process your request at the moment.")

# Start the bot
if __name__ == "__main__":
  executor.start_polling(dp, skip_updates=True)

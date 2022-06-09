import webscraping as wp
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import re
import os 
from dotenv import load_dotenv
load_dotenv()

class TelegramBot:
  token = os.getenv('TOKEN')

  def __init__(self):
    self.wp = wp.Webscraping()
    self.updater = Updater(self.token)
    self.dispatcher = self.updater.dispatcher
    self.dispatcher.add_handler(CommandHandler("start", self.command_start))
    self.dispatcher.add_handler(CommandHandler("help",  self.command_help))
    self.dispatcher.add_handler(CommandHandler("means", self.command_means))
    self.dispatcher.add_handler(CommandHandler("expression", self.command_expression))
    self.dispatcher.add_handler(CommandHandler("meansPT", self.command_meansPT))
    #self.dispatcher.add_handler(CommandHandler("voice", self.command_voice))
    self.updater.start_polling()
    self.updater.idle()

  def command_start(self, update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
    )

  def command_help(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    text = """
      Hello! I am a bot to search words in Cambridge dictionary.
      You can type "/means word" and I will search and give the means to you
      with a pronunciation
      """
    update.message.reply_text(text)

  def command_echo(update, context) -> None:
    """Echo the user message."""
    print(update.message)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)

  def command_means(self, update: Update, context: CallbackContext) -> None:
    try:
      wordTyped = update.message.text.replace("/means ", "")
      user = update.effective_user
      result = re.search(r"^[A-Za-z]*$", wordTyped)
      self._reply_to_user(result, user, update)
    except Exception as err:
      print(f"{type(err).__name__} was raised: {err}")
      update.message.reply_text(
          'Sorry, ' + user.name + '. Something went wrong when I was trying to process your request.')
      
  def command_meansPT(self, update: Update, context: CallbackContext) -> None:
    try:
      wordTyped = update.message.text.replace("/meansPT ", "")
      user = update.effective_user
      result = re.search(r"^[A-Za-z]*$", wordTyped)
      self._reply_to_user(result, user, update)            
    except Exception as err:
      print(f"{type(err).__name__} was raised: {err}")
      update.message.reply_text(
          'Sorry, ' + user.name + '. Something went wrong when I was trying to process your request.')
      
  def command_expression(self, update: Update, context: CallbackContext) -> None:
    try:
      user = update.effective_user
      wordTyped = update.message.text.replace("/expression ", "")
      result = re.search(r"^[a-zA-z]+\s[a-zA-z]*$", wordTyped)
      self._reply_to_user(result, user, update)
    except Exception as err:
      print(f"{type(err).__name__} was raised: {err}")
      update.message.reply_text(
          'Sorry, ' + user.name + '. Something went wrong when I was trying to process your request.')
  
  def _reply_to_user(self, result, user, update: Update) -> None:
    if(result != None):
        word = result[0]
        word = word.replace(" ", "-")
        print(word)
        means, audioLink, examples = wp.Webscraping.get_word_means(
            self.wp, word)

        reply = 'Hi ' + user.name + ','
        reply += '\n' + 'You asked for the means of the word: ' + word + '.'
        reply += '\n' + 'And here is: \n\n'
        for index, mean in enumerate(means):
          reply += str(index + 1) + '. ' + mean + '\n'

        if len(examples) > 0:
          reply += '\n'
          reply += 'And here are some examples: '
          reply += '\n'
          for index, example in enumerate(examples):
            reply += str(index + 1) + '. ' + example + '\n'

        update.message.reply_text(reply)
        if audioLink:
          update.message.reply_voice(
              voice=self._get_audio_from_link(audioLink))
        else:
          update.message.reply_text('We not found any audio from this word')
    else:
      update.message.reply_text('Sorry, ' + user.name + '. I was not able to undestand what word do you want I get. Try again with something like this "/means word".')
    
  def _get_audio_from_link(self, audio_link):
    r = requests.get(audio_link, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    return r.content
  
  #def command_voice(self, update: Update, context: CallbackContext) -> None:
  #  r = requests.get("https://dictionary.cambridge.org/pt/media/ingles-portugues/us_pron_ogg/h/hou/house/house.ogg", headers={
  #      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  #  })
  #  context.bot.send_voice(chat_id=update.effective_chat.id, voice=r.content)

if __name__ == '__main__':
  bot = TelegramBot()

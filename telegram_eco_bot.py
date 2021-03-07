import os

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler


class TelegramEcoBot:
    def __init__(self):
        self.updater = Updater(token=os.environ['token_bot'], use_context=True)
        dp = self.updater.dispatcher
        # self.bot = telegram.Bot(os.environ['token_bot'])

        dp.add_handler(CommandHandler('start', self.start))

        self.updater.start_polling()

    def start(self, update, context):
        text = "%s \n%s \n%s \n%s \n%s \n%s" % (
                                                 "Привет!",
                                                 "Этот бот в будущем поможет тебе разобраться с вопросом "
                                                 "раздельного сбора в Череповце",
                                                 "",
                                                 "Сейчас он находится на этапе разработки",
                                                 "",
                                                 "По вопросам пишите @Elrik237",
                                              )
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

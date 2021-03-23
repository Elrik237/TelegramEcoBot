import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from markings_database import MarkingsDatabase


class TelegramEcoBot:
    def __init__(self):
        self.updater = Updater(token=os.environ['token_bot'], use_context=True)
        dp = self.updater.dispatcher

        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CommandHandler('event', self.nearest_event))
        dp.add_handler(CommandHandler('info', self.info_che))
        dp.add_handler(CommandHandler('marking', self.general_information))
        dp.add_handler(MessageHandler(Filters.text & (~Filters.command), self.send_marking))
        dp.add_handler(CallbackQueryHandler(self.get_callback_from_button))
        dp.add_handler(MessageHandler(Filters.command, self.unknown))

        self.db_markings = MarkingsDatabase()

        self.updater.start_polling()

    def start(self, update, context):
        text = "%s \n%s \n%s \n%s \n%s" % (
            "Привет! Хотите сдавать отходы раздельно, но запутались? Со мной всё станет проще!",
            "",
            "Я стану вашим проводником в мир раздельного сбора, подскажу, как различать маркировки, "
            "что и куда можно сдать на переработку, как подготовить вторсырье дома.",
            "",
            "Я сотрудничаю с общественной организацией «РазДельный сбор» (г. Череповец), "
            "которая проводит акции по сбору вторсырья каждую первую субботу месяца."

        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                                 reply_markup=self.keyboard_start())

    def keyboard_start(self):
        keyboard_start = [
            [
                InlineKeyboardButton("Маркировки ", callback_data='1'),
                InlineKeyboardButton("Что можно сдать в Череповце", callback_data='2'),
            ],
            [
                InlineKeyboardButton("Ближайшая акция", callback_data='3'),
            ]
        ]

        markup_start = InlineKeyboardMarkup(keyboard_start, one_time_keyboard=True)
        return markup_start

    def nearest_event(self, update, context):
        text = 'Следующая акция РазДельного Сбора пройдет:\n 03 ареля 2021.\n\n' \
               'Место проведения уточняйте в группе VK: https://vk.com/rs_che'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    def info_che(self, update, context):
        text = '%s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n %s\n' % (
            'На ближайщей акции можно сдать::',
            '',
            '* Диски (CD/DVD и пр.),',
            '* Зубные щетки,',
            '* Батарейки, аккумуляторы,',
            '* Пластиковые крышечки,',
            '* Стеклотару (любых цветов) (бутылки и банки),',
            '* Бутылочный ПЭТ и HDPE,',
            '* Металл (жесть и алюминий),',
            '* Одежду (упакованную в мешки, НЕ ВЕТОШЬ!),',
            '* Отходы электрооборудования, оригинальные картриджи от лазерных принтеров,',
            '* Таблетки и блистерную упаковку от таблеток (пожалуйста, отдельно друг от друга),',
            '* Пластиковые пакеты: HDPE/02, LDPE/04, пузырчатую и стрейч пленки (отдельно друг от друга),',
            '* Использованные рекламные баннеры,',
            '* Жесткий бытовой полипропилен PР/ПП (05) и HDPE/ПЭ (02) '
            '(хозяйственные ведра, овощные ящики или контейнеры, тазы и другие хозяйственные '
            'предметы с указанной маркировкой.'

        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    def general_information(self, update, context):
        keyboard_info = [
            [
                InlineKeyboardButton("Выбрать из категории ", callback_data='4'),
                InlineKeyboardButton("Ввести в ручную", callback_data='5'),
            ],

        ]

        markup_info = InlineKeyboardMarkup(keyboard_info, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                 reply_markup=markup_info)

    def send_marking(self, update, context):
        message = update.message.text
        self.db_markings.send_marking(update, context, message)

    def send_categories(self, update, context):
        keyboard_categories = [
            [
                InlineKeyboardButton("Пластик", callback_data='6'),
                InlineKeyboardButton("Пакеты", callback_data='7'),

            ],
            [
                InlineKeyboardButton("Стекло", callback_data='8'),
                InlineKeyboardButton("Металл", callback_data='9'),

            ],
            [
                InlineKeyboardButton("Бумага, картон", callback_data='10'),
                InlineKeyboardButton("Электрооборудование", callback_data='11'),

            ],
            [
                InlineKeyboardButton("Лампочки", callback_data='12'),
                InlineKeyboardButton("Батарейки", callback_data='13'),

            ],
            [
                InlineKeyboardButton("Таблетки и блистеры", callback_data='14'),
                InlineKeyboardButton("Одежда", callback_data='15'),

            ],
            [
                InlineKeyboardButton("Рекламные баннеры", callback_data='16'),
                InlineKeyboardButton("Зубные щётки", callback_data='17'),

            ],
            [
                InlineKeyboardButton("Диски", callback_data='18'),
                InlineKeyboardButton("Тетрапак", callback_data='19'),
            ]

        ]

        markup_categories = InlineKeyboardMarkup(keyboard_categories, resize_keyboard=False,
                                                 one_time_keyboard=True)

        context.bot.send_message(chat_id=update.effective_chat.id, text='Категории:',
                                 reply_markup=markup_categories)

        context.bot.editMessageReplyMarkup(chat_id=update.effective_chat.id,
                                           message_id=update.effective_message.message_id,
                                           reply_markup=self.keyboard_start())

    def get_callback_from_button(self, update, context):
        query = update.callback_query

        if query.data == '1':
            self.general_information(update, context)
        elif query.data == '2':
            self.info_che(update, context)
        elif query.data == '3':
            self.nearest_event(update, context)
        elif query.data == '4':
            self.send_categories(update, context)
        elif query.data == '5':
            context.bot.send_message(chat_id=update.effective_chat.id, text='Введите номер маркировки,'
                                                                            ' в формате двухзначного числа:')
        elif query.data == '6':
            keyboard_plastic = [
                [
                    InlineKeyboardButton("PET (PETE) / ПЭТ / ПЭТФ / 01 ", callback_data='M-01'),
                ],
                [
                    InlineKeyboardButton("PEHD / HDPE / ПЭНД / 02", callback_data='M-02'),
                ]
            ]
            markup_plastic = InlineKeyboardMarkup(keyboard_plastic, resize_keyboard=False,
                                                  one_time_keyboard=True)

            context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                     reply_markup=markup_plastic)
        elif query.data == '7':
            keyboard_plastic = [
                [
                    InlineKeyboardButton("PET (PETE) / ПЭТ / ПЭТФ / 01 ", callback_data='M-01'),
                ],
                [
                    InlineKeyboardButton("PEHD / HDPE / ПЭНД / 02", callback_data='M-02'),
                ]
            ]
            markup_plastic = InlineKeyboardMarkup(keyboard_plastic, resize_keyboard=False,
                                                  one_time_keyboard=True)

            context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                     reply_markup=markup_plastic)
        elif query.data == '8':
            keyboard_plastic = [
                [
                    InlineKeyboardButton("PET (PETE) / ПЭТ / ПЭТФ / 01 ", callback_data='M-01'),
                ],
                [
                    InlineKeyboardButton("PEHD / HDPE / ПЭНД / 02", callback_data='M-02'),
                ]
            ]
            markup_plastic = InlineKeyboardMarkup(keyboard_plastic, resize_keyboard=False,
                                                  one_time_keyboard=True)

            context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                     reply_markup=markup_plastic)
        elif query.data == '9':
            keyboard_plastic = [
                [
                    InlineKeyboardButton("PET (PETE) / ПЭТ / ПЭТФ / 01 ", callback_data='M-01'),
                ],
                [
                    InlineKeyboardButton("PEHD / HDPE / ПЭНД / 02", callback_data='M-02'),
                ]
            ]
            markup_plastic = InlineKeyboardMarkup(keyboard_plastic, resize_keyboard=False,
                                                  one_time_keyboard=True)

            context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                     reply_markup=markup_plastic)
        elif query.data == '10':
            keyboard_plastic = [
                [
                    InlineKeyboardButton("PET (PETE) / ПЭТ / ПЭТФ / 01 ", callback_data='M-01'),
                ],
                [
                    InlineKeyboardButton("PEHD / HDPE / ПЭНД / 02", callback_data='M-02'),
                ]
            ]
            markup_plastic = InlineKeyboardMarkup(keyboard_plastic, resize_keyboard=False,
                                                  one_time_keyboard=True)

            context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                     reply_markup=markup_plastic)
        elif query.data == '11':
            keyboard_plastic = [
                [
                    InlineKeyboardButton("PET (PETE) / ПЭТ / ПЭТФ / 01 ", callback_data='M-01'),
                ],
                [
                    InlineKeyboardButton("PEHD / HDPE / ПЭНД / 02", callback_data='M-02'),
                ]
            ]
            markup_plastic = InlineKeyboardMarkup(keyboard_plastic, resize_keyboard=False,
                                                  one_time_keyboard=True)

            context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                     reply_markup=markup_plastic)
        elif query.data == '12':
            keyboard_plastic = [
                [
                    InlineKeyboardButton("PET (PETE) / ПЭТ / ПЭТФ / 01 ", callback_data='M-01'),
                ],
                [
                    InlineKeyboardButton("PEHD / HDPE / ПЭНД / 02", callback_data='M-02'),
                ]
            ]
            markup_plastic = InlineKeyboardMarkup(keyboard_plastic, resize_keyboard=False,
                                                  one_time_keyboard=True)

            context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                     reply_markup=markup_plastic)
        elif query.data == '13':
            keyboard_plastic = [
                [
                    InlineKeyboardButton("PET (PETE) / ПЭТ / ПЭТФ / 01 ", callback_data='M-01'),
                ],
                [
                    InlineKeyboardButton("PEHD / HDPE / ПЭНД / 02", callback_data='M-02'),
                ]
            ]
            markup_plastic = InlineKeyboardMarkup(keyboard_plastic, resize_keyboard=False,
                                                  one_time_keyboard=True)

            context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                     reply_markup=markup_plastic)
        elif query.data == '14':
            keyboard_plastic = [
                [
                    InlineKeyboardButton("PET (PETE) / ПЭТ / ПЭТФ / 01 ", callback_data='M-01'),
                ],
                [
                    InlineKeyboardButton("PEHD / HDPE / ПЭНД / 02", callback_data='M-02'),
                ]
            ]
            markup_plastic = InlineKeyboardMarkup(keyboard_plastic, resize_keyboard=False,
                                                  one_time_keyboard=True)

            context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                     reply_markup=markup_plastic)
        elif query.data == '15':
            keyboard_plastic = [
                [
                    InlineKeyboardButton("PET (PETE) / ПЭТ / ПЭТФ / 01 ", callback_data='M-01'),
                ],
                [
                    InlineKeyboardButton("PEHD / HDPE / ПЭНД / 02", callback_data='M-02'),
                ]
            ]
            markup_plastic = InlineKeyboardMarkup(keyboard_plastic, resize_keyboard=False,
                                                  one_time_keyboard=True)

            context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                     reply_markup=markup_plastic)
        elif query.data == '16':
            keyboard_plastic = [
                [
                    InlineKeyboardButton("PET (PETE) / ПЭТ / ПЭТФ / 01 ", callback_data='M-01'),
                ],
                [
                    InlineKeyboardButton("PEHD / HDPE / ПЭНД / 02", callback_data='M-02'),
                ]
            ]
            markup_plastic = InlineKeyboardMarkup(keyboard_plastic, resize_keyboard=False,
                                                  one_time_keyboard=True)

            context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                     reply_markup=markup_plastic)
        elif query.data == '17':
            keyboard_plastic = [
                [
                    InlineKeyboardButton("PET (PETE) / ПЭТ / ПЭТФ / 01 ", callback_data='M-01'),
                ],
                [
                    InlineKeyboardButton("PEHD / HDPE / ПЭНД / 02", callback_data='M-02'),
                ]
            ]
            markup_plastic = InlineKeyboardMarkup(keyboard_plastic, resize_keyboard=False,
                                                  one_time_keyboard=True)

            context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                     reply_markup=markup_plastic)
        elif query.data == '18':
            keyboard_plastic = [
                [
                    InlineKeyboardButton("PET (PETE) / ПЭТ / ПЭТФ / 01 ", callback_data='M-01'),
                ],
                [
                    InlineKeyboardButton("PEHD / HDPE / ПЭНД / 02", callback_data='M-02'),
                ]
            ]
            markup_plastic = InlineKeyboardMarkup(keyboard_plastic, resize_keyboard=False,
                                                  one_time_keyboard=True)

            context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                     reply_markup=markup_plastic)
        elif query.data == '19':
            keyboard_plastic = [
                [
                    InlineKeyboardButton("PET (PETE) / ПЭТ / ПЭТФ / 01 ", callback_data='M-01'),
                ],
                [
                    InlineKeyboardButton("PEHD / HDPE / ПЭНД / 02", callback_data='M-02'),
                ]
            ]
            markup_plastic = InlineKeyboardMarkup(keyboard_plastic, resize_keyboard=False,
                                                  one_time_keyboard=True)

            context.bot.send_message(chat_id=update.effective_chat.id, text='На выбор:',
                                     reply_markup=markup_plastic)
        elif 'M' in query.data:
            marking = query.data.split('-')
            self.db_markings.send_marking(update, context, marking[1])

    def unknown(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Простите, я не понял вашу команду, попробуйте снова!")

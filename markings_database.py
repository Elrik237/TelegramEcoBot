import os

import pandas as pd
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import DeclarativeBase
from models.marking import Marking


class MarkingsDatabase:
    def __init__(self):
        self.engine = create_engine('sqlite:///database/marking.db', echo=None)

        DeclarativeBase.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        if os.path.exists('database/marking.csv') == False:
            self.parser()

    def parser(self):
        data_xls = pd.read_excel('marking.xlsx', index_col=None)
        data_xls.to_csv('database/marking.csv', encoding='UTF-8')

        with open('database/marking.csv', encoding='UTF-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            for row in file_reader:
                marking = Marking(row[1], row[2], row[3], row[4])
                self.session.add(marking)
            self.session.commit()
            self.session.close()

    def send_marking(self, update, context, message):
        for markings, danger, using, processing in self.session.query(Marking.markings, Marking.using,
                                                                      Marking.danger, Marking.processing):
            if message in markings:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f'{markings} \n{using} \n{danger} \n{processing}')





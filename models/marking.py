from sqlalchemy import Column, Integer, String

from models import DeclarativeBase


class Marking(DeclarativeBase):
    __tablename__ = 'marking'
    id = Column(Integer, primary_key=True)
    markings = Column(String)
    using = Column(String)
    danger = Column(String)
    processing = Column(String)

    def __init__(self, markings, using, danger, processing):
        self.markings = markings
        self.using = using
        self.danger = danger
        self.processing = processing

    def __repr__(self):
        return "%s, %s, %s, %s" % (
            self.markings, self.using, self.danger, self.processing)

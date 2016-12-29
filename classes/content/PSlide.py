# -*- coding: utf-8 -*-
from classes.content.SingleContent import SingleContent
from classes.play.PlaySlide import PlaySlide
from classes.insert.InsertAtEnd import InsertAtEnd
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


class PSlide(SingleContent):

    def __init__(self, filepath, display_duration):
        super(PSlide, self).__init__(filepath, InsertAtEnd(), PlaySlide(display_duration))
















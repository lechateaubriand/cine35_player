# -*- coding: utf-8 -*-
from classes.content.SingleContent import SingleContent
from classes.play.PlayMovie import PlayMovie
from classes.insert.InsertAtEnd import InsertAtEnd
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


class Movie(SingleContent):

    def __init__(self, filepath):
        super(Movie, self).__init__(filepath, InsertAtEnd(), PlayMovie())
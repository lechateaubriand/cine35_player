# -*- coding: utf-8 -*-
from classes.play.IPlay import IPlay
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)

class PlayMovie(IPlay):

    def play(self, singleContentMovie):
        print("Play movie")
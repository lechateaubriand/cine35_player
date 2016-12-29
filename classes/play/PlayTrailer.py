# -*- coding: utf-8 -*-
from classes.play.IPlay import IPlay
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)

class PlayTrailer(IPlay):

    def play(self, iContentTrailer):
        print("Play trailer")
        iContentTrailer.movie.play()
        iContentTrailer.slide.play()
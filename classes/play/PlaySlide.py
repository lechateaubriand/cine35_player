# -*- coding: utf-8 -*-
from classes.play.IPlay import IPlay
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)

class PlaySlide(IPlay):

    def __init__(self, display_duration):
        self.display_duration = display_duration

    def play(self, singleContentSlide):
        print("Play slide")
        print("wait for %i seconds" % self.display_duration)
# -*- coding: utf-8 -*-
from classes.content.Movie import Movie
from classes.insert.InsertSeveralTimes import InsertSeveralTimes
import env_variables
import os
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


class LoopedMovie(Movie):

    def __init__(self, filepath):
        super(LoopedMovie, self).__init__(filepath)
        self.start_place = int(os.path.basename(filepath).split("__")[1])
        self.loop_step = int(os.path.basename(filepath).split("__")[2])
        self.insert_behaviour = InsertSeveralTimes(self.start_place, self.loop_step)

# -*- coding: utf-8 -*-
from classes.content.Movie import Movie
from classes.insert.InsertSeveralTimes import InsertSeveralTimes
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


class LoopedMovie(Movie):

    def __init__(self, filepath, start_place, loop_step):
        super(LoopedMovie, self).__init__(filepath)
        self.insert_behaviour = InsertSeveralTimes(start_place, loop_step)

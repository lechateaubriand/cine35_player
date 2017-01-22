# -*- coding: utf-8 -*-
from classes.content.PSlide import PSlide
from classes.insert.InsertSeveralTimes import InsertSeveralTimes
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


class LoopedSlide(PSlide):

    def __init__(self, filepath, start_place, loop_step):
        super(LoopedSlide, self).__init__(filepath, env_variables.looped_slide_duration)
        self.insert_behaviour = InsertSeveralTimes(start_place, loop_step)

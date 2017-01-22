# -*- coding: utf-8 -*-
from classes.insert.IInsert import IInsert
from classes.content.Trailer import Trailer
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)

class InsertSeveralTimes(IInsert):

    def __init__(self, start_index, loop_step):
        self.start_index = start_index
        self.loop_step = loop_step

    def insert(self, icontent, playlist):
        new_list = []
        can_be_last = True
        if self.start_index == 0:
            new_list = [icontent]
            can_be_last = False

        nb_trailer = 0
        for index, each in enumerate(playlist):
            new_list.append(each)
            if isinstance(each, Trailer):
                if nb_trailer != 0 and nb_trailer%self.loop_step == 0:
                    if (index == len(playlist)-1 and can_be_last is False):
                        pass
                    else:
                        new_list.append(icontent)
                nb_trailer += 1

        return new_list

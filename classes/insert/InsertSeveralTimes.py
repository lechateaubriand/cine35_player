# -*- coding: utf-8 -*-
from classes.insert.IInsert import IInsert
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)

class InsertSeveralTimes(IInsert):

    def __init__(self, start_place, loop_step):
        self.start_place = start_place
        self.loop_step = loop_step

    def insert(self, icontent, playlist):
        new_list = []
        if self.start_place == 0:
            new_list.append(icontent)

        for start_index in range(self.start_place, len(playlist), self.loop_step):
            new_list.extend(playlist[start_index:start_index+self.loop_step])
            if start_index+self.loop_step < len(playlist):
                new_list.append(icontent)
        return new_list

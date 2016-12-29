# -*- coding: utf-8 -*-
from classes.insert.IInsert import IInsert
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)

class InsertAtEnd(IInsert):

    def insert(self, icontent, playlist):
        playlist.append(icontent)
        return playlist
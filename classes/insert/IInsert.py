# -*- coding: utf-8 -*-
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)

class IInsert:

    def insert(self, icontent, playlist):
        raise NotImplementedError
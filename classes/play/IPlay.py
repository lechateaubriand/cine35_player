# -*- coding: utf-8 -*-
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)

class IPlay:
    def play(self):
        raise NotImplementedError
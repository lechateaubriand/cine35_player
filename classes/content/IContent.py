# -*- coding: utf-8 -*-
from time import mktime, strptime
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


class IContent:

    def __init__(self, insert_behaviour, play_behaviour):
        self.insert_behaviour = insert_behaviour
        self.play_behaviour = play_behaviour

    def play(self, play_thread):
        self.play_behaviour.play(play_thread, self)

    def insert(self, playlist):
        updated_playlist = self.insert_behaviour.insert(self, playlist)
        return updated_playlist

    def __str__(self):
        raise NotImplementedError
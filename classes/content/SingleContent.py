# -*- coding: utf-8 -*-
import os.path
from time import mktime, strptime
from classes.content.IContent import IContent
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


class SingleContent(IContent):

    def __init__(self, filepath, insert_behaviour, play_behaviour):
        super(SingleContent, self).__init__(insert_behaviour, play_behaviour)
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.end_date = self.filename.split("__")[0]
        self.end_date_epoch = mktime(strptime(self.end_date, "%Y_%m_%d"))

    def __str__(self):
        chaine = "["
        chaine += ','.join([self.filepath, self.end_date])
        chaine += "]"
        return chaine

    def get_filename(self):
        return [self.filename]

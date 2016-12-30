# -*- coding: utf-8 -*-
import subprocess
from classes.play.IPlay import IPlay
from time import sleep
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)

class PlaySlide(IPlay):

    def __init__(self, display_duration):
        self.display_duration = display_duration

    def play(self, play_thread, singleContentSlide):
        """ 
        function that displays the slide using feh command during 
        display_duration number of timer_in_seconds
        """
        try:
            logging.info("slide montre: %s" % singleContentSlide.filepath)
            command = "export DISPLAY=:0;/usr/bin/feh --no-fehbg --bg-scale '" + singleContentSlide.filepath +"'"
            return_code = subprocess.call(command, shell=True)
            if self.display_duration != 0 and return_code == 0:
                target_time = time.time() + self.display_duration
                while time.time() < target_time and not play_thread.stoprequest.isSet() \
                and not play_thread.nextrequest.isSet() and not play_thread.previousrequest.isSet():
                    sleep(0.5)
            else:
                raise RuntimeError("error when displaying the slide")

        except Exception as e:
            logging.error("command is: %s" % command)
            logging.error("display slide return code: %i" % return_code)
            logging.error('image display failed: %s' % str(e))
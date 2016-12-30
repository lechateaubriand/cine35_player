# -*- coding: utf-8 -*-
from classes.play.IPlay import IPlay
from classes.content.PSlide import PSlide
from omxplayer import OMXPlayer
from dbus.exceptions import DBusException
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)
logging.getLogger('omxplayer').setLevel(logging.CRITICAL)
logging.getLogger('dbus').setLevel(logging.CRITICAL)

class PlayMovie(IPlay):

    def play(self, play_thread, singleContentMovie):
        """
        function qui lance une bande-annonce dans omx player
        """
        player = OMXPlayer(singleContentMovie.filepath, args=['-o', 'hdmi', '-b', '--no-osd'])
        player.play()

        # affichage d'un ecran noir pour ne pas voir l'ecran de la ba precedente
        # brievement avant le changement d'ecran
        black_slide = PSlide(env_variables.black_image, 1)
        black_slide.play(play_thread)
        logging.info("ba: %s, status: %s" % (singleContentMovie.filepath, player.playback_status()))                        

        # tant que la ba n'est pas fini ou stoppee, on attend
        while True:
            try:
                if player.playback_status() == "Playing" and not play_thread.stoprequest.isSet() \
                and not play_thread.previousrequest.isSet() \
                and not play_thread.nextrequest.isSet():
                    sleep(1)
                    #logging.info("%s, %s, %s" % (player.playback_status(),stop, time_status))  
                else:
                    logging.info("player quit")
                    player.quit()
                    # sortie boucle while
                    break
            except DBusException:
                # on passe ici a la fin de la ba, sortie du while
                break
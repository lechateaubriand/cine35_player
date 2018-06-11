# -*- coding: utf-8 -*-
from classes.play.IPlay import IPlay
from classes.content.Slide import Slide
from omxplayer import OMXPlayer
from dbus.exceptions import DBusException
from time import sleep
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)
#logging.getLogger('omxplayer').setLevel(logging.CRITICAL)
#logging.getLogger('dbus').setLevel(logging.CRITICAL)
logging.getLogger('omxplayer').setLevel(logging.DEBUG)
logging.getLogger('dbus').setLevel(logging.INFO)

class PlayMovie(IPlay):

    def play(self, play_thread, singleContentMovie):
        """
        function qui lance une bande-annonce dans omx player
        """
        try:
            player = OMXPlayer(singleContentMovie.filepath, args=['-o', 'hdmi', '-b', '--no-osd'], pause=False)
            player.play()
            logging.debug("after play - before warm-up - ba: %s, status: %s" % (singleContentMovie.filepath, player.playback_status()))                        
            sleep(5)
            logging.debug("after play - after warm-up - ba: %s, status: %s" % (singleContentMovie.filepath, player.playback_status()))                        
        except Exception as e:
            logging.error(str(e), exc_info=1)
            player.quit()
            return

        # affichage d'un ecran noir pour ne pas voir l'ecran de la ba precedente
        # brievement avant le changement d'ecran
        background_slide = Slide(env_variables.background_image, 1, static=True)
        background_slide.play(play_thread)
        logging.info("after background - ba: %s, status: %s" % (singleContentMovie.filepath, player.playback_status()))                        

        # tant que la ba n'est pas fini ou stoppee, on attend
        while True:
            try:
                if player.playback_status() == "Playing" \
                and not play_thread.stoprequest.isSet() \
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
                logging.debug("dbus exception, ba ended")
                player.quit()
                break
            except Exception as e:
                logging.error(str(e), exc_info=1)
                break

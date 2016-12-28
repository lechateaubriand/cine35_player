import sys
import os
if os.environ['HOME_BA'] not in sys.path:
    try:
        sys.path.append(os.environ['HOME_BA'])
    except:
        print("error in HOME_BA environment variable")
import subprocess
import threading
import subprocess
import time
import datetime
import pickle
from time import sleep, mktime, strptime
import logging, logging.config
import env_variables
from classes.MyPlaylist import PlaylistElement
from classes.MySlideList import Slide
from classes.MyBaList import Ba
from omxplayer import OMXPlayer
from dbus.exceptions import DBusException
logging.config.dictConfig(env_variables.LOGGING)
logging.getLogger('omxplayer').setLevel(logging.CRITICAL)
logging.getLogger('dbus').setLevel(logging.CRITICAL)


class BaOmxThread(threading.Thread):
    """
    Thread qui fait tourner les ba et slides en boucle sur un player omx
    """

    def __init__(self, ba_file_list, timer_in_seconds=None):
        super(BaOmxThread, self).__init__()
        self.ba_file_list = ba_file_list
        self.timer_in_seconds = timer_in_seconds
        self.name = "etoile_cinema"
        self.stoprequest = threading.Event()
        self.nextrequest = threading.Event()
        self.previousrequest = threading.Event()
        
        # initialise the stop file to True
        stop = True
        save_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.stop_file)
        pickle.dump(stop, open( save_file, "wb" ))


    def _display_slide(self, slide_path, display_duration):
        """ 
        function that displays the slide using feh command during 
        display_duration number of timer_in_seconds
        """
        try:
            logging.info("slide montre: %s" % slide_path)
            command = "export DISPLAY=:0;/usr/bin/feh --no-fehbg --bg-scale '" + slide_path +"'"
            return_code = subprocess.call(command, shell=True)
            if return_code == 0:
                target_time = time.time() + display_duration
                while time.time() < target_time and not self.stoprequest.isSet() \
                and not self.nextrequest.isSet() and not self.previousrequest.isSet():
                    sleep(0.5)
            else:
                raise RuntimeError("error when displaying the slide")

        except Exception as e:
            logging.error("command is: %s" % command)
            logging.error("display slide return code: %i" % return_code)
            logging.error('image display failed: %s' % str(e))

    def _play_ba(self, ba_path, time_status):
        """
        function qui lance une bande-annonce dans omx player
        """
        player = OMXPlayer(ba_path, args=['-o', 'hdmi', '-b', '--no-osd'])
        player.play()

        # affichage d'un ecran noir pour ne pas voir l'ecran de la ba precedente
        # brievement avant le changement d'ecran
        self._display_slide(env_variables.black_image, 1)
        logging.info("ba: %s, status: %s" % (ba_path, player.playback_status()))                        

        # tant que la ba n'est pas fini ou stoppee, on attend
        while True:
            try:
                if player.playback_status() == "Playing" and not self.stoprequest.isSet() \
                and time_status is False and not self.previousrequest.isSet() \
                and not self.nextrequest.isSet():
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

    def run(self):
        time_status = False
        logging.info("in run method")
    
        # tant que l'on a pas appuye sur "stopper les ba", on continue !
        env_variables.lock.acquire()
        # ajouter un check de la valeur de timer
        timeout = time.time() + self.timer_in_seconds

        while not self.stoprequest.isSet() and time_status is False:
            try:       
                i = 0
                
                while (i < len(self.ba_file_list)):

                    # si index negatif, on sort de la lecture
                    if (i < 0):
                        raise IndexError('negative index')
    
                    track = self.ba_file_list[i]
    
                    if isinstance(track, PlaylistElement):
                        # diffusion de la ba dans l'omx player
                        self._play_ba(track.ba_path, time_status)
                        # affichage du slide avec dates de diffusion entre deux bande-annonces
                        # si pendant le play de la ba, on appuie sur next, ne rien faire, le slide sera diffuse
                        if self.nextrequest.isSet():
                            self.nextrequest.clear()
                        if not self.stoprequest.isSet() and not self.previousrequest.isSet():
                            self._display_slide(track.slide_path, env_variables.temps_entre_2_ba)
    
                    elif isinstance(track, Slide):
                        # affichage de la promo
                        self._display_slide(track.filepath, env_variables.temps_affichage_promo)
    
                    elif isinstance(track, Ba):
                        # lancement de la ba seule e.g. carte fidelite dans l'omx player
                        self._play_ba(track.filepath, time_status)
    
                    time_status = time.time() > timeout
    
                    # sortie de la boucle for si stop = True
                    if self.stoprequest.isSet() or time_status:
                        break
    
                    # si next, clear du signal et on continue la boucle immediatement
                    if self.nextrequest.isSet():
                        i = i + 1
                        self.nextrequest.clear()
                        continue
    
                    # si previous, clear du signal et on continue la boucle immediatement
                    if self.previousrequest.isSet():
                        i = i - 1
                        self.previousrequest.clear()
                        continue              
    
                    # pas d'action: poursuite de la boucle while permettant de parcourir la playlist
                    i = i + 1
                
            except IndexError:
                # partie de code utilisee dans le cas:
                # on est dans la premiere ba et on clique sur previous
                # negative index, on sort
                break

        # fin de lecture
        env_variables.lock.release()

        # si demande d'arret, on remet le slide black pour ne pas rester sur le slide d'annonce
        logging.info("slide montre: %s" % env_variables.black_image)
        command_black = "export DISPLAY=:0;/usr/bin/feh --no-fehbg --bg-scale '" + env_variables.black_image +"'"
        subprocess.call(command_black, shell=True)

        if time_status is True:
            subprocess.call(['sudo', 'shutdown', '-h', 'now'])

    def next(self):
        self.nextrequest.set()

    def previous(self):
        self.previousrequest.set()

    def stop(self):
        self.stoprequest.set()

import threading
import subprocess
import time
import pickle
import os.path
import env_variables
from classes.content.PSlide import PSlide
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


class PlaylistThread(threading.Thread):
    """
    Thread qui fait tourner les ba et slides en boucle sur un player omx
    """

    def __init__(self, playlist, timer_in_seconds=None):
        super(PlaylistThread, self).__init__()
        self.playlist = playlist
        self.timer_in_seconds = timer_in_seconds
        self.name = "etoile_cinema"
        self.stoprequest = threading.Event()
        self.nextrequest = threading.Event()
        self.previousrequest = threading.Event()
        
        # initialise the stop file to True
        stop = True
        save_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.stop_file)
        pickle.dump(stop, open( save_file, "wb" ))


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
                
                while (i < len(self.playlist)):

                    # si index negatif, on sort de la lecture
                    if (i < 0):
                        raise IndexError('negative index')
    
                    track = self.playlist[i]
                    track.play(self)   
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
        black_slide = PSlide(env_variables.black_image, 0)
        black_slide.play(self)

        if time_status is True:
            subprocess.call(['sudo', 'shutdown', '-h', 'now'])

    def next(self):
        self.nextrequest.set()

    def previous(self):
        self.previousrequest.set()

    def stop(self):
        self.stoprequest.set()

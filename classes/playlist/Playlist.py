# -*- coding: utf-8 -*-
import sys
import os
if os.environ['HOME_BA'] not in sys.path:
    try:
        sys.path.append(os.environ['HOME_BA'])
    except:
        print("error in HOME_BA environment variable")


import time
import datetime
from time import mktime, strptime
import os.path
from random import shuffle
from classes.util.ListDir import ListDir
from classes.content.Trailer import Trailer
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


class Playlist():

    def __init__(self):
        self.movie_list = []
        self.slide_list = []
        self.playlist = self.make_playlist()
        logging.info("PLAYLIST APRES TOUTES LES INSERTIONS:\n %s" % (self))

    def __str__(self):
        chaine = ""
        for each in self.playlist:
            chaine += str(each) + "\n"
        return chaine

    def make_playlist(self):
        """
        fonction qui fabrique une playlist
        """

        playlist = []

        # lister les fichiers de /var/bande-annonces et creer les trailers
        self.movie_list = ListDir.list_directory(env_variables.ba_directory, 'mp4')
        self.slide_list = ListDir.list_directory(env_variables.ba_directory, 'jpg')

        for each_movie in self.movie_list:
            slidepath = os.path.splitext(each_movie)[0] + '.jpg'
            if slidepath in self.slide_list:
                trailer = Trailer(each_movie, slidepath)
                playlist = trailer.insert(playlist)

        if env_variables.random_play is True:
            shuffle(playlist)

        # lister les ecrans de promo et les ajouter a la playlist apres chaque trailer
        # slide_promo_list = ListDir.list_directory(env_variables.slide_promo_directory, 'jpg')

        # if slide_promo_list != []: 
        #     for each_promo in slide_promo_list:
        #         promo = PSlide(each_promo, env_variables.temps_affichage_promo)
        #         playlist = promo.insert(playlist)
        return playlist


if __name__ == '__main__':
    my_playlist = Playlist()
    print(my_playlist)


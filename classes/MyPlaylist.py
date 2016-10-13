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
import logging, logging.config
import env_variables
from classes.MyBaList import MyBaList, Ba
from classes.MySlideList import MySlideList, Slide
logging.config.dictConfig(env_variables.LOGGING)


class PlaylistElement():
    def __init__(self, ba_path, slide_path):
        self.ba_path = ba_path
        self.slide_path = slide_path

    def __str__(self):
        chaine = "["
        chaine += ",".join([self.ba_path, self.slide_path])
        chaine += "]"
        return chaine


class MyPlaylist():

    def __init__(self):
        self.ba_list = MyBaList()
        self.slide_list = MySlideList()
        self.playlist = self.make_playlist_to_run()
        logging.info("PLAYLIST APRES TOUTES LES INSERTIONS:\n %s" % (self))

    def __str__(self):
        chaine = "Playlist a jouer:\n"
        for each in self.playlist:
            if isinstance(each, PlaylistElement):
                chaine += each.ba_path + "\n" + each.slide_path + "\n"
            elif isinstance(each, Ba) or isinstance(each, Slide):
                chaine += each.filepath + "\n"
        return chaine

    def make_playlist_to_run(self):
        """
        fonction qui fabrique une playlist a partir de la ba_list, de la slide_list, insere les slides de promo
        """

        playlist = []

        # s'il y a un slide, on cree un PlaylistElement avec la ba et le slide correspondant
        # sinon, on ajoute la ba seule
        for each_ba in self.ba_list.ba_list_prog:
            slidename = each_ba.filename.split('.')[0] + '.jpg'
            if self.slide_list.slidename_is_in_slidelist_prog(slidename):
                slidepath = self.slide_list.get_slidepath_from_slidename(slidename)
                playlist.append(PlaylistElement(each_ba.filepath, slidepath))
            else:
                playlist.append(each_ba)

        # on ajoute a la playlist, les ecrans de promo apres chaque bande-annonce reelle 
        # (c'est a dire une bande annonce plus un slide)
        if env_variables.slide_promo_list != []: 
            new_playlist = []
            for each in playlist:
                if isinstance(each, PlaylistElement):
                    new_playlist.append(each)
                    new_playlist.extend(map(Slide, env_variables.slide_promo_list))
                else:
                    new_playlist.append(each)
            playlist = list(new_playlist)
        return playlist


if __name__ == '__main__':
    my_playlist = MyPlaylist()
    print(my_playlist)


# -*- coding: utf-8 -*-
import sys
import os
try:
    sys.path.append(os.environ['HOME_BA'])
except:
    print("error in HOME_BA environment variable")
from time import time, mktime, strptime
import logging, logging.config
import env_variables
logging.config.dictConfig(env_variables.LOGGING)


class MyList():

    def delete(self, mylist_list):
        """
        fonction qui efface les bande_annonces ou les slides
        """
        for each in mylist_list:
            if os.path.isfile(each.filepath):
                os.remove(each.filepath)


    def convert_files_into_list_of_dict(self, filepath_list):
        """
        fonction that converts a list of filepath [/media/usb/2016_8_26__titre_film1.mp4, /media/usb/2016_8_26__titre_film2.mp4]
        into a list of dict:
        [ {filepath: /media/usb/2016_8_26__titre_film1.mp4,
           end_date_epoch: epoch time}, 
          {filepath: /media/usb/2016_8_26__titre_film1.mp4,
           end_date_epoch: epoch time},  
        ]  
        """
        list_to_return = []
        for each in filepath_list:
            l_dict = {}
            each_end_date = strptime(os.path.basename(each).split("__")[0], "%Y_%m_%d")
            l_dict["end_date_epoch"] = mktime(each_end_date)
            l_dict["filepath"] = each
            list_to_return.append(l_dict)
        return list_to_return


    def select_playlist(self, mylist_list, criteria=None, **kwargs):
        """
        selectionne une playlist a partir d'un critere
        :param criteria: valeurs possibles: 'prog', 'all', 'past'
        * si criteria = 'prog', retourne la liste des ba dont la end_date n'a pas ete depassee
        * si criteria = 'all', retourne la liste de toutes les ba
        * si criteria = 'past', retourne la liste des ba donc la end_date est depassee
        """
        my_list_to_return = []
        if criteria == 'prog':
            try:
                for each in mylist_list:
                    if each.end_date_epoch > time():
                        my_list_to_return.append(each)
                logging.debug("select('prog')-liste programmee: %s" % ','.join(map(str, my_list_to_return)))
            except:
                logging.error("select('prog')-aucun fichier trouve")
                raise
        
        elif criteria == 'all':
            try:
                my_list_to_return = mylist_list
                logging.debug("select('all')-liste complete: %s" % ','.join(map(str, my_list_to_return)))
            except:
                logging.error("select('all')-aucun fichier trouve")
                raise   

        elif criteria == 'past':
            try:
                for each in mylist_list:
                    if each.end_date_epoch < time():
                        my_list_to_return.append(each)
                logging.debug("select('past')-liste dans le passe: %s" % ','.join(map(str, my_list_to_return)))
            except:
                logging.error("select('past')-aucun fichier trouves")
                raise   

        else:
            logging.error('criteria is not prog or all')    

        return my_list_to_return


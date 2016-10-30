# -*- coding: utf-8 -*-
import sys
import os
if os.environ['HOME_BA'] not in sys.path:
    try:
        sys.path.append(os.environ['HOME_BA'])
    except:
        print("error in HOME_BA environment variable")
import logging, logging.config
from time import mktime, strptime
from random import shuffle
import env_variables
from classes.MyList import MyList
logging.config.dictConfig(env_variables.LOGGING)


class Ba():
    """ class pour un seul bande annonce """

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.end_date = self.filename.split("__")[0]
        self.end_date_epoch = mktime(strptime(self.end_date, "%Y_%m_%d"))

    def __str__(self):
        chaine = "["
        chaine += ','.join([self.filepath, self.end_date])
        chaine += "]"
        return chaine



class MyBaList(MyList):

    def __init__(self):
        self.ba_list_prog = self.select_playlist(self.listdir_fullpath_ba(env_variables.ba_directory), 'prog')
        if env_variables.random_play is True:
            shuffle(self.ba_list_prog)
        self._insert_carte_fidelite()
        self.ba_list_in_past = self.select_playlist(self.listdir_fullpath_ba(env_variables.ba_directory), 'past')
        self.ba_list_all = self.select_playlist(self.listdir_fullpath_ba(env_variables.ba_directory), 'all')

    def __str__(self):
        chaine = "Toutes les BA:\n"
        chaine += '\n'.join(map(str, self.ba_list_all)) + "\n\n"
        chaine += "BAs en programmation:\n"
        chaine += '\n'.join(map(str, self.ba_list_prog)) + "\n\n"
        chaine += "BAs dans le passe:\n"
        chaine += '\n'.join(map(str, self.ba_list_in_past)) + "\n\n"
        return chaine

    def listdir_fullpath_ba(self, d):
        """
        fonction qui liste le directory et verifie que la date est separee par un __
        et que le nom du fichier commence par un 2
        les fichiers doivent s'appeler en 201x_xx_xx__titre.mp4
        :param d: directory path
        :type d: string
        """
        ba_list = []
        # verification que le fichier commence par un 2 et que la date est separee
        # du reste du nom de fichier par "__"
        for filename in os.listdir(d):
            try:
                if filename.split("__")[0][0] == '2' and filename.split(".")[-1] == 'mp4':
                    new_ba = Ba(os.path.join(d,filename))
                    ba_list.append(new_ba)
            except:
                raise
        return ba_list

    def _insert_carte_fidelite(self):
        """
        insere le film sur les cartes de fidelite dans la playlist
        """
        if env_variables.ba_carte_fidelite != '' and env_variables.ba_carte_fidelite is not None:
            i = 0
            new_ba_list = [Ba(env_variables.ba_carte_fidelite)]
            for each in self.ba_list_prog:
                if i < env_variables.nbre_ba_entre_deux_carte_fidelite:
                    new_ba_list.append(each)
                else:
                    if i % env_variables.nbre_ba_entre_deux_carte_fidelite == 0:
                        new_ba_list.append(Ba(env_variables.ba_carte_fidelite))
                        new_ba_list.append(each)
                    else:
                        new_ba_list.append(each)
                i = i + 1
            self.ba_list_prog = new_ba_list
        logging.debug("liste des ba apres insertion carte fidelite: %s" % ','.join(map(str,self.ba_list_prog)))
        


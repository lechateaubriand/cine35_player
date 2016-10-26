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
import env_variables
from classes.MyList import MyList
logging.config.dictConfig(env_variables.LOGGING)


class Slide():
    """ class pour un seul slide """

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



class MySlideList(MyList):
    """ class pour une liste de slide """

    def __init__(self, directory=env_variables.ba_directory):
        self.slide_list_prog = self.select_playlist(self.listdir_fullpath_slide(directory), 'prog')
        self.slide_list_in_past = self.select_playlist(self.listdir_fullpath_slide(directory),'past')
        self.slide_list_all = self.select_playlist(self.listdir_fullpath_slide(directory),'all')

    def __str__(self):
        chaine = "Tous les slides:\n"
        chaine += '\n'.join(map(str, self.slide_list_all)) + "\n\n"
        chaine += "Slides en programmation:\n"
        chaine += '\n'.join(map(str, self.slide_list_prog)) + "\n\n"
        chaine += "Slides dans le passe:\n"
        chaine += '\n'.join(map(str, self.slide_list_in_past)) + "\n\n"
        return chaine

    def listdir_fullpath_slide(self, d):
        """
        fonction qui liste le directory et verifie que la date est separee par un __
        et que le nom du fichier commence par un 2
        les fichiers doivent s'appeler en 201x_xx_xx__titre.jpg
        :param d: directory path
        :type d: string
        """
        slide_list = []
        # verification que le fichier commence par un 2 et que la date est separee
        # du reste du nom de fichier par "__"
        for filename in os.listdir(d):
            try:
                if filename.split("__")[0][0] == '2' and filename.split(".")[-1] == 'jpg':
                    new_slide = Slide(os.path.join(d, filename))
                    slide_list.append(new_slide)
            except:
                pass
        return slide_list

    def _filename_based_generator_on_slidelist_prog(self):
        """ 
        generateur qui retourne les filename des slides de self.slide_list_prog 
        """
        for each_slide in self.slide_list_prog:
            yield each_slide.filename

    def slidename_is_in_slidelist_prog(self, slidename):
        """
        function that returns true if the a Slide object with a 
        Slide.slidename == slidename exists in self.slide_list_prog
        """
        if slidename in self._filename_based_generator_on_slidelist_prog():
            return True
        else:
            return False

    def get_slidepath_from_slidename(self, slidename):
        """
        function that looks into self.slide_list_prog and returns the slidepath corresponding to the slidename
        """
        for slide in self.slide_list_prog:
            if slide.filename == slidename:
                return slide.filepath
        return False

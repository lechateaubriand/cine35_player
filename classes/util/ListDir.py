import os.path
from time import time, strptime, mktime


class ListDir:

    @staticmethod
    def list_directory(directory, extension):
        """
        fonction qui liste le directory et verifie que la date est separee par un __
        et que le nom du fichier commence par un 2
        les fichiers doivent s'appeler en 201x_xx_xx__titre.mp4
        :param extension: extension of the files to list (e.g. mp4, jpg)
        :param directory: directory path
        """
        file_list = []
        # verification que le fichier commence par un 2 et que la date est separee
        # du reste du nom de fichier par "__"
        for filename in os.listdir(directory):
            if filename.split("__")[0][0] == '2' and filename.split(".")[-1] == extension:
                file_list.append(os.path.join(directory, filename))
        return file_list

    @staticmethod
    def list_directory_in_past(directory, extension, time_condition = 'past'):
        """
        fonction qui liste le directory et verifie que la date est separee par un __
        et qu'elle est dans le passe
        :param extension: extension des fichiers a lister (e.g. mp4, jpg)
        :param directory: chemin du repertoire
        :param time_condition: 'past' or 'future', indique si les fichiers retournes 
                                doivent etre ceux dont la end_date est depasse ou pas
        :return list: retourne une liste des fichiers qui sont passes
        """
        file_list = []
        # verification que le fichier commence par un 2 et que la date est separee
        # du reste du nom de fichier par "__" et qu'elle est dans le passe
        for filename in os.listdir(directory):
            end_date = strptime(filename.split("__")[0], "%Y_%m_%d")
            end_date_epoch = mktime(end_date)
            if time_condition == 'past' and end_date_epoch < time() and filename.split(".")[-1] == extension:
                file_list.append(os.path.join(directory, filename))
            elif time_condition == 'future' and end_date_epoch > time() and filename.split(".")[-1] == extension:
                file_list.append(os.path.join(directory, filename))
        return file_list

    @staticmethod
    def delete(mylist):
        """
        fonction qui efface les fichiers listes
        :param mylist: liste des fichiers a effacer (path des fichiers)
        """
        for each in mylist:
            if os.path.isfile(each):
                os.remove(each)

    @staticmethod
    def convert_files_into_list_of_dict(filepath_list):
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

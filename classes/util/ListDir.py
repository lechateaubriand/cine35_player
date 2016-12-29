import os.path


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
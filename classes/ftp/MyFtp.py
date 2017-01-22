import os
import time
import datetime
import env_variables
from classes.util.ListDir import ListDir
from ftplib import FTP
from simplecrypt import encrypt, decrypt
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)
import pickle


class MyFtp(FTP):

    def __init__(self):
        FTP.__init__(self, env_variables.ftp_server)
        try:
            self.login(env_variables.ftp_login, self._get_word())
        except Exception:
            logging.error("could not log in on FTP server", exc_info=True)
            raise RuntimeError("error when logging to ftp server")

    def __del__(self):
        self.quit()

    def _get_word(self):
        """ function used to get file from ftp server"""
        with open(env_variables.ftp_bapd_file, 'rb') as f:
            unpick = pickle.Unpickler(f)
            unpick_data = unpick.load()
        in_bytes = decrypt('etoilecinema', unpick_data)
        return str(in_bytes,'utf-8')

    def download_trailer_from_ftpserver(self):
        """
        this function downloads mp4 and corresponding slides from the ftp server.
        """
        logging.info("in download_ba_from_ftp server")

        # get the file names already in trailer_directory into a list
        # they shall not be downloaded again
        my_trailer_list = ListDir.list_directory(env_variables.trailer_directory, 'mp4')
        local_trailer_list = [ os.path.basename(x) for x in my_trailer_list ]

        # get the list of files
        os.chdir(env_variables.trailer_directory) #changes the active dir - this is where downloaded files will be saved to

        ftp_files_mp4 = self.nlst(env_variables.ftp_filematch) # filter the file listing
        logging.info("list of files on ftp server: %s" % ftp_files_mp4)

        converted_ftp_files_mp4 = ListDir.convert_files_into_list_of_dict(ftp_files_mp4)
        # ne pas selectionner les bande annonce qui seraient dans le passe
        ftp_files_in_future = [each["filepath"] for each in converted_ftp_files_mp4 if each["end_date_epoch"] > time.time()]
        # ne pas selectionner les bande annonces que l'on a deja charge
        ftp_files_to_download = [file_mp4 for file_mp4 in ftp_files_in_future if file_mp4 not in local_trailer_list]
        logging.info("list of files on ftp server eligible for download: %s" % ftp_files_mp4)


        for filename_mp4 in ftp_files_to_download[:env_variables.nb_files_per_boot]: # Loop - looking for matching files
            # download the mp4 file
            logging.info('Getting ' + filename_mp4)
            fhandle = open(filename_mp4, 'wb')
            self.retrbinary('RETR ' + filename_mp4, fhandle.write)
            fhandle.close()

            # download corresponding slide
            filename_jpg = '.'.join([filename_mp4.split('.')[0], 'jpg'])
            logging.info('Getting ' + filename_jpg)
            try:
                fhandle = open(filename_jpg, 'wb')
                self.retrbinary('RETR ' + filename_jpg, fhandle.write)
                fhandle.close()

            except Exception:
                logging.error("Could not download {} from ftp server".format(filename_jpg), exc_info=True)

    def delete_past_trailer_in_ftpserver(self):
        """
        this function deletes one mp4 file and its corresponding slide on ftp server
        :param ftp: an opened ftp session
        :type ftp: ftplib.FTP client
        """
        logging.info("in delete_past_ba_in_ftpserver")

        self.cwd('/')
        self.cwd(env_variables.ftp_home_dir)

        ftp_files_mp4 = self.nlst(env_variables.ftp_filematch) # filter the file listing
        logging.info("list of files on ftp server: %s" % ftp_files_mp4)

        # select only file which end_date is in the past
        converted_ftp_files_mp4 = ListDir.convert_files_into_list_of_dict(ftp_files_mp4)
        trailer_list_filtered = [each["filepath"] for each in converted_ftp_files_mp4 if each["end_date_epoch"] < time.time()]
        logging.info("list of files on ftp server eligible for deletion: %s" % trailer_list_filtered)

        # delete only one ba and its slide per boot on ftp server
        try:
            filename_mp4 = trailer_list_filtered[0]
            logging.info('Deleting ' + filename_mp4) #for confort sake, shows the file that's being retrieved
            try:
                self.delete(filename_mp4)
            except:
                logging.error("could not delete file %s on ftp server" % filename_mp4, exc_info=True)
        
            filename_jpg = '.'.join([filename_mp4.split('.')[0], 'jpg'])
            logging.info('Deleting ' + filename_jpg) #for confort sake, shows the file that's being retrieved
            try:
                self.delete(filename_jpg)
            except:
                logging.error("could not delete file %s on ftp server" % filename_jpg)
        except IndexError:
            logging.info("no ba in the past to delete on FTP server")


    def upload_log_file(self):
        logging.info("upload log file to server")

        try:
            movie_list = ListDir.list_directory(env_variables.trailer_directory, 'mp4')
            slide_list = ListDir.list_directory(env_variables.trailer_directory, 'jpg')
            write_in_file = self._print_file_list(movie_list, slide_list)

            self.cwd('/')
            self.cwd(env_variables.ftp_upload_dir)
            
            with open(env_variables.ftp_uploaded_file, 'wb') as file:
                file.write(write_in_file)

            with open(env_variables.ftp_uploaded_file,'rb') as file:
                self.storlines('STOR cine35_player.log', file)
        except:
            logging.error("could not write or send file %s on ftp server" % env_variables.ftp_uploaded_file)
            raise

    def _print_file_list(self, movie_list, slide_list):
        now = datetime.datetime.now()
        to_return = str(now)
        to_return += "\nmovies:\n"
        for file in movie_list:
            to_return += file + "\n"

        to_return += "\nslides:\n"
        for file in slide_list:
            to_return += file + "\n"

        return to_return

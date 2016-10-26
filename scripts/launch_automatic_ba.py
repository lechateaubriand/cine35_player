import sys
import os
try:
    sys.path.append(os.environ['HOME_BA'])
except:
    print("error in HOME_BA environment variable")
import env_variables
from classes.MyFtpClass import MyFtpClass
from classes.MyBaList import MyBaList
from classes.MySlideList import MySlideList
from classes.MyPlaylist import MyPlaylist
from classes.MyBaThread import BaOmxThread
from random import shuffle
import logging
import logging.config
logging.config.dictConfig(env_variables.LOGGING)


def ftp_server_operation():
    """
    fonction qui charge les bande-annonces depuis le serveur ftp et nettoie le serveur ftp
    """
    try:
        ftp = MyFtpClass()
        ftp.cwd(env_variables.ftp_home_dir)
    except RuntimeError:
        return
    except Exception:
        logging.error("erreur de connection au serveur ftp", exc_info=True)
        return
    
    try:
        ftp.download_ba_from_ftpserver()
    except Exception:
        logging.error("erreurs en essayant de deleter les bande-annonces sur le serveur FTP", exc_info=True)

    try:
        ftp.delete_past_ba_in_ftpserver()
    except Exception:
        logging.error("erreurs en essayant de deleter les bande-annonces sur le serveur FTP", exc_info=True)


def clean():
    my_ba_list = MyBaList()
    my_slide_list = MySlideList()
    my_slide_promo_list = MySlideList(env_variables.slide_promo_directory)

    try:
        my_ba_list.delete(my_ba_list.ba_list_in_past)
    except:
        logging.error("erreurs en essayant de deleter les bande-annonces locales")
        print("erreurs en essayant de deleter les bande-annonces locales")

    try:
        my_slide_list.delete(my_slide_list.slide_list_in_past)
    except:
        logging.error("erreurs en essayant de deleter les slides locaux")
        print("erreurs en essayant de deleter les slides locaux")

    try:
        my_slide_list.delete(my_slide_promo_list.slide_list_in_past)
    except:
        logging.error("erreurs en essayant de deleter les slides de promo")
        print("erreurs en essayant de deleter les slides de promo")
        

def main():
    logging.info('################################')
    logging.info('#### PROCEDURE DEMARRAGE #######')
    logging.info('################################')
    playlist = MyPlaylist().playlist
    if env_variables.omx is True:
        if not env_variables.lock.locked():
            omx_thread = BaOmxThread(playlist, timer_in_seconds=env_variables.ba_timer)
            omx_thread.start()


if __name__ == "__main__":

    if env_variables.ftp is True:
        ftp_server_operation()
    clean()
    main()
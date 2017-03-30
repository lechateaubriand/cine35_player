# -*- coding: utf-8 -*-
import sys
import os
if os.environ['HOME_BA'] not in sys.path:
    try:
        sys.path.append(os.environ['HOME_BA'])
    except:
        print("error in HOME_BA environment variable")
import pickle
from classes.ftp.MyFtp import MyFtp
from classes.playlist.Playlist import Playlist
from classes.thread.PlaylistThread import PlaylistThread
from classes.thread.Watcher import Watcher
from classes.util.ListDir import ListDir
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


def ftp_server_operation():
    """
    fonction qui charge les bande-annonces depuis le serveur ftp et nettoie le serveur ftp
    """
    try:
        ftp = MyFtp()
        ftp.cwd(env_variables.ftp_home_dir)
    except RuntimeError:
        return
    except Exception:
        logging.error("erreur de connection au serveur ftp", exc_info=True)
        return
    
    try:
        ftp.download_trailer_from_ftpserver()
    except Exception:
        logging.error("erreurs en essayant de deleter les bande-annonces sur le serveur FTP", exc_info=True)

    try:
        ftp.delete_past_trailer_in_ftpserver()
    except Exception:
        logging.error("erreurs en essayant de deleter les bande-annonces sur le serveur FTP", exc_info=True)

    try:
        ftp.upload_log_file()
    except Exception:
        logging.error("erreurs en essayant d'uploader le fichier sur le serveur FTP", exc_info=True)


def clean():
    """
    fonction qui enleve les bande-annonces qui sont dans le passe
    """
    try:
        movie_in_past = ListDir.list_directory_in_past(env_variables.trailer_directory, 'mp4', 'past')
        ListDir.delete(movie_in_past)
    except Exception as e:
        logging.error("erreur en essayant de deleter les bande-annonces passees: %s" % str(e))

    try:
        slide_in_past = ListDir.list_directory_in_past(env_variables.trailer_directory, 'jpg', 'past')
        ListDir.delete(slide_in_past)
    except Exception as e:
        logging.error("erreur en essayant de deleter les slides passes: %s" % str(e))

    try:
        looped_movie_in_past = ListDir.list_directory_in_past(env_variables.looped_movie_directory, 'mp4', 'past')
        ListDir.delete(looped_movie_in_past)
    except Exception as e:
        logging.error("erreur en essayant de deleter les looped movies passes: %s" % str(e))

    try:
        looped_slide_in_past = ListDir.list_directory_in_past(env_variables.looped_slide_directory, 'jpg', 'past')
        ListDir.delete(looped_slide_in_past)
    except Exception as e:
        logging.error("erreur en essayant de deleter les looped slides passes: %s" % str(e))



def main():
    logging.info('################################')
    logging.info('#### PROCEDURE DEMARRAGE #######')
    logging.info('################################')
    playlist = Playlist().playlist
    if env_variables.omx is True:
        if not env_variables.lock.locked():
            # stockage de la playlist en cours pour le site web
            web_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.playlist_file)
            playlist_file = [x.filename for x in playlist]
            pickle.dump(web_file, open(playlist_file, "wb"))

            # initialisation a stop = False pour le fichier stop.p
            stop = True
            save_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.stop_file)
            pickle.dump(stop, open( save_file, "wb" ))

            # lancement des lectures
            omx_thread = PlaylistThread(playlist, timer_in_seconds=env_variables.shutdown_timer)
            watcher = Watcher(omx_thread)
            watcher.start()


if __name__ == "__main__":

    if env_variables.ftp is True:
        ftp_server_operation()
    clean()
    main()
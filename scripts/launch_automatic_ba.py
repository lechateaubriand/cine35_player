import pickle
from classes.ftp.MyFtp import MyFtp
from classes.playlist.Playlist import Playlist
from classes.thread.PlaylistThread import PlaylistThread
from classes.thread.Watcher import Watcher
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
        ftp.download_ba_from_ftpserver()
    except Exception:
        logging.error("erreurs en essayant de deleter les bande-annonces sur le serveur FTP", exc_info=True)

    try:
        ftp.delete_past_ba_in_ftpserver()
    except Exception:
        logging.error("erreurs en essayant de deleter les bande-annonces sur le serveur FTP", exc_info=True)


def main():
    logging.info('################################')
    logging.info('#### PROCEDURE DEMARRAGE #######')
    logging.info('################################')
    playlist = Playlist().playlist
    if env_variables.omx is True:
        if not env_variables.lock.locked():
            # initialisation a stop = False pour le fichier stop.p
            stop = True
            save_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.stop_file)
            pickle.dump(stop, open( save_file, "wb" ))

            # lancement des lectures
            omx_thread = PlaylistThread(playlist, timer_in_seconds=env_variables.ba_timer)
            watcher = Watcher(omx_thread)
            watcher.start()


if __name__ == "__main__":

    if env_variables.ftp is True:
        ftp_server_operation()
#    clean()
    main()
import os.path
import pickle
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


def main():
    stop = True
    save_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.stop_file)
    pickle.dump(stop, open( save_file, "wb" ))
    logging.info('#### PROCEDURE ARRET CLASSIQUE SANS SHUTDOWN--- arret playlist par bouton stop de telecommande')




if __name__ == "__main__":
    main()
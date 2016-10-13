import sys
import os
import subprocess
try:
    sys.path.append(os.environ['HOME_BA'])
except:
    print("error in HOME_BA environment variable")
import pickle
import env_variables
import logging
import logging.config
logging.config.dictConfig(env_variables.LOGGING)


def main():
    stop = True
    save_file = os.path.join(env_variables.home_ba, 'save.p')
    pickle.dump(stop, open( save_file, "wb" ))
    logging.info('#### PROCEDURE ARRET CLASSIQUE SANS SHUTDOWN--- arret playlist par bouton stop de telecommande')




if __name__ == "__main__":
    main()
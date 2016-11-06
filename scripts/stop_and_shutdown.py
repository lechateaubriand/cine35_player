import sys
import os
import pickle
import subprocess
try:
    sys.path.append(os.environ['HOME_BA'])
except:
    print("error in HOME_BA environment variable")
import env_variables
from time import sleep
import logging
import logging.config
logging.config.dictConfig(env_variables.LOGGING)


def stop():
    stop = True
    save_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.stop_file)
    pickle.dump(stop, open( save_file, "wb" ))
    logging.info('#### PROCEDURE ARRET CLASSIQUE --- arret playlist par bouton wakeup de telecommande')

def shutdown():
    logging.info('#### PROCEDURE ARRET CLASSIQUE --- shutdown par bouton wakeup de telecommande')
    subprocess.call(['sudo', 'shutdown', '-h', 'now'])



if __name__ == "__main__":
    stop()
    sleep(3)
    shutdown()
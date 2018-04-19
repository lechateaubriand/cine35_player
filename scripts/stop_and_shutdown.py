import os.path
import pickle
import subprocess
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


def stop():
    stop = True
    save_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.stop_file)
    pickle.dump(stop, open( save_file, "wb" ))
    logging.info('#### PROCEDURE ARRET CLASSIQUE --- arret playlist par bouton wakeup de telecommande')

def shutdown():
    logging.info('#### PROCEDURE ARRET CLASSIQUE --- shutdown par bouton wakeup de telecommande')
    subprocess.call(['sudo', 'shutdown', '-P', 'now'])

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
    save_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.next_file)
    pickle.dump(True, open(save_file, "wb" ))
    logging.info('#### NEXT BANDE ANNONCE depuis bouton de telecommande')




if __name__ == "__main__":
    main()
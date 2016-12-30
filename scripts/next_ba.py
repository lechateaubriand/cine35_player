import os.path
import pickle
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


def main():
    next_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.next_file)
    pickle.dump(True, open(next_file, "wb" ))
    logging.info('#### NEXT BANDE ANNONCE depuis bouton de telecommande')




if __name__ == "__main__":
    main()
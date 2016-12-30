import os
import pickle
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


def main():
    previous_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.previous_file)
    pickle.dump(True, open(previous_file, "wb" ))
    logging.info('#### PREVIOUS BANDE ANNONCE depuis bouton de telecommande')


if __name__ == "__main__":
    main()
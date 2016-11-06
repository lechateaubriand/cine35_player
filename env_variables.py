import sys
import os
import threading

################
#  DIRECTORIES
################
home_ba = '/home/pi/my_envs/cine35_lecteur_ba'
ba_directory = '/var/bande_annonces'
ba_timer = 5400

################
# FILES TO CONTROL OMX PLAYER
################
stopnextprevious_dir = os.path.join(home_ba, 'play_files')
next_file = 'next.p'
previous_file = 'previous.p'
stop_file = 'stop.p'

################
# DIVERS
################
omx = True
ba_carte_fidelite = '/var/bande_annonces_static/2025_12_01__carte_fidelite.mp4'
nbre_ba_entre_deux_carte_fidelite = 2
random_play = True


################
# SLIDES
################
# temps d'affichage du slide annoncant les dates:
temps_entre_2_ba = 7
black_image = '/var/bande_annonces_static/black.jpg'
# slides de promo
slide_promo_directory = '/var/bande_annonces_slide_promo'
temps_affichage_promo = 7


################
# FTP SERVER
################
ftp = False
ftp_server = 'ftp.cluster003.ovh.net'
ftp_port = '21'
ftp_login = 'jurocozoue'
ftp_home_dir = 'bande_annonces'
ftp_filematch = '*.mp4'
nb_files_per_boot = 2


################
#  LOGS
################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default_formatter': {
            'format': '%(asctime)s : %(levelname)s : %(message)s',
            'datefmt': '%d-%b-%Y %H:%M:%S'
            },
        },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
            'stream': sys.stdout,
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default_formatter',
            'filename': '/var/log/cine35_lecteur_ba/cine35_lecteur_ba.log',
            'maxBytes': 50000,
            'backupCount': 3,
        }
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO'
    }
}


################
# MULTITHREAD
################
lock = threading.Lock()


import sys
import os
import threading

################
#  DIRECTORIES
################
home_player = '/home/pi/my_envs/cine35_player'
trailer_directory = '/var/cine35/trailer'
shutdown_timer = 5400


################
# FILES TO CONTROL OMX PLAYER
################
stopnextprevious_dir = os.path.join(home_player, 'play_files')
next_file = 'next.p'
previous_file = 'previous.p'
stop_file = 'stop.p'
playlist_file = 'playlist.p'


################
# DIVERS
################
omx = True
# image name shall respect YYYY_MM_DD__name.jpg
background_image = os.path.join(home_player, 'static', 'black.jpg')


################
# TRAILER
################
trailer_slide_duration = 7
random_play = True


################
# LOOPED MOVIES
################
looped_movie_directory = '/var/cine35/looped_movie'


################
# LOOPED SLIDES
################
looped_slide_directory = '/var/cine35/looped_slide'
looped_slide_duration = 7


################
# FTP SERVER
################
ftp = False
ftp_server = ''
ftp_port = '21'
ftp_login = ''
ftp_home_dir = 'bande_annonces'
ftp_upload_dir = 'logs'
ftp_filematch = '*.mp4'
nb_files_per_boot = 2
ftp_bapd_file = ''
ftp_uploaded_file = '/var/log/cine35_player/list_of_directories.log'


################
#  LOGS
################
log_file = "/var/log/cine35_player/cine35_player.log"
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
            'filename': log_file,
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


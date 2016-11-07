import sys
import os
try:
    sys.path.append(os.environ['HOME_BA'])
except:
    print("error in HOME_BA environment variable")
import env_variables
from scripts import launch_automatic_ba, stop_and_shutdown, stop_automatic_ba, previous_ba, next_ba
from time import sleep
import logging
import logging.config
logging.config.dictConfig(env_variables.LOGGING)
import lirc

lirc.init('telecommande', blocking=False)
while True:
    ircode = lirc.nextcode()
    print(ircode)
    if len(ircode) != 0:

        if ircode[0] == 'play':
            print("PLAY")
            logging.info('play_ba depuis appui play / ok telecommande')
            logging.info("env_variables.lock.locked = %s" % env_variables.lock.locked())
            if not env_variables.lock.locked():
                launch_automatic_ba.main()

        elif ircode[0] == 'stop':
            print("STOP")
            logging.info('stop_ba depuis appui stop / ok telecommande')
            stop_automatic_ba.main()

        elif ircode[0] == 'next':
            print("NEXT")
            logging.info('next ba depuis telecommande')
            next_ba.main()

        elif ircode[0] == 'previous':
            print("PREVIOUS")
            logging.info('previous ba depuis telecommande')
            previous_ba.main()
        
        elif ircode[0] == 'shutdown':
            print("SHUTDOWN")
            logging.info('stop_ba puis shutdown depuis appui wakeup telecommande')
            stop_and_shutdown.stop()
            sleep(3)
            stop_and_shutdown.shutdown()
            break
    else:
        pass
lirc.deinit()

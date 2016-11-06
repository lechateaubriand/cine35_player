# -*- coding: utf-8 -*-
import time
import threading
import os.path
import logging, logging.config
import env_variables
import pickle
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
logging.config.dictConfig(env_variables.LOGGING)


class Watcher(threading.Thread):

    def __init__(self, ba_thread):
        self.observer = Observer()
        self.ba_thread = ba_thread

    def run(self):
        """
        this function starts the tread that will play the playlist
        then it launch the watching of stop.p, previous.p and next.p files
        """
        self.ba_thread.start()
        
        # indicate the ba are played
        stop = False
        save_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.stop_file)
        pickle.dump(stop, open( save_file, "wb" ))

        event_handler = Handler(self.ba_thread)
        self.observer.schedule(event_handler, env_variables.stopnextprevious_dir)
        self.observer.start()
        try:
            # watching the files through observer will happen
            # until the player thread has ended its job
            self.ba_thread.join()
            self.observer.stop()
        except Exception:
            self.observer.stop()
            logging.debug("Watcher stopped")
        # wait for the closing of the observer
        self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, ba_thread):
        super(Handler, self).__init__()
        self.ba_thread = ba_thread

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(env_variables.next_file):
            self.ba_thread.next()

        if not event.is_directory and event.src_path.endswith(env_variables.previous_file):
            self.ba_thread.previous()

        if not event.is_directory and event.src_path.endswith(env_variables.stop_file):
            self.ba_thread.stop()

# -*- coding: utf-8 -*-
import threading
import os.path
import pickle
import env_variables
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


class Watcher(threading.Thread):

    def __init__(self, playlist_thread):
        super(Watcher, self).__init__()
        self.observer = Observer()
        self.playlist_thread = playlist_thread

    def run(self):
        """
        this function starts the tread that will play the playlist
        then it launch the watching of stop.p, previous.p and next.p files
        """
        logging.info("watcher started")
        self.playlist_thread.start()
        
        # indicate the ba are played
        stop = False
        save_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.stop_file)
        pickle.dump(stop, open( save_file, "wb" ))

        event_handler = Handler(self.playlist_thread)
        self.observer.schedule(event_handler, env_variables.stopnextprevious_dir)
        self.observer.start()
        try:
            # watching the files through observer will happen
            # until the player thread has ended its job
            self.playlist_thread.join()
            self.observer.stop()
        except Exception:
            self.observer.stop()
            logging.debug("Watcher stopped")
        # wait for the closing of the observer
        self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, playlist_thread):
        super(Handler, self).__init__()
        self.playlist_thread = playlist_thread

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(env_variables.next_file):
            self.playlist_thread.next()

        if not event.is_directory and event.src_path.endswith(env_variables.previous_file):
            self.playlist_thread.previous()

        if not event.is_directory and event.src_path.endswith(env_variables.stop_file):
            self.playlist_thread.stop()

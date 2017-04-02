# -*- coding: utf-8 -*-
from classes.content.IContent import IContent
from classes.content.Movie import Movie
from classes.content.Slide import Slide
from classes.insert.InsertAtEnd import InsertAtEnd
from classes.play.PlayTrailer import PlayTrailer
import env_variables
import logging, logging.config
logging.config.dictConfig(env_variables.LOGGING)


class Trailer(IContent):

    def __init__(self, movie_filepath, slide_filepath):
        super(Trailer, self).__init__(InsertAtEnd(), PlayTrailer())
        self.movie = Movie(movie_filepath)
        self.slide = Slide(slide_filepath, env_variables.trailer_slide_duration)

    def __str__(self):
        to_print = str(self.movie) + "\n"
        to_print += str(self.slide)
        return to_print

    def get_filename(self):
        return self.movie.filename.extend(self.slide.filename)

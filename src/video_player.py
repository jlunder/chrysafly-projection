from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

from logging import getLogger

import evento
from datetime import datetime
import logging


class omxPlayerMock():
    '''
    Mock class for instantiating when a video/audio file is not available
    The idea is to keep all code pertaining to omxPlayer while allowing
    for instances of OmxDmx without an actual OMXPlayer.
    '''

    def __init__(self, filename):
        self.logger = logging.getLogger("omxPlayerMock")
        self.logger.info("Mock OMXPlayer class initiated")

        self.pauseEvent = evento.event.Event()
        self.playEvent = evento.event.Event()
        self.stopEvent = evento.event.Event()
        self.exitEvent = evento.event.Event()
        self.seekEvent = evento.event.Event()
        self.positionEvent = evento.event.Event()

        self.playbackStatus = "Stopped"  # ("Playing" | "Paused" | "Stopped")
        self.start_time = datetime.utcnow() # keep track of when mock system started "playing"

    def hide_video(self):
        pass

    def pause(self):
        self.playbackStatus = "Paused"
        self.pauseEvent(self)

    def play(self):
        self.playbackStatus = "Playing"
        self.start_time = datetime.utcnow()
        self.logger.debug("start_time = {0}".format(self.start_time.timestamp()))
        self.playEvent(self)

    def position(self):
        current_position = float((datetime.utcnow() - self.start_time).total_seconds())
        self.logger.debug("current_position = {0}".format(current_position))
        return current_position

    def stop(self):
        self.playbackStatus = "Stopped"
        self.stopEvent(self)

    def exit(self):
        self.exitEvent(self)

    def seek(self, val):
        self.seekEvent(self)

    def playback_status(self):
        return self.playbackStatus

    def show_video(self):
        pass

    def duration(self):
        return (sys.maxsize)  # always greater than position()

    def quit(self):
        pass


class VideoPlayer:

    logger = getLogger()

    def __init__(self, video_file):
        self.video_file = video_file
        VIDEO_PATH = Path(video_file)
        try:
            self.player = OMXPlayer(VIDEO_PATH, dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=['-b', '-o', 'both'])
        except Exception:
            self.player = omxPlayerMock(VIDEO_PATH)

    def play_step(self, step):
        play_range(self.step_start, self.step_end)

    def play_range(self, start, end):
        if start > end:
            raise Exception('start cant be greater than end')

        self.player.seek_to(start)
        self.player.play()

        while self.player.position() < end:
            sleep(50)


    def play_steps(self, observable):
        #start at starting index

        #play until ending index

        observable.subscribe(self.play_step)

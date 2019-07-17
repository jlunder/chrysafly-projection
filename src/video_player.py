from pathlib import Path
from time import sleep

from logging import getLogger

import evento
from datetime import datetime, timedelta
import logging
import  rx
from rx import operators as ops
from rx.core import pipe


class OmxPlayerMock:
    '''
    Mock class for instantiating when a video/audio file is not available
    The idea is to keep all code pertaining to omxPlayer while allowing
    for instances of OmxDmx without an actual OMXPlayer.
    '''

    def __init__(self, filename):
        self.logger = logging.getLogger('omxPlayerMock')
        self.logger.info('Mock OMXPlayer class initiated')

        self.pauseEvent = evento.event.Event()
        self.playEvent = evento.event.Event()
        self.stopEvent = evento.event.Event()
        self.exitEvent = evento.event.Event()
        self.seekEvent = evento.event.Event()
        self.positionEvent = evento.event.Event()

        self.playbackStatus = 'Stopped'  # ('Playing' | 'Paused' | 'Stopped')
        self.start_time = None

        self.play()

    def hide_video(self):
        pass

    def pause(self):
        self.logger.info('Pause')
        self.playbackStatus = 'Paused'
        self.pauseEvent(self)

    def play(self):
        self.logger.info('Playing')
        self.playbackStatus = 'Playing'
        self.start_time = datetime.utcnow()
        self.logger.debug('start_time = {0}'.format(self.start_time.timestamp()))
        self.playEvent(self)

    def position(self):
        if not self.start_time:
            return 0

        current_position = float((datetime.utcnow() - self.start_time).total_seconds())
        #self.logger.info('current_position = {0}'.format(current_position))
        return current_position

    def stop(self):
        self.start_time = None
        self.logger.info('Stop')
        self.playbackStatus = 'Stopped'
        self.stopEvent(self)

    def exit(self):
        self.logger.info('Exit')
        self.exitEvent(self)

    def set_position(self, val):
        self.logger.info('Seek to %s', val)
        self.start_time = datetime.utcnow() - timedelta(seconds=val+0.5)
        self.seekEvent(self)

    def playback_status(self):
        return self.playbackStatus

    def show_video(self):
        pass

    def duration(self):
        return (sys.maxsize)  # always greater than position()

    def quit(self):
        pass


class LoggingPlayer:
    def __init__(self, video_file, args=None):
        from omxplayer.player import OMXPlayer
        
        self.logger = logging.getLogger('OMXPlayer')
        self.player_ = OMXPlayer(video_file, args) if args != None else OMXPlayer(video_file)
        self.pauseEvent = self.player_.pauseEvent
        self.playEvent = self.player_.playEvent
        self.stopEvent = self.player_.stopEvent
        self.exitEvent = self.player_.exitEvent
        self.seekEvent = self.player_.seekEvent
        self.positionEvent = self.player_.positionEvent
        
        self.logger.info('Logging OMXPlayer class initiated')

    def hide_video(self):
        self.player_.hide_video()

    def pause(self):
        self.logger.info('Pause')
        self.player_.pause()

    def play(self):
        self.logger.info('Playing')
        self.player_.play()

    def position(self):
        current_position = self.player_.position()
        self.logger.info('current_position = {0}'.format(current_position))
        return current_position

    def stop(self):
        self.logger.info('Stop')
        self.player_.stop()

    def exit(self):
        self.logger.info('Exit')
        self.player_.exit()

    def set_position(self, val):
        self.logger.info('Seek to %s', val)
        self.player_.set_position(val)

    def playback_status(self):
        current_status = self.player.playback_status()
        self.logger.info('current_status = {0}'.format(current_status))
        return current_status

    def show_video(self):
        self.player_.show_video()

    def duration(self):
        return self.player_.duration()

    def quit(self):
        self.player_.quit()


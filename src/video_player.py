
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
        self.logger.info('current_position = {0}'.format(current_position))
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



class VideoPlayer:

    logger = getLogger()

    def __init__(self, video_file):

        try:
            from omxplayer.player import OMXPlayer
            self.player = OMXPlayer(Path(video_file), dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=['-b', '-o', 'both'])
        except Exception:
            self.player = OmxPlayerMock(video_file)

    def play_step(self, step, cancel):
        interval = rx.interval(0.1)
        interval_steps = rx.just(step).pipe(
            ops.flat_map(lambda step: interval.pipe(ops.map(lambda _: step)))
        )

        step_done = interval_steps.pipe(
            ops.filter(lambda step: self.player.position() >= step.step_end),
            ops.do_action(lambda step: self.player.set_position(step.loop_start)),
            ops.take(1)
        )

        loop_done = interval_steps.pipe(
            ops.filter(lambda step: self.player.position() >= step.loop_end),
            ops.do_action(lambda step: self.player.set_position(step.loop_start)),
            ops.take_until(cancel.pipe(ops.skip(1)))
        )

        return step_done.pipe(ops.merge(
            loop_done
        ))

    def play_stream(self, step_stream, flushes):
        self.player.play()
        play_steps = step_stream.pipe(
            ops.flat_map(lambda step: self.play_step(step, step_stream))
        )

        play_steps.pipe(
            ops.filter(lambda step: step.threshold == 100),
            ops.do_action(lambda _: flushes.on_next(1)),
        ).subscribe(lambda x: print('Reset!', x), lambda x: print('Error', x), lambda: print('Complete'))

        play_steps.subscribe(lambda x: print('Played step', x), lambda x: print('Error', x), lambda: print('Complete'))


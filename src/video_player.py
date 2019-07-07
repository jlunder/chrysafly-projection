from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

from logging import getLogger

class VideoPlayer:

    logger = getLogger()

    def __init__(self, video_file):
        self.video_file =. video_file
        VIDEO_PATH = Path(video_file)
        self.player = OMXPlayer(VIDEO_PATH)

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

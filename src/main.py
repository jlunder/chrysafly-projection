import logging

from rx.subject import Subject

from audio import Audio
from config import SOUND_DEVICE
from config import STEPS
from config import VIDEO_FILE
from config import WINDOW
from intensity_steps import intensity_steps
from video_player import VideoPlayer

logging.basicConfig(level=logging.INFO)

flushes = Subject()

audio = Audio(device=SOUND_DEVICE, window=WINDOW)
step_stream = audio.stream.pipe(
    intensity_steps(STEPS, flushes)
)

video_player = VideoPlayer(video_file=VIDEO_FILE)
video_player.play_stream(step_stream, flushes)

audio.start_stream()
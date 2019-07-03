from rx.subject import Subject

from audio import Audio
from config import SOUND_DEVICE
from config import STEPS
from config import VIDEO_FILE
from config import WINDOW
from intensity_steps import intensity_steps
from video_player import VideoPlayer



audio = Audio(device=SOUND_DEVICE, window=WINDOW)
video_player = VideoPlayer(video_file=VIDEO_FILE)

subject = Subject()
audio.stream.subscribe(lambda x: x.subscribe(lambda y: subject.on_next(y)))
audio.start_stream()


subject.pipe(
    intensity_steps(STEPS)
).subscribe(lambda step: video_player.play_step(step))




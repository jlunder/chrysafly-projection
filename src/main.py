from audio import Audio
from intensity_steps import intensity_steps
from config import STEPS
from rx.subject import Subject


subject = Subject()

audio = Audio()
audio.stream.subscribe(lambda x: x.subscribe(lambda y: subject.on_next(y)))
intensity_steps(subject, STEPS).subscribe(lambda x: print('would trigger video', x))

audio.start_stream()



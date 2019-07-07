from dataclasses import dataclass

import numpy as np
import sounddevice as sd

from rx import operators as ops
from rx.subject import Subject


@dataclass
class Audio:

    device: int = 1
    window: int = 1
    subject_: Subject = Subject()


    def start_stream(self):

        samplerate = sd.query_devices(self.device, 'input')['default_samplerate']

        def callback(indata, frames, time, status):
            self.subject_.on_next(int(np.linalg.norm(indata)*10))

        with sd.InputStream(device=self.device,
                            channels=1,
                            callback=callback,
                            finished_callback=lambda: self.subject_.on_completed(),
                            samplerate=samplerate):
            while True:
                sd.sleep(1000)

    @property
    def stream(self):
        return self.subject_.pipe(
           ops.window_with_time(self.window),
           ops.map(lambda x: x.pipe(ops.average(), ops.first()))
        )

from dataclasses import dataclass

import numpy as np
import sounddevice as sd
import logging
import math
import config

from rx import operators as ops
from rx.subject import Subject


@dataclass
class Audio:
    device: int = 1 # index into device list
    window: int = 0.1 # seconds
    subject_: Subject = Subject()
    buf_: np.array = np.array([], dtype=np.float32)

    def __init__(self, device, window):
        self.logger_ = logging.getLogger('audio')
        self.device = device
        self.window = window
        
        # stream outputs a moving-window RMS value for audio intensity
        self.rms_power = self.subject_

    def start_stream(self):
        # stop_running won't normally be how we quit -- typically the path
        # would be more like, we receive SIGBREAK, the exception propagates
        # through the except clause below, and that clause calls
        # subject_.on_error -- this mechanism is more here for completeness.
        # It might come into play if the USB audio device gets unplugged?
        run = True
        def stop_running(*args):
            run = False
        self.subject_.subscribe(on_error=stop_running, on_completed=stop_running)
        
        samplerate = sd.query_devices(self.device, 'input')['default_samplerate']
        window_samples = round(samplerate * self.window)
        
        self.logger_.info('rate={0}, window={1}'.format(samplerate, window_samples))

        def callback(indata, frames, time, status):
            try:
                # indata is returned column-major, transpose before concat'ing
                self.buf_ = np.concatenate((self.buf_, indata.transpose()[0]))
                while len(self.buf_) >= window_samples:
                    # (P = (V ** 2) * R) so P ** 2 is proportional to V ** 4 
                    power = math.sqrt(sum(self.buf_[:window_samples] ** 4) / window_samples)
                    self.buf_ = self.buf_[window_samples:]
                    #self.logger_.info('Audio RMS power={0}'.format(power))
                    self.subject_.on_next(power)
            except Exception as e:
                self.subject_.on_error(e)

        try:
            with sd.InputStream(device=self.device,
                                channels=1,
                                callback=callback,
                                samplerate=samplerate):
                while run:
                    sd.sleep(100)
            self.subject_.on_completed()
        except Exception as e:
            self.subject_.on_error(e)



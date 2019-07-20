import logging, math

from pathlib import Path
from datetime import datetime

from rx import operators as ops
from rx.subject import Subject

from audio import Audio
from video_player import LoggingPlayer, OmxPlayerMock

import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main')

flushes = Subject()

audio = Audio(device=config.SOUND_DEVICE, window=config.RMS_WINDOW)


# sense_accumulate takes a stream of RMS values from audio and normalizes them
# to produce an index into the steps list corresponding to the audio
# intensity.

# The function is somewhat complicated: first it takes the max RMS power over
# a sliding window (this is so that short, loud barks will be counted as loud
# as a long yell); the window size is determined by SENSE_WINDOW. If the
# window is too short, the participant will have to sustain more to activate
# the system; if it's too long, random sounds will tend to trigger
# transitions. (A similar principle applies to RMS_WINDOW -- the current 50ms
# time for that seems to filter out lone claps and similar impulses, which is
# desirable because you don't want the system to transition just because
# someone knocked the mic over or dropped their water bottle, but still
# activates on even fairly short barks).

# Next, the windowed RMS power is converted to log scale using RMS_MIN and
# RMS_MAX. This is our normalized "instantaneous" sense value.

# Finally, the value actually returned is filtered by slewing at a constant
# rate (set by SENSE_SLEW_POS and SENSE_SLEW_NEG) towards the instantaneous
# sense value. Additionally, we keep track of the max sense value (high water)
# achieved, and don't let them slide back more than SENSE_SLEW_BACKSLIDE. This
# forces the participant to sustain the noise for a little while to actually
# achieve the full effect -- hopefully without punishing them too much for
# stopping to take a longer breath.

rms_min_norm = config.RMS_MIN / config.RMS_MAX
log_rms_range = -math.log(rms_min_norm)
sense_slew_pos_per_rms_val = config.SENSE_SLEW_POS * config.RMS_WINDOW
sense_slew_neg_per_rms_val = config.SENSE_SLEW_NEG * config.RMS_WINDOW

class SenseAccumulator:
    def __init__(self):
        self.logger = logging.getLogger('sense')
        self.reset()

    def reset(self):
        self.rms_vals = [0] * round(config.SENSE_WINDOW / config.RMS_WINDOW)
        self.sense_val = 0.0
        self.sense_high_water = 0.0
        self.last_active_time = datetime.utcnow()

    def sense_accumulate(self, rms):
        global rms_vals, sense_val, sense_high_water
        self.rms_vals = self.rms_vals[1:]
        self.rms_vals.append(rms)
        sense_window_max = max(self.rms_vals)
        rms_norm = max(sense_window_max, config.RMS_MIN) / config.RMS_MAX
        log_rms_norm = math.log(rms_norm)
        sense_instant = (min(log_rms_norm, 0.0) + log_rms_range) / log_rms_range

        if sense_instant > config.SENSE_INACTIVE_THRESHOLD:
            self.last_active_time = datetime.utcnow()
        elif (datetime.utcnow() - self.last_active_time).total_seconds() > config.SENSE_INACTIVE_TIMEOUT:
            self.logger.info('timeout - reset')
            self.reset()

        if self.sense_val + sense_slew_pos_per_rms_val < sense_instant:
            self.sense_val += sense_slew_pos_per_rms_val
        elif self.sense_val - sense_slew_neg_per_rms_val > sense_instant:
            self.sense_val -= sense_slew_neg_per_rms_val
        else:
            self.sense_val = sense_instant
        self.sense_val = max(self.sense_val, self.sense_high_water - config.SENSE_SLEW_BACKSLIDE)
        self.sense_high_water = max(self.sense_val, self.sense_high_water)
        #self.logger.info('inst: {0} sense: {1}'.format(sense_instant, self.sense_val))
        return self.sense_high_water


quitting = False

class VideoPlayer:
    def __init__(self, video_file, stream, reset):
        self.video_file = video_file
        self.stream = stream
        self.stream.subscribe(self.play_step)
        self.reset = reset
        self.start_player()

    def on_player_exit(self, player, status):
        return
        #global quitting
        #if quitting:
        #    return
        #if self.reset:
        #    self.reset()

    def start_player(self):
        self.player = LoggingPlayer(Path(self.video_file), args=['-b', '--no-osd'])
        ##self.player = OmxPlayerMock(self.video_file)
        #self.player.exitEvent += self.on_player_exit

    def play_step(self, step):
        #logger.info('step: {0}'.format(step))
        if self.player.position() >= step[1]:
            self.player.set_position(step[0])


try:
    acc = SenseAccumulator()
    video_player = VideoPlayer(
        config.VIDEO_FILE,
        audio.rms_power.pipe(
            ops.map(acc.sense_accumulate),
            ops.map(lambda x: min(math.floor(x * len(config.STEPS)), len(config.STEPS) - 1)),
            ops.map(lambda x: config.STEPS[x])
            ),
        acc.reset)

    audio.rms_power.subscribe(lambda x: x)
    audio.start_stream()
finally:
    quitting = True
    video_player.player.quit()


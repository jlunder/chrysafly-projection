STEPS = [(0.5, 1.8),
         (11.0, 14.0),
         (17.0, 20.0),
         (23.0, 24.0),
         (30.0, 33.5),
         (40.0, 48.0),
         ]

SOUND_DEVICE = 1 # index into device list
RMS_WINDOW = 0.05 # seconds 
RMS_MIN = 0.001 # Basic volume scaling - what is a whisper?
RMS_MAX = 0.100 # Basic volume scaling - what is the loudest shout?

SENSE_WINDOW = 0.5 # seconds
SENSE_SLEW_POS = 1.0 # units per second
SENSE_SLEW_NEG = 1.0 # units per second
SENSE_SLEW_BACKSLIDE = 1.0 # units - fall back at most this far from our high water mark
SENSE_INACTIVE_THRESHOLD = 0.1 # normalized sense value
SENSE_INACTIVE_TIMEOUT = 30 # seconds

VIDEO_FILE = '/home/pi/chrysalis/media/Chrysafly.mp4'

STEPS = [(0.0, 2.0),
         (10.0, 14.0),
         (17.0, 20.0),
         (22.0, 24.0),
         (30.0, 34.0),
         (42.0, 48.0),
         ]

SOUND_DEVICE = 1 # index into device list
RMS_WINDOW = 0.05 # seconds 
RMS_MIN = 1.0e-4
RMS_MAX = 0.5e-0

SENSE_WINDOW = 0.5 # seconds
SENSE_SLEW_POS = 0.1 # units per second
SENSE_SLEW_NEG = 0.1 # units per second
SENSE_SLEW_BACKSLIDE = 0.3 # units - fall back at most this far from our high water mark
SENSE_INACTIVE_THRESHOLD = 0.1 # normalized sense value
SENSE_INACTIVE_TIMEOUT = 120 # seconds

VIDEO_FILE = '/home/pi/chrysalis/media/Chrysafly.mp4'


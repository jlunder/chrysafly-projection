from step import Step

STEPS = [Step(step_start=0, step_end=10, loop_start=10, loop_end=12, threshold=0),
         Step(step_start=12, step_end=15, loop_start=15, loop_end=20, threshold=10),
         Step(step_start=20, step_end=10, loop_start=10, loop_end=12, threshold=40),
         Step(step_start=22, step_end=10, loop_start=10, loop_end=12, threshold=75),
         Step(step_start=30, step_end=10, loop_start=10, loop_end=12, threshold=100)
        ]

SOUND_DEVICE = 1
WINDOW = 1

VIDEO_FILE = '../Exports/Metamorphosis.mp4'
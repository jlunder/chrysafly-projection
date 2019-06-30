from step import Step

STEPS = [Step(step='1.mov', transition='1t.mov', threshold=0),
         Step(step='2.mov', transition='2t.mov', threshold=10),
         Step(step='3.mov', transition='3t.mov', threshold=40),
         Step(step='4.mov', transition='4t.mov', threshold=75),
         Step(transition='finish.mov', threshold=100)
        ]

SOUND_DEVICE = 0
WINDOW = 1

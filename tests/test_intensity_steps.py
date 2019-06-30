import unittest

from rx.testing import TestScheduler, ReactiveTest

from step import Step
from intensity_steps import intensity_steps

on_next = ReactiveTest.on_next
on_completed = ReactiveTest.on_completed


class TestIntensitySteps(unittest.TestCase):
    steps = [Step(step='1.mov', transition='1t.mov', threshold=0),
             Step(step='2.mov', transition='2t.mov', threshold=10),
             Step(step='3.mov', transition='3t.mov', threshold=40),
             Step(step='4.mov', transition='4t.mov', threshold=75),
             Step(transition='finish.mov', threshold=100)
            ]

    def test_first_step(self):
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable(on_next(150, 5),
                                             on_next(210, 5),
                                             on_completed(390)
                                             )

        def create():
            return intensity_steps(xs, self.steps)

        results = scheduler.start(create)
        assert results.messages == [on_next(210, self.steps[0]),
                                    on_completed(390)
                                   ]

    def test_two_steps(self):
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable(on_next(150, 10),
                                             on_next(210, 20),
                                             on_completed(390)
                                            )

        def create():
            return intensity_steps(xs, self.steps)

        results = scheduler.start(create)
        assert results.messages == [on_next(210, self.steps[0]),
                                    on_next(210, self.steps[1]),
                                    on_completed(390)
                                   ]

    def test_low_then_higher(self):
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable(on_next(150, 5),
                                             on_next(210, 5),
                                             on_next(250, 45),
                                             on_next(270, 45),
                                             on_completed(390)
                                             )

        def create():
            return intensity_steps(xs, self.steps)

        results = scheduler.start(create)
        assert results.messages == [on_next(210, self.steps[0]),
                                    on_next(250, self.steps[1]),
                                    on_next(250, self.steps[2]),
                                    on_completed(390)
                                   ]


    def test_repeating_same_step(self):
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable(on_next(150, 5),
                                             on_next(210, 5),
                                             on_next(250, 45),
                                             on_next(270, 45),
                                             on_completed(390)
                                             )

        def create():
            return intensity_steps(xs, self.steps)

        results = scheduler.start(create)
        assert results.messages == [on_next(210, self.steps[0]),
                                    on_next(250, self.steps[1]),
                                    on_next(250, self.steps[2]),
                                    on_completed(390)
                                   ]

    def test_all(self):
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable(on_next(150, 5),
                                             on_next(210, 5),
                                             on_next(250, 45),
                                             on_next(270, 45),
                                             on_next(300, 101),
                                             on_completed(390)
                                             )

        def create():
            return intensity_steps(xs, self.steps)

        results = scheduler.start(create)
        assert results.messages == [on_next(210, self.steps[0]),
                                    on_next(250, self.steps[1]),
                                    on_next(250, self.steps[2]),
                                    on_next(300, self.steps[3]),
                                    on_next(300, self.steps[4]),
                                    on_completed(390)
                                   ]

    def test_reset(self):
        scheduler = TestScheduler()
        xs = scheduler.create_hot_observable(on_next(150, 5),
                                             on_next(210, 5),
                                             on_next(250, 45),
                                             on_next(270, 45),
                                             on_next(300, 101),
                                             on_next(310, 101),
                                             on_next(320, 5),
                                             on_completed(390)
                                             )

        def create():
            return intensity_steps(xs, self.steps)

        results = scheduler.start(create)
        assert results.messages == [on_next(210, self.steps[0]),
                                    on_next(250, self.steps[1]),
                                    on_next(250, self.steps[2]),
                                    on_next(300, self.steps[3]),
                                    on_next(300, self.steps[4]),
                                    on_next(310, self.steps[0]),
                                    on_next(310, self.steps[1]),
                                    on_next(310, self.steps[2]),
                                    on_next(310, self.steps[3]),
                                    on_next(310, self.steps[4]),
                                    on_next(320, self.steps[0]),
                                    on_completed(390)
                                   ]

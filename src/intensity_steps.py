from typing import List

import rx
from rx import operators as ops

from step import Step


def intensity_steps(source, steps: List[Step]):
    """

    Given an intensity value, return the list of steps
    which should be played back. The logic indexes higher
    based on the intensity value until it is reset by the final step

    :param source:
    :param steps:
    """

    composed = source.pipe(
        ops.flat_map(lambda event: rx.from_iterable(steps).pipe(ops.map(lambda step: (step, event)))),
        ops.filter(lambda x: x[0] <= x[1]),
        ops.map(lambda x: x[0]),
    )

    reset = composed.pipe(
        ops.filter(lambda x: not x.step),
        ops.merge(rx.from_iterable([1])),
        ops.skip(1)
    )

    return composed.pipe(
        ops.distinct(flushes=reset)
    )


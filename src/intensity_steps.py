from typing import List

import rx
from rx import operators as ops
from rx.core import Observable, pipe

from step import Step


def intensity_steps(steps: List[Step], flushes):
    """

    Given an intensity value, return the list of steps
    which should be played back. The logic indexes higher
    based on the intensity value until it is reset by the final step

    :param steps:
    """

    return pipe(
        ops.flat_map(lambda event: rx.from_iterable(steps).pipe(ops.map(lambda step: (step, event)))),
        ops.filter(lambda x: x[0] <= x[1]),
        ops.map(lambda x: x[0]),
        ops.distinct(flushes=flushes)
    )


from dataclasses import dataclass
from functools import total_ordering
from numbers import Number

@dataclass
@total_ordering
class Step:

    step: str = 0
    transition: str = 0
    threshold: int = 0

    def _is_valid_operand(self, other):
        return hasattr(other, 'threshold') or isinstance(other, Number)

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        if isinstance(other, Number):
            return self.threshold == other

        return self.threshold == other.threshold

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        if isinstance(other, Number):
            return self.threshold < other

        return self.threshold < other.threshold

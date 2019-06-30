import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path = [os.path.join(here, "../src")] + sys.path

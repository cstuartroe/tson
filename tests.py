import json
import unittest

import tson


class JSONBackwardsCompatibilityTests(unittest.TestCase):
    pass


if __name__ == "__main__":
    with open("tests/little.tson", "r") as fh:
        print(tson.load(fh))

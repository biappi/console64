import sys
import unittest


class ConsoleTopLevelTests(unittest.TestCase):
    pass


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

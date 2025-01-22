import os
import unittest
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from test.lang_tests import TestLang
from test.io_tests import TestIO  # Ensure this path is correct
from test.db_tests import TestDatabase  # Ensure this path is correct

class TestRunAllTests(unittest.TestCase):

    def test_run_all_tests(self):
        result = TestDatabase.run_all_tests()
        self.assertTrue(result.wasSuccessful(), f"Some tests failed. Failures: {result.failures}")
        # Check the number of failures (if any)
        self.assertEqual(len(result.failures), 0, f"Test failures: {result.failures}")

        result = TestIO.run_all_tests()
        self.assertTrue(result.wasSuccessful(), f"Some tests failed. Failures: {result.failures}")
        # Check the number of failures (if any)
        self.assertEqual(len(result.failures), 0, f"Test failures: {result.failures}")

        result = TestLang.run_all_tests()
        self.assertTrue(result.wasSuccessful(), f"Some tests failed. Failures: {result.failures}")
        # Check the number of failures (if any)
        self.assertEqual(len(result.failures), 0, f"Test failures: {result.failures}")

import os
import py_compile
import unittest


class SyntaxTest(unittest.TestCase):
    def test_compile(self):
        for root, _, files in os.walk('app'):
            for f in files:
                if f.endswith('.py'):
                    py_compile.compile(os.path.join(root, f))

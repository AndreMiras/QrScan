# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import unittest

from main import CodeType


class CodeTypeTestCase(unittest.TestCase):

    def test_from_data_simple(self):
        data = "https://github.com/AndreMiras/QrScan"
        code_type = CodeType.from_data(data)
        self.assertEqual(code_type, CodeType.URL)

    def test_from_data_special_char(self):
        """
        Verifies we can decode special characters when already specified
        as unicode, refs #10.
        """
        # "Sábado" not unicode
        data = b"S\xc3\xa1bado"
        with self.assertRaises(TypeError):
            code_type = CodeType.from_data(data)
        # unicode
        data = data.decode('utf8')
        code_type = CodeType.from_data(data)
        self.assertEqual(code_type, CodeType.TEXT)

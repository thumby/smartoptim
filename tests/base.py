#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of smartoptim.
# https://github.com/thumby/smartoptim

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Thumby <dev@thumby.io>

from tempfile import NamedTemporaryFile
from unittest import TestCase as PythonTestCase


class TestCase(PythonTestCase):
    def img(self, name):
        with open(name) as img:
            return img.read()

        return None

    def debug(self, buffer):
        with NamedTemporaryFile(delete=False) as ifile:
            ifile.write(buffer)

            print "File saved at %s" % ifile.name

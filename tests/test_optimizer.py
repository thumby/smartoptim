#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of smartoptim.
# https://github.com/thumby/smartoptim

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Thumby <dev@thumby.io>

from preggy import expect

from smartoptim.optimizer import Optimizer, get_ssim
from tests.base import TestCase


class OptimizerTestCase(TestCase):
    def test_can_create_optimizer(self):
        image = "./tests/fixtures/sample.jpg"
        with open(image) as img:
            opt = Optimizer(image=img.read())

        expect(opt.image).not_to_be_null()
        expect(opt.image_array).not_to_be_null()
        expect(opt.result).to_be_null()

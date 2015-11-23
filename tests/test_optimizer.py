#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of smartoptim.
# https://github.com/thumby/smartoptim

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Thumby <dev@thumby.io>

import cStringIO
from mock import Mock
import numpy as np
from preggy import expect

from PIL import Image
from smartoptim.optimizer import Optimizer, get_ssim
from thumbor.optimizers.jpegtran import Optimizer as JpegTranOptimizer
from tests.base import TestCase


class OptimizerTestCase(TestCase):
    def test_can_create_optimizer(self):
        optimizers = [1, 2, 3]

        img = self.img("./tests/fixtures/sample.jpg")
        opt = Optimizer(image=img, optimizers=optimizers)

        expect(opt.image).not_to_be_null()
        expect(opt.image_array).not_to_be_null()
        expect(opt.result).to_be_null()
        expect(opt.optimizers).to_equal(optimizers)

    def test_can_run_optimizer(self):
        context = Mock(
            config=Mock(
                JPEGTRAN_PATH='/usr/local/opt/mozjpeg/bin/jpegtran',
            )
        )
        img = self.img("./tests/fixtures/sample_small.jpg")
        optimizers = [
            JpegTranOptimizer,
        ]
        opt = Optimizer(image=img, optimizers=optimizers, context=context, pop=100, generations=20)

        result = opt.optimize()

        expect(result).not_to_be_null()

        im = Image.open(cStringIO.StringIO(result))
        im2 = Image.open(cStringIO.StringIO(img))

        ssim = get_ssim(np.array(im), np.array(im2))
        print "Source image has %.2fkb." % (len(img) / 1024.0)
        print "Best individual has %.2fkb and %.2f SSIM with source image" % (
            len(result) / 1024.0,
            ssim,
        )
        expect(ssim).to_be_greater_than(0.8)

        self.debug(result)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of smartoptim.
# https://github.com/thumby/smartoptim

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Thumby <dev@thumby.io>

import cStringIO

import numpy as np
from PIL import Image
from skimage.measure import structural_similarity


def get_ssim(actual, expected):
    im = Image.fromarray(actual)
    im2 = Image.fromarray(expected)

    if im.size[0] != im2.size[0] or im.size[1] != im2.size[1]:
        raise RuntimeError(
            "Can't calculate SSIM for images of different sizes (one is %dx%d, the other %dx%d)." % (
                im.size[0], im.size[1],
                im2.size[0], im2.size[1],
            )
        )
    return structural_similarity(actual, expected, multichannel=True)


class Individual:
    def __init__(self, source_image):
        self.source_image = source_image
        self.result = None

    @property
    def fitness(self):
        return get_ssim(self.result, self.source_image)


class Optimizer:
    def __init__(self, image):
        self.image = image
        im = Image.open(cStringIO.StringIO(image))
        im = im.convert('RGBA')
        self.image_array = np.array(im)
        self.result = None

    def calculate_fitness(self, individual):
        return individual.fitness

    def optimize(self):
        pass

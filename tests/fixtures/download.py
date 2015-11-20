#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of smartoptim.
# https://github.com/thumby/smartoptim

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Thumby <dev@thumby.io>


import os
from os.path import exists
from cStringIO import StringIO

from octopus import TornadoOctopus
from PIL import Image

NUM_IMAGES = 1000

SIZES = [
    ('large', 1024, 768),
    ('medium', 600, 350),
    ('small', 200, 140),
]


def download():
    otto = TornadoOctopus(
        concurrency=100, auto_start=True,
    )

    def enqueue(size, index, width, height):
        url = 'http://lorempixel.com/%d/%d/' % (width, height)
        print "Enqueuing %s image %d..." % (size, i + 1)
        otto.enqueue(url, handle_url_response(size, i + 1, width, height))

    def handle_url_response(size, index, width, height):
        def handle(url, response):
            if response.status_code != 200:
                print "%s image %d (%d) failed." % (size, index, response.status_code)
                enqueue(size, index, width, height)
                return

            print "%s image %d (%d) saved." % (size, index, response.status_code)

            path = './tests/fixtures/imageset/%s' % size
            if not exists(path):
                os.makedirs(path)
            jpg = StringIO(response.text)
            img = Image.open(jpg)
            img.save('%s/image_%d.jpg' % (path, index))

        return handle

    for i in range(NUM_IMAGES):
        for size, width, height in SIZES:
            enqueue(size, i + 1, width, height)

    otto.wait()  # waits until queue is empty or timeout is ellapsed


if __name__ == "__main__":
    download()

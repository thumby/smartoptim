#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of smartoptim.
# https://github.com/thumby/smartoptim

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Thumby <dev@thumby.io>

import cStringIO
import random
from io import BytesIO

import numpy as np
from PIL import Image
from skimage.measure import structural_similarity
from deap import tools, base


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


class Fitness:
    def __init__(self, value, valid):
        self.value = value
        self.valid = valid

    def __neg__(self):
        return self.value * -1


class Individual:
    def __init__(self, source_image, source_image_array, optimizer, min_fit, context, quality=None):
        self.optimizer = optimizer
        self.source_image = source_image
        self.source_image_array = source_image_array
        self.min_fit = min_fit
        self.context = context

        self.result = None
        self.result_array = None
        self.__fit = None
        self.__size = None

        self.quality = quality
        if self.quality is None:
            self.quality = random.randint(40, 90)

    def apply(self):
        if self.result is not None:
            return

        opt = self.optimizer(self.context)
        result = opt.run_optimizer('.jpg', self.source_image)
        im = Image.open(cStringIO.StringIO(result))
        im = im.convert('RGBA')
        img_buffer = BytesIO()
        im.save(img_buffer, 'JPEG', quality=self.quality)
        self.result = img_buffer.getvalue()
        self.result_array = np.array(im)

    def clear(self):
        self.result = None
        self.result_array = None
        self.__fit = None
        self.__size = None

    @property
    def fitness(self):
        if self.__fit is None:
            self.__fit = get_ssim(self.result_array, self.source_image_array)
            self.__size = len(self.result)

        #avg = (1.0 / self.__size) * self.__fit
        avg = (1.0 / self.__size)

        return Fitness(value=avg, valid=self.__fit < self.min_fit)

    @classmethod
    def mate(self, individual1, individual2):
        optimizer = random.choice([individual1.optimizer, individual2.optimizer])
        quality = random.choice([individual1.quality, individual2.quality])

        ind = Individual(
            source_image=individual1.source_image,
            source_image_array=individual1.source_image_array,
            optimizer=optimizer,
            min_fit=individual1.min_fit,
            context=individual1.context,
            quality=quality,
        )

        ind.apply()

        return ind

    @classmethod
    def mutate(self, individual, optimizers):
        individual.optimizer = random.choice(optimizers)
        individual.quality = random.randint(70, 100)
        individual.clear()
        individual.apply()


class Optimizer:
    def __init__(self, image, optimizers, context=None, min_fit=0.8, pop=2, generations=2):
        self.pop = pop
        self.generations = generations
        self.optimizers = optimizers
        self.min_fit = min_fit
        self.context = context

        self.image = image
        im = Image.open(cStringIO.StringIO(image))
        im = im.convert('RGBA')
        self.image_array = np.array(im)

        self.result = None

        self.toolbox = base.Toolbox()
        self.toolbox.register(
            "individual", self.create_random_individual
        )
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.calculate_fitness)
        self.toolbox.register("mate", Individual.mate)
        self.toolbox.register("mutate", Individual.mutate)
        self.toolbox.register("select", self.select)

    def select(self, selection, count):
        return sorted(selection, key=lambda item: -item.fitness)[:count]

    def create_random_individual(self):
        return Individual(
            source_image=self.image,
            source_image_array=self.image_array,
            optimizer=random.choice(self.optimizers),
            min_fit=self.min_fit,
            context=self.context,
        )

    def calculate_fitness(self, individual):
        individual.apply()
        return individual.fitness

    def optimize(self):
        pop = self.toolbox.population(n=self.pop)
        CXPB = 0.5

        for individual in pop:
            individual.apply()

        print("  Evaluated %i individuals" % len(pop))

        # Begin the evolution
        for g in range(self.generations):
            print("-- Generation %i --" % g)

            # Select the next generation individuals
            offspring = self.toolbox.select(pop, len(pop))

            # Clone the selected individuals
            offspring = list(map(self.toolbox.clone, offspring))

            kill = 0
            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):

                # cross two individuals with probability CXPB
                if random.random() < CXPB:
                    child = self.toolbox.mate(child1, child2)
                    if child.fitness.valid:
                        offspring.append(child)
                        kill += 1

            #for mutant in offspring:
                ## mutate an individual with probability MUTPB
                #if random.random() < MUTPB:
                    #self.toolbox.mutate(mutant, self.optimizers)

            # The population is entirely replaced by the offspring
            pop[:] = offspring[:len(offspring) - kill]

            # Gather all the fitnesses in one list and print the stats
            fits = [ind.fitness.value for ind in pop]

            length = len(pop)
            mean = sum(fits) / length
            sum2 = sum(x*x for x in fits)
            std = abs(sum2 / length - mean**2)**0.5

            print("  Min %s" % min(fits))
            print("  Max %s" % max(fits))
            print("  Avg %s" % mean)
            print("  Std %s" % std)

        print("-- End of (successful) evolution --")

        # best_ind = tools.selBest(pop, 1)[0]
        best_ind = sorted(pop, key=lambda item: -item.fitness)[:1][0]
        #print("Best individual is %s, %s" % (best_ind.result, best_ind.fitness.value))

        return best_ind.result

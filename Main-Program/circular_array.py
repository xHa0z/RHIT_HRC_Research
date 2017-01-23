import numpy as np
import math
class CircularArray:


    def __init__(self, size):

        self.array = [np.NaN] * size
        self.index = 0
        self.counter = 1

    def add_value(self, value):


        self.array[self.index] = value

        self.index = (self.index + 1) % (len(self.array))
        self.counter += 1
    def averager_function(self):
        count = 0
        sum = 0

        for k in range(0, len(self.array)):

            if np.isnan(self.array[k]) == False:

                sum += self.array[k]
                count += 1
        if count == 0:
            return 0
        else:
            sum_avg = sum / (count)


            return sum_avg


    def standard_deviation(self, size):

        std = .001
        if self.counter < size + 1:


            for k in range(0, len(self.array)):
                print
                print self.counter
                print
                std += ((self.array[k] - self.averager_function()) ** 2)
                return (math.sqrt(std) / self.counter)


        elif self.counter >= size + 1:
            ff = .001
            for k in range(0, len(self.array)):
                print
                print self.counter
                print
                ff += ((self.array[k] - self.averager_function()) ** 2)
                return (math.sqrt(ff) / len((self.array)))

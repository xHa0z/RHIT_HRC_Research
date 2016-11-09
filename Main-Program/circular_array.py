import numpy as np

class CircularArray:


    def __init__(self, size):

        self.array = [np.NaN] * size
        self.index = 0
    def add_value(self, value):
        self.array[self.index] = value
        self.index = (self.index + 1) % (len(self.array))
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




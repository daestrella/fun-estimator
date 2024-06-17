import numpy as np
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, figsize, title, xlabel, ylabel, x_domain, x_max, y_range=None):
        '''
        figsize: (x, y)
        title, xlabel, ylabel: string
        x_domain: (min, max)
        x_max: float
        y_range: (min, max)
        '''
        self.max = x_max
        plt.figure(figsize=figsize)
        plt.title(title)
        plt.axhline(0, color='black', linewidth=0.5)    # x-axis
        plt.axvline(0, color='black', linewidth=0.5)    # y-axis
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.xlim(*x_domain)
        if y_range:
            plt.ylim(*y_range)

    def plot(self, label, y, x=None):
        if not x:   # x is not defined
            x = np.linspace(-self.max, self.max, 1000)
        
        if callable(y): # y is a function
            with np.errstate(divide='ignore', invalid='ignore'):
                plt.plot(x, np.vectorize(y)(x),
                         label=label)
        else:
            plt.plot(x, y, label=label)

        plt.legend()
        plt.draw()

    def show_graph(self):
        plt.show()

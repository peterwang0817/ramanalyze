from scipy.optimize import curve_fit
from inspect import signature


class Series():

    def __init__(self, name, xdata, ydata, params, color):
        
        self.name = name
        self.xdata = xdata
        self.ydata = ydata
        self.params = params
        self.color = color

    def fit(self, func, guess):
        #print(signature(func))
        params, _ = curve_fit(func, self.xdata, self.ydata, p0=guess)
        for i in range(len(params)):
            if (i + 1) % 3 == 0:
                print(params[i])
        yfit = func(self.xdata, *params)
        return Series(f'fit of {self.name}', self.xdata, yfit, params, self.color)
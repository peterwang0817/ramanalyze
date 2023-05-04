from scipy.optimize import curve_fit

class Series():

    def __init__(self, name, xdata, ydata, params, color):
        
        self.name = name
        self.xdata = xdata
        self.ydata = ydata
        self.params = params
        self.color = color

    def fit(self, func, guess):

        params, _ = curve_fit(func, self.xdata, self.ydata, guess)
        yfit = func(self.xdata, *params)
        return Series(f'fit of {self.name}', self.xdata, yfit, params, self.color)
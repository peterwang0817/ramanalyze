import numpy as np

def gaussian(x, a, b, c):
    # Gaussian distribution. Accepts the parameters a, b, c
    return (a / b) * np.exp(-((x - c) / b) ** 2)

def lorentzian(x, a, b, c):
    # Lorentz distribution. Accepts the parameters a, b, c
    return (a / b) * np.reciprocal(1.0 + ((x - c) / b) ** 2)

def voigt(x, a, b, c, d):
    # Voigt distribution. Accepts the parameters a, b, c, and an additional mixing factor d.
    return d * gaussian(x, a, b, c) + (1.0 - d) * lorentzian(x, a, b, c)
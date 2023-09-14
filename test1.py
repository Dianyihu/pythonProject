import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.gaussian_process.kernels import ConstantKernel, RBF
from sklearn.gaussian_process import GaussianProcessRegressor
from scipy.interpolate import interp1d

X = np.linspace(120, 150, 7)
y = [-8, -6, -4, 5, 10, 15, -20]

f = interp1d(X,y,kind=3)

# kernel = ConstantKernel(constant_value=1000, constant_value_bounds=(-10, 10000)) * RBF(length_scale=10, length_scale_bounds=(0.0, 100))
# gpr = GaussianProcessRegressor(kernel=kernel).fit(X, y)
#
# gpr.fit(X, y)

x_new = np.arange(120, 150, 0.5)
y_new = f(x_new)

plt.plot(x_new, y_new)
plt.show()







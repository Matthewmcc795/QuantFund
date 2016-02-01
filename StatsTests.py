# from scipy import stats
# import numpy as np
# x = np.random.random(10)
# y = np.random.random(10)
# slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

from sklearn import linear_model
clf = linear_model.LinearRegression()
clf.fit ([[0, 0], [1, 1], [2, 2]], [0, 1, 2])
LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
clf.coef_
array([ 0.5,  0.5])
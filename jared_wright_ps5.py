# -*- coding: utf-8 -*-
"""jared_wright_ps5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nQpye14BrgEx-aCeRELG6OFQPU1Do3ss
"""

# Commented out IPython magic to ensure Python compatibility.
#JARED WRIGHT

# import the modules and function you will use here
import numpy as np
import sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')
import csv

# %matplotlib inline
from google.colab import drive
drive.mount('/content/gdrive')
# %cd '/content/gdrive/My Drive/Econ 484/auxiliaries'

"""This problem deals with regularized regression. The boston dataset is described right after it is loaded in just by running the code that is aleardy there."""

from sklearn.datasets import load_boston
boston = load_boston()
print(boston['DESCR'])
x = pd.DataFrame(boston['data'], columns=boston['feature_names'])
y = pd.Series(boston['target'])

"""$(a)$ Split the data into a train and a test set"""

X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=24)

"""$(b)$ Use this data to fit an OLS, LASSO, ridge, and ElasticNet model on the data. For now, use the default for the penalty coefficient. Display the coefficients and test error for each."""

from sklearn.linear_model import LinearRegression
OLS = LinearRegression().fit(X_train, y_train)
print("OLS coefficients: {:}".format(OLS.coef_))
print("OLS accuracy on test set: {:.3f}".format(OLS.score(X_test, y_test)))

from sklearn.linear_model import Lasso
lasso = Lasso().fit(X_train, y_train)
print("Lasso coefficients: {:}".format(lasso.coef_))
print("Lasso accuracy on test set: {:.3f}".format(lasso.score(X_test, y_test)))

from sklearn.linear_model import ElasticNet
elastic = ElasticNet().fit(X_train, y_train)
print("ElasticNet coefficients: {:}".format(elastic.coef_))
print("ElasticNet accuracy on test set: {:.3f}".format(elastic.score(X_test, y_test)))

"""$(c)$ Describe the differences that you see in the coefficients and error. What is the cause of this difference in coefficients?"""

#OLS did the best. It also was not penalizing coefficients so although some coefficients were
#small, it did not try to minimize coefficients. I think this is why it had better predictions
#than the other methods. Lasso and ElasticNet have some coefficients that are 0 because they penalized.

"""$(d)$ Use K-fold cross validation to find an optimal penalty parameter for Ridge and Lasso."""

from sklearn.model_selection import GridSearchCV

param_grid = {
    'alpha': [0.0001, 0.001, 0.005, 0.01, 0.1, 1],
    'fit_intercept': [0,1],
    'max_iter': [15, 20, 50, 100, 500, 1000]
}

lasso = Lasso()
grid_search_lasso = GridSearchCV(estimator=lasso, param_grid=param_grid, cv=3)
grid_search_lasso.fit(X_train, y_train)
print("Lasso best parameters: {:}".format(grid_search_lasso.best_params_))
print("Lasso score: {:}".format(grid_search_lasso.score(X_test, y_test)))


from sklearn.linear_model import Ridge
ridge = Ridge()
grid_search_ridge = GridSearchCV(estimator=ridge, param_grid=param_grid, cv=3)
grid_search_ridge.fit(X_train, y_train)
print("Ridge best parameters: {:}".format(grid_search_ridge.best_params_))
print("Ridge score: {:}".format(grid_search_ridge.score(X_test, y_test)))

"""$(e)$ Now use cross validation, to find the optimal penalty parameter. Use LOOCV and Kfold cross validation with K=5 to find optimal parameters for the ElasticNet model. How do the test errors and optimal parameters differ?"""

n = y_train.size

alpha_grid = {'alpha': [.0001, .0005,.001, .002, .003, .004, .006, .008, .01, .012, .014, .016 ,.018, .02 ],'max_iter': [100000]}
grid_search = GridSearchCV(ElasticNet(),alpha_grid,cv=n,return_train_score=True) #I LET CV = n
loo=grid_search.fit(X_train,y_train)
print("Leave-one-out ElasticNet accuracy on test set: {:.4f}".format(loo.score(X_test, y_test)))
print("Leave-one-out ElasticNet alpha: {:}".format(loo.best_params_))

alpha_grid = {'alpha': [.0001, .0005,.001, .002, .003, .004, .006, .008, .01, .012, .014, .016 ,.018, .02 ],'max_iter': [100000]}
grid_search = GridSearchCV(ElasticNet(),alpha_grid,cv=5,return_train_score=True)
five_fold=grid_search.fit(X_train,y_train)
print("5-fold ElasticNet accuracy on test set: {:.4f}".format(loo.score(X_test, y_test)))
print("5_fold CV best parameters: ",five_fold.best_params_)

#test errors are the same but with 5-fold validation the model did best with an alpha of 0.0005 as opposed to 0.0001 with leave-one-out cv.

"""$(f)$ Now that we have tuned the models to perform about as well as they can, which one performs best on the training data? Which one performs best on the test data? Which of these models allow us to do effective causal inference with the coefficients? Why?"""

print("Lasso accuracy on test set: {:}".format(grid_search_lasso.score(X_test, y_test)))
print("Ridge accuracy on test set: {:}".format(grid_search_ridge.score(X_test, y_test)))
print("Leave-one-out ElasticNet accuracy on test set: {:.4f}".format(loo.score(X_test, y_test)))
print("5-fold ElasticNet accuracy on test set: {:.4f} \n".format(loo.score(X_test, y_test)))

print("Lasso accuracy on training set: {:}".format(grid_search_lasso.score(X_train, y_train)))
print("Ridge accuracy on training set: {:}".format(grid_search_ridge.score(X_train, y_train)))
print("Leave-one-out ElasticNet accuracy on training set: {:.4f}".format(loo.score(X_train, y_train)))
print("5-fold ElasticNet accuracy on training set: {:.4f}".format(loo.score(X_train, y_train)))

#I got very similar results with most models. Lasso does slightly better on the test set, whereas it ties with ElasticNet on the training set 
#

"""For the next problem we will be using the `Carseats` data set that is available on learningsuite. Load the data and convert the text variables into dummies so that we can use them in the data. Pandas has a function called `get_dummies` that you might want to use."""

carseat = pd.read_csv('Carseats.csv')
carseat = pd.get_dummies(carseat)
print(carseat.head)

"""Now that the data has only numeric columns, we can proceed to the analysis.  
Use `Sales` as the outcome variable  
(a) Split the data set into a training set and a test set.  
(b) Fit a regression tree to the training set with the default depth. What train and test MSE do you obtain?  
(c) Use cross-validation in order to determine the optimal level of tree complexity. Does pruning the tree improve the test MSE? Plot a tree with a depth of 3, and interpret the results.  
(d) Use a bagging approach in order to analyze this data. What test MSE do you obtain? Look at the feature importances attribute of your model object to determine which variables are most important.  
(e) Use random forests to analyze this data. What test MSE do you obtain? Look at the feature importances attribute of your model object function to determine which variables are most important. Describe the effect of m, the number of variables considered at each split, on the error rate obtained.
"""

y = carseat.filter(items=['Sales'])
X = carseat.loc[:, carseat.columns != 'Sales']
print(y.head)
print(X.head)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=24)

from sklearn.tree import DecisionTreeRegressor
dtree = DecisionTreeRegressor().fit(X_train, y_train)
print("Decision Tree accuracy on training set: {:.3f}".format(dtree.score(X_train, y_train)))
print("Decision Tree accuracy on test set: {:.3f} \n".format(dtree.score(X_test, y_test)))


param_grid = {
    'max_depth': [7,10,15,20,25,35],
    'min_samples_split': [2,6,12],
    'max_features': [7,10,15,40,100,200,300,400],
    'ccp_alpha': [0.0,0.001,0.01,0.1,1,5,10]
}

dtree = DecisionTreeRegressor()
grid_search_dtree = GridSearchCV(estimator=dtree, param_grid=param_grid, cv=3)
grid_search_dtree.fit(X_train, y_train)
print("Decision Tree best parameters: {:}".format(grid_search_dtree.best_params_))
print("Decision Tree score: {:}".format(grid_search_dtree.score(X_test, y_test)))

#Pruning the tree does improve test MSE because the best parameter of ccp_alpha is non-zero


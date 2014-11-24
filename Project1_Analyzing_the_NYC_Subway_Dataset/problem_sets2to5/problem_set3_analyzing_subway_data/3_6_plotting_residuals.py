import numpy as np
import scipy
import matplotlib.pyplot as plt

def plot_residuals(turnstile_weather, predictions):
    '''
    Using the same methods that we used to plot a histogram of entries
    per hour for our data, why don't you make a histogram of the residuals
    (that is, the difference between the original hourly entry data and the predicted values).

    Based on this residual histogram, do you have any insight into how our model
    performed?  Reading a bit on this webpage might be useful:

    http://www.itl.nist.gov/div898/handbook/pri/section2/pri24.htm
    '''
    plt.figure() #creat a figure
    (turnstile_weather["ENTRIESn_hourly"] - predictions).hist(bins = 20) #plot histogram
    plt.xlabel("Difference between ENTRIESn_hourly and predictions") #set xlabel
    plt.ylabel("Frequancy") #set ylabel
    plt.title("Histogram of the residuals") #set title
    return plt
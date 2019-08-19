# -*- coding: utf-8 -*-
"""
Perform statistical tests on paired (column) data.
One of the key use-cases is comparing some performance metric for a task before and after applying your own changes.
If the 'perform_homogeneity_tests()' function returns True, it means that the change has had no effect on the metric

@author: Ishaan Bhat
@email: ishaan@isi.uu.nl

"""
import numpy as np
from scipy.stats import normaltest
from scipy.stats import bartlett
from scipy.stats import levene
from scipy.stats import ttest_ind
from scipy.stats import mannwhitneyu
from sklearn.utils import resample
import seaborn as sns
import matplotlib.pyplot as plt


class CheckHomogeneity:
    """
    Check whether values contained in the 2 arrays come from the same distribution

    :param arr1 : (numpy ndarray) Array of metrics computed
    :param arr2 : (numpy ndarray) Array of metrics computed
    :param alpha : Significance level used to test (Default : 0.05)
    :param verbose: (bool) Flag to indicate whether info about tests performed be printed

    """
    def __init__(self, arr1, arr2, alpha=0.05, verbose=False):

        try:
            assert(isinstance(arr1, np.ndarray) and isinstance(arr2, np.ndarray))
        except AssertionError:
            print("PyStatCheck works with numpy ndarrays."
                  "Please convert your iterable object to a numpy array")

        try:
            assert((arr1.ndim == 1) and (arr2.ndim == 1))
        except AssertionError:
            print("PyStatCheck works with 1D sample arrays."
                  "The given arrays are of the dimensions {} and {} respectively".format(arr1.ndim, arr2.ndim))

        self.arr1 = arr1
        self.arr2 = arr2
        self.verbose = verbose
        self.alpha = alpha

    def perform_homogeneity_tests(self):

        try:
            assert (self.arr1.shape == self.arr2.shape)
        except AssertionError:
            print('The 2 arrays must be of the same shape')

        if self._check_normality(self.arr1) is True and self._check_normality(self.arr2) is True:
            # Tests for data with normal distributions
            _, p = bartlett(self.arr1, self.arr2)
            if p > self.alpha:
                # T-test with equal variances
                _, p = ttest_ind(self.arr1, self.arr2, equal_var=True)
                if p > self.alpha:
                    if self.verbose is True:
                        print('Distributions have the same mean according to t-test (equal variance).'
                              'p-value : {}'.format(p))
                    return True
                else:
                    if self.verbose is True:
                        print('Distributions do not have the same mean according to t-test (equal variance).'
                              'p-value : {}'.format(p))
                    return False

            else:
                # T-test for unequal variances
                _, p = ttest_ind(self.arr1, self.arr2, equal_var=False)
                if p > self.alpha:
                    if self.verbose is True:
                        print('Distributions have the same mean according to t-test (unequal variance).'
                              'p-value : {}'.format(p))
                    return True
                else:
                    if self.verbose is True:
                        print('Distributions do not have the same mean according to t-test (unequal variance).'
                              'p-value : {}'.format(p))
                    return False
        else:
            # Tests for data with non-normal distribution
            _, p = levene(self.arr1, self.arr2)
            if p > self.alpha:
                if self.verbose is True:
                    print('Data distributions have equal variances according to Levene test.'
                          'p-value : {}'.format(p))
            else:
                if self.verbose is True:
                    print('Data distributions have unequal variances according to Levene test.'
                          'p-value : {}'.format(p))

            _, p = mannwhitneyu(self.arr1, self.arr2)
            if p > self.alpha:
                if self.verbose is True:
                    print('Distributions have the same median according to the Mann-Whitney U test.'
                          'p-value : {}'.format(p))
                return True
            else:
                if self.verbose is True:
                    print('Distributions do not have the same median according to Mann-Whitney U test.'
                          'p-value : {}'.format(p))
                return False

    def visualize_distributions(self, fname='data_viz.png', b_steps=1000, names=None, title=None):
        """
        Visualize distribution plots by by plotting a histogram of bootstrap sample means

        :param fname: (str) Filename used to save the image
        :param b_steps: (int) Number of sampling steps to create one bootstrap sample
        :param names: (str) List of strings to be used as legend
        :param title: (str) Title of the figure
        :return:
        """
        sample_means_arr1 = self._bootstrap(self.arr1, b_steps=b_steps)
        sample_means_arr2 = self._bootstrap(self.arr2, b_steps=b_steps)
        if names is None:
            labels = ['Distribution 1', 'Distribution 2']
        else:
            labels = names

        sns.distplot(sample_means_arr1, label=labels[0])
        sns.distplot(sample_means_arr2, label=labels[1])

        plt.legend()
        if title is not None:
            plt.title(title)
        plt.savefig(fname)
        plt.close()

    @staticmethod
    def _bootstrap(col, b_steps=1000):
        """
        Estimate population distribution by bootstrapping the sample distribution

        :param col:
        :param b_steps:
        :return: sample_means: (numpy ndarray) Array containing means of bootstrapped samples
        """
        sample_means = []
        for step in range(b_steps):
            sample_means.append(np.mean(resample(col)))
        return np.asarray(sample_means, dtype=np.float32)

    def _check_normality(self, col):
        """
        Check for normality
        """
        _, p = normaltest(col)
        if p > self.alpha:
            return True

        return False

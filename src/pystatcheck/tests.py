# -*- coding: utf-8 -*-
"""
Perform statistical tests on paired (column) data.
One of the key use-cases is comparing some performance metric for a task before and after applying your own changes.
If the 'perform_homogeneity_tests()' function returns True, it means that the change has had no effect on the metric

Author: Ishaan Bhat (ibhat@umcutrecht.nl)

"""
from scipy.stats import shapiro
from scipy.stats import bartlett
from scipy.stats import levene
from scipy.stats import ttest_ind
from scipy.stats import mannwhitneyu


class CheckHomogeneity:
    """
    Check whether values contained in the 2 arrays come from the same distribution

    :param arr1 : (numpy ndarray) Array of metrics computed
    :param arr2 : (numpy ndarray) Array of metrics computed
    :param alpha : Significance level used to test (Default : 0.05)
    :param verbose: (bool) Flag to indicate whether info about tests performed be printed

    """
    def __init__(self, arr1, arr2, alpha=0.05, verbose=False):
        self.arr1 = arr1
        self.arr2 = arr2
        self.verbose = verbose
        self.alpha = alpha

    def perform_homogeneity_tests(self):

        try:
            assert (self.arr1.shape == self.arr2.shape)
        except AssertionError:
            print('The 2 arrays must be of the same shape')

        if self.check_normality(self.arr1) is True and self.check_normality(self.arr2) is True:
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

    @staticmethod
    def check_normality(col):
        """
        Check for normality
        """
        _, p = shapiro(col)
        if p > 0.05:
            return True

        return False

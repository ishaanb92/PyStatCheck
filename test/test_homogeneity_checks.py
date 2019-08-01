# -*- coding: utf-8 -*-
from unittest import TestCase
from pystatcheck.tests import CheckHomogeneity
import numpy as np

__author__ = "Ishaan Bhat"
__copyright__ = "Ishaan Bhat"
__license__ = "mit"


class TestHomogeneityChecks(TestCase):
    """
    Test suite to check if the module can detect homogeneity in known cases

    """
    def test_same_distribution(self):
        arr1 = np.random.normal(loc=0, scale=3.0, size=(1000,))
        arr2 = np.random.normal(loc=0, scale=3.0, size=(1000,))
        assert(CheckHomogeneity(arr1=arr1, arr2=arr2, verbose=False).perform_homogeneity_tests() is True)

    def test_different_distribution_equal_variance(self):
        arr1 = np.random.normal(loc=0, scale=3.0, size=(1000,))
        arr2 = np.random.normal(loc=1.0, scale=3.0, size=(1000,))
        assert(CheckHomogeneity(arr1=arr1, arr2=arr2, verbose=False).perform_homogeneity_tests() is False)

    def test_different_distribution_unequal_variance(self):
        arr1 = np.random.normal(loc=0, scale=3.0, size=(1000,))
        arr2 = np.random.normal(loc=1.0, scale=5.0, size=(1000,))
        assert(CheckHomogeneity(arr1=arr1, arr2=arr2, verbose=False).perform_homogeneity_tests() is False)

    def test_same_distribution_non_normal(self):
        arr1 = np.random.binomial(n=10, p=0.5, size=(1000,))
        arr2 = np.random.binomial(n=10, p=0.5, size=(1000,))
        assert(CheckHomogeneity(arr1=arr1, arr2=arr2, verbose=False).perform_homogeneity_tests() is True)

    def test_different_distribution_non_normal(self):
        arr1 = np.random.binomial(n=10, p=0.5, size=(1000,))
        arr2 = np.random.binomial(n=10, p=0.8, size=(1000,))
        assert(CheckHomogeneity(arr1=arr1, arr2=arr2, verbose=False).perform_homogeneity_tests() is False)










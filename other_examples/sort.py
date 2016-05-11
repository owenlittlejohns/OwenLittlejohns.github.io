#!/usr/bin/env python3

"""
Test various sorting algorithms to compare efficiencies
Owen Littlejohns - 2016 May 11th
"""

import numpy as np # For random arrays, and array maths
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib import font_manager

def bubble_sort(input_arr, n_comp):
    """
    Perform the bubble sort:
    Optimizations: 
       - don't compare elements fixed at the end
       - if No comparisons done in an interation, then break out
    Return sorted array and number of comparisons
    """

    iter_swap = 1
    iter_no   = 1
    n_comp    = 0

    while iter_swap > 0:
        iter_swap = 0
        for el_ind in range(len(input_arr) - 1 - (iter_no - 1)):
            if(input_arr[el_ind] > input_arr[el_ind + 1]):
                input_arr[el_ind], input_arr[el_ind + 1] = \
                    input_arr[el_ind + 1], input_arr[el_ind]
                iter_swap += 1

            n_comp += 1

        iter_no += 1

    return n_comp, input_arr


def quick_sort(input_arr, n_comp):
    """
    Sort array using quick sort (pivot index comparison)
    Base case is array length of one (it WILL be sorted)
    Return sorted array and number of comparisons
    """

    if len(input_arr) > 1:
        pivot_index   = len(input_arr) // 2 # Choose middle point as a pivot
        small = [] # Create empty array for items smaller than pivot
        big   = [] # Create empty array for items larger than pivot

        for el_ind, el_val in enumerate(input_arr):
            if el_ind != pivot_index:
                if len(input_arr) > 1: n_comp += 1
                if el_val < input_arr[pivot_index]:
                    small.append(el_val)
                else:
                    big.append(el_val)

        n1, small_sort = quick_sort(small, 0)
        n2, big_sort   = quick_sort(big, 0)

        n_comp += n1 # Add comparisons from small items call
        n_comp += n2 # Add comparisons from big items call

        # Reconstruct the input array from the small, pivot and big elements
        input_arr[:] = small_sort + [input_arr[pivot_index]] + big_sort

    return n_comp, input_arr


def merge_sort(input_arr, n_comp):
    """
    Sort array using merge sort
       - Check if list is more than one element (so possibly out of order
       - Split down to single elements
       - Merge back up
       - Return sorted array and number of comparisons
    """

    if len(input_arr) > 1:
        mid   = len(input_arr) // 2 # Find the middle elements
        left  = input_arr[:mid]     # Create the left array
        right = input_arr[mid:]     # Create the right array

        n1, l1 = merge_sort(left, n_comp)  # Recursively sort the lefthand side
        n2, l1 = merge_sort(right, n_comp) # Recursively sort the righthand side

        n_comp += n1 # Add comparisons from smaller left array size
        n_comp += n2 # Add comparisons from smaller right array size

        l, r = 0, 0  # Indices for the left and right lists

        for i in range(len(input_arr)):
            lval = left[l]  if l < len(left)  else None # Account for odd length
            rval = right[r] if r < len(right) else None # Account for odd length

            if (lval is not None and rval is not None and lval < rval) or rval is None:
                input_arr[i] = lval
                l            += 1 # Increment index for left
                n_comp       += 1 # Increment number of comparisons
            elif (lval is not None and rval is not None and lval >= rval) or lval is None:
                input_arr[i] = rval
                r            += 1 # Increment index for right
                n_comp       += 1 # Increment number of comparisons
            else:
                return None, None
                
    return n_comp, input_arr


def compare_iter(arr_len, n_iter):
    """
    Use bubble, quick and merge sorts of random arrays of a set length,
    for n_iter times. Then return mean and standard deviations of results
    The arrays are limited to values less than 1000.
    """
    bubble_comps = []
    quick_comps  = []
    merge_comps  = []

    # Perform sorting the required number of times:
    for ind in range(n_iter):
        rand_arr = np.random.randint(1000, size = arr_len)
        bubble_comps.append(bubble_sort(rand_arr, 0))
        quick_comps.append(quick_sort(rand_arr, 0))
        merge_comps.append(merge_sort(rand_arr, 0))

    # Extract the number of comparisons:
    bub_no = np.array([x[0] for x in bubble_comps])
    qck_no = np.array([x[0] for x in quick_comps])
    mrg_no = np.array([x[0] for x in merge_comps])

    # Calculate mean and standard deviations:
    bub_mean   = np.nanmean(bub_no)
    qck_mean   = np.nanmean(qck_no)
    mrg_mean   = np.nanmean(mrg_no)
    bub_stddev = np.nanstd(bub_no)
    qck_stddev = np.nanstd(qck_no)
    mrg_stddev = np.nanstd(mrg_no)

    # Return the means and standard deviations
    return bub_mean, bub_stddev, qck_mean, qck_stddev, mrg_mean, mrg_stddev


def nlogn_func(x, a, b):
    """
    Helper function for SciPy curve_fit
    """
    return a * x * np.log(x) + b


def quad_func(x, a, b, c):
    """
    Helper function for SciPy curve_fit
    """
    return a + b * x + c * x**2.0

if __name__ == "__main__":
    """
    Test sorting algorithms
    """

    # Set up parameters and output arrays
    n_iter      = 1000
    arr_lens    = np.array([2, 3, 4, 5, 8, 10, 20, 30, 50, 75, 100, 150]) # Longer is really slow
    bub_means   = np.zeros_like(arr_lens)
    bub_stddevs = np.zeros_like(arr_lens)
    qck_means   = np.zeros_like(arr_lens)
    qck_stddevs = np.zeros_like(arr_lens)
    mrg_means   = np.zeros_like(arr_lens)
    mrg_stddevs = np.zeros_like(arr_lens)
    
    # Test each length of array:
    for ind in range(len(arr_lens)):
        print("Testing array length: n =", arr_lens[ind])
        bub_means[ind], bub_stddevs[ind], qck_means[ind], qck_stddevs[ind], mrg_means[ind], mrg_stddevs[ind] = compare_iter(arr_lens[ind], n_iter)


    # Fit expected curves to the results:
    #bub_fit = np.polyfit(arr_lens, bub_means, 2, w = np.divide(1.0, bub_stddevs))
    bub_fit, bub_cov = curve_fit(quad_func, arr_lens, bub_means)
    qck_fit, qck_cov = curve_fit(nlogn_func, arr_lens, qck_means)
    mrg_fit, mrg_cov = curve_fit(nlogn_func, arr_lens, mrg_means)

    bub_mod = quad_func(arr_lens, bub_fit[0], bub_fit[1], bub_fit[2])
    qck_mod = nlogn_func(arr_lens, qck_fit[0], qck_fit[1])
    mrg_mod = nlogn_func(arr_lens, mrg_fit[0], mrg_fit[1])

    # Set up plot canvas defaults
    plt.rc("figure", figsize = [6, 6])
    plt.rc("figure", dpi = 200)
    plt.rc("text", usetex = "True")
    plt.rc("font", family = "serif")
    plt.rc("font", serif = "Times New Roman")
    plt.rc("ps", usedistiller = "xpdf")
    plt.rc("axes", linewidth = 0.5)
    plt.rc("legend", frameon = "False")
    plt.rc("patch", linewidth = 0.5)
    plt.rc("patch", facecolor = "black")
    plt.rc("patch", edgecolor = "black")
    plt.rc("xtick", labelsize = "8")
    plt.minorticks_on()

    # Set up specifics for this plot (log/lin, labels etc)
    fig, ax = plt.subplots()
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel(r"Number of comparisons")
    ax.set_xlabel(r"Array length")
    ax.set_xlim([1, 300])
    ax.set_ylim([0.5,3e4])

    # Plot results
    plt.plot(arr_lens, bub_mod, "k--")
    plt.plot(arr_lens, qck_mod, "b--")
    plt.plot(arr_lens, mrg_mod, "r--")
    plt.scatter(arr_lens, bub_means, color = "k", s = 10, \
                    label = "Bubble sort: $O(n^{2})$")
    plt.scatter(arr_lens, qck_means, color = "b", s = 10, \
                    label = "Quick sort: $O(n \log{n})$")
    plt.scatter(arr_lens, mrg_means, color = "r", s = 10, \
                    label = "Merge sort: $O( n \log{n})$")

    # Add legend:
    plt.legend(loc = "upper left")

    # Save plot:
    plt.savefig("sorting_comparison.png")
    plt.savefig("sorting_comparison.pdf")

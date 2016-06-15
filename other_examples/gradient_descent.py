#!/usr/bin/env python3

"""
Write a simple code to perform gradient descent fitting on a simple linear model
This can be solved analytically, but this is to demonstrate the methodology
(Also note, this doesn't account for local minima)
Owen Littlejohns 2016-06-14
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager


def create_data(number_points):
    """
    Create fake linear data:
        1) Randomise parameters for the model
        2) Create gridded independent variable values
        3) Create perfect dependent variable values from model
        4) Include Gaussian fluctuations standard deviation = 10

    Inputs:
        number_points:     float - number of random data points
        number_parameters: float - number of parameters in model

    Outputs:
        x_values:   data x values
        y_values:   data y values
        parameters: randomized parameters for later comparison
    """

    # Parameters:
    parameters = np.random.uniform(-20, 20, (2, 1))

    # The form for picking lists of input variables (e.g. x, y, z)
    x = np.ones(shape = (number_points, 2))
    y = np.zeros(shape = number_points)

    x[:, 1] = np.linspace(-100, 100, num = number_points)

    # Calculate perfect values for random parameters values:
    perfect_values = np.dot(x, parameters)
    perfect_values = np.array(perfect_values)

    # Create random scatter
    scatter_range = (np.max(perfect_values) - np.min(perfect_values)) / 10.0
    independent_scatter = np.random.uniform(-scatter_range, scatter_range, 
                                             (number_points, 1))

    # Include scatter to scramble the correlation a bit
    y = np.add(perfect_values, independent_scatter)

    # Output data, with model parameters
    return x, y, parameters


def parameter_update(x, y, step_size, input_parameters):
    """
    1) Calculate the gradient for each parameter
    2) simultaneously update the input parameters to new values
    3) Return new parameter values
   
    Inputs:
        dependent_variable:    np.array - input variable values
        independent_variables: np.array - actual values trying to recreate
        step_size:             float     - learning rate (alpha)
        input_parameters:      np.array - parameter values before gradient 
                                           descent step

    Outputs:
        output_parameters: modified parameters after gradient descent step
    """
    output_parameters = np.zeros_like(input_parameters)

    # Calculate the model values:
    model_predictions = np.dot(x, input_parameters)

    # Calculate differences:
    model_differences = model_predictions - y

    # Calculate the gradients for all parameters
    gradients = np.dot(np.transpose(x), model_differences)

    # Update all parameters simultaneously
    output_parameters = input_parameters - (gradients * step_size / float(len(y)))

    return output_parameters



def calculate_cost(x, y, parameters):
    """
    Calculate model predictions, find cost functin
   
    Inputs:
        x:          np.array - input variable values
        y:          np.array - actual values trying to recreate
        parameters: np.array - parameter values before gradient descent step

    Outputs:
        cost_value: cost function, J, for those parameter values
    """
    model_predictions = x * parameters

    # Calculate differences:
    model_differences = model_predictions - y

    # Calculate cost function value
    cost_value = np.sum(np.multiply(model_differences, model_differences)) / (2.0 * len(y))

    return cost_value


if __name__ == "__main__":
    # Create new random data
    x, y, original_parameters = create_data(250)

    # Define fitting characteristics
    guess_list = []

    for ind in range(len(original_parameters)):
        guess_list += [[1]]

    guess_parameters = np.matrix(guess_list)
    step_size = 0.0005 # This is a very sensitive parameter
    new_cost = 10000.0
    cost_threshold = 100.0
    temp_params = guess_parameters
    n_steps = 0
    step_limit = 100000 # The more steps, the closer you get - but takes longer

    while new_cost > cost_threshold and n_steps < step_limit:
        new_parameters = parameter_update(x, y, step_size, temp_params)
        new_cost = calculate_cost(x, y, guess_parameters)
        n_steps += 1
        temp_params = new_parameters

        if n_steps == step_limit:
            "Maximum number of steps reached"
    
    # Save the best fit
    best_parameters = temp_params

    """
    Plot out the results:
    """

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
    ax.set_xlabel(r"Independent variable")
    ax.set_ylabel(r"Dependent variable")

    model_predictions = np.dot(x, best_parameters)

    plt.scatter(np.array(x)[:, 1], np.array(y)[:, 0], color = "k", s = 8,
                label = "Randomly generated data")
    plt.plot(np.array(x)[:, 1], np.array(model_predictions)[:, 0], "g-",
             label = "Results of gradient descent")
    if float(best_parameters[1][0]) > 0:
        plt.legend(loc = "upper left")
    else:
        plt.legend(loc = "upper right")

    plt.savefig("gradient_descent.png")

    print("Original fit:", np.transpose(np.array(original_parameters[:, 0])))
    print("Best fit:", np.transpose(np.array(best_parameters[:, 0])))
    print("Cost:", calculate_cost(x, y, best_parameters))



from math import comb
from random import randrange
from statistics import variance

from pytest import param
from .base import RunManager
import numpy as np
import itertools
from stonesoup.types.array import StateVector, CovarianceMatrix
from stonesoup.types.numeric import Probability
from datetime import datetime, timedelta
import random


class InputManager(RunManager):
    def __init__(self, montecarlo, seed) -> None:
        super().__init__()
        self.seed = random.seed(seed)
        self.montecarlo = montecarlo

    def set_stateVector(self, list_state_vector):
        """Get a list and return a state vector

        Parameters:
            list_state_vector: State vector list

        Returns:
            StateVector: state vector
        """
        vector_list = []
        for idx, elem in enumerate(list_state_vector):
            vector_list.append(StateVector(elem))
        return vector_list

    def set_int(self, input_int):
        """
        Set int

        Parameters:
            input_int: value to convert

        Returns:
            int: int value
        """
        input_int = int(input_int)
        return input_int

    def set_float(self, input_float):
        """
        Set float

        Parameters:
            input_float: value to convert

        Returns:
            float: float value
        """
        input_float = float(input_float)
        return input_float

    def set_covariance(self, covar):
        """Get a list and return a covar

        Parameters:
            list_state_covar: covar vector list

        Returns:
            CovarianceMatrix: covariance
        """
        covar_list = []
        for idx, elem in enumerate(covar):
            covariance_matrix = np.zeros((len(elem), len(elem)), dtype=int)
            np.fill_diagonal(covariance_matrix, list(elem))
            covar_list.append(CovarianceMatrix(covariance_matrix))
        return covar_list

    def set_tuple(self, list_tuple):
        """
        Set tuple

        Parameters:
            input_tuple: list of tuple

        Returns:
            tuple: tuple
        """
        tuple_list = []
        for idx, elem in enumerate(list_tuple):
            tuple_list.append(tuple(elem))
        return tuple_list

    def set_bool():
        """
        Set bool

        Parameters:
            input_bool: value to convert

        Returns:
            bool: bool value
        """
        raise NotImplementedError

    def set_ndArray(self, arr):
        """
        Set ndArray

        Parameters:
            input_ndarray: value to convert

        Returns:
            ndarray: ndarray value
        """
        return np.array(arr)

    def set_time_delta(self, time_delta):
        """
        Set timedelta

        Parameters:
            input_timedelta: value to convert

        Returns:
            timedelta: timedelta value
        """
        return timedelta(time_delta)

    def set_probability():
        """
        Set probability

        Parameters:
            input_probability: value to convert

        Returns:
            Probability: probability value
        """
        raise NotImplementedError

    def state_vector_helper(self, parameter):
        if self.montecarlo == 0:
            combinations = self.generate_combinations_list(parameter)
        elif self.montecarlo == 1:
            NotImplementedError
        elif self.montecarlo == 2:
            NotImplementedError
        elif self.montecarlo == 3:
            combinations = self.variance_distribution_list(parameter)
        combinations = self.get_array_list(combinations, len(parameter["value_min"]))
        output_values = self.set_stateVector(combinations)
        return output_values

    def integer_helper(self, parameter):
        if self.montecarlo == 0:
            combinations = self.generate_combinations(parameter)
        elif self.montecarlo == 1:
            NotImplementedError
        elif self.montecarlo == 2:
            NotImplementedError
        elif self.montecarlo == 3:
            combinations = self.variance_distribution(parameter)
        output_values = [int(x) for x in combinations]

        return output_values
    
    def float_helper(self, parameter):
        if self.montecarlo == 0:
            combinations = self.generate_combinations(parameter)
        elif self.montecarlo == 1:
            NotImplementedError
        elif self.montecarlo == 2:
            NotImplementedError
        elif self.montecarlo == 3:
            combinations = self.variance_distribution(parameter)
        output_values = [float(x) for x in combinations]

        return output_values

    def probability_helper(self, parameter):
        if self.montecarlo == 0:
            combinations = self.generate_combinations(parameter)
        elif self.montecarlo == 1:
            NotImplementedError
        elif self.montecarlo == 2:
            NotImplementedError
        elif self.montecarlo == 3:
            combinations = self.variance_distribution(parameter)
        output_values = [Probability(x) for x in combinations]

        return output_values
    
    def generate_parameters_combinations(self, parameters):
        """From a list of parameters with, min, max and n_samples values
        generate all the possible values

        Parameters
        ----------
        parameters : list
            list of parameters used to calculate all the possible combinations

        Returns
        -------
        dict:
            dictionary of all the combinations
        """
        combination_dict = {}
        for parameter in parameters:
            combination_list = {}
            path = parameter["path"]
            try:
                if parameter["type"] == "StateVector":
                    combination_list[path] = self.state_vector_helper(parameter)
                    combination_dict.update(combination_list)

                if parameter["type"] == "int":
                    combination_list[path] = self.integer_helper(parameter)
                    combination_dict.update(combination_list)

                if parameter["type"] == "float":
                    combination_list[path] = self.float_helper(parameter)
                    combination_dict.update(combination_list)

                if parameter["type"] == "Probability":
                    combination_list[path] = self.probability_helper(parameter)
                    combination_dict.update(combination_list)

                if parameter["type"] == 'bool':
                    # Doesn't require changing for monte-carlo
                    combination_list = self.generate_bool_combinations(parameter)
                    combination_dict.update(combination_list)

                if parameter["type"] == "CovarianceMatrix":
                    combination_list = self.generate_covariance_combinations(parameter)
                    combination_dict.update(combination_list)

                if parameter["type"] == "DateTime":
                    combination_list = self.generate_date_time_combinations(parameter)
                    combination_dict.update(combination_list)

                if (parameter["type"] == "Tuple"):
                    combination_list = self.generate_tuple_list_combinations(parameter)
                    combination_dict.update(combination_list)

                if parameter["type"] == "timedelta":
                    iteration_list = self.generate_combinations(parameter)
                    combination_list[path] = [self.set_time_delta(x) for x in iteration_list]
                    combination_dict.update(combination_list)

                if parameter["type"] == "ndarray":
                    combination_list = self.generate_ndarray_combinations(parameter)
                    combination_dict.update(combination_list)

            except KeyError:
                pass

        return combination_dict

    # def logarithmic_range_gen(self, parameter):
    #     log_scale = np.random.lognormal(size=[parameter["value_min"], parameter["value_max"]])
    #     return log_scale

    def exponential_range_gen(self, parameter):
        exponential = np.random.exponential(scale=1.0,
                                            size=[parameter["value_min"],
                                                  parameter["value_max"]])
        return exponential

    def compare_min_max(self, list):
        NotImplementedError

    def generate_ndarray_combinations(self, parameter):
        """Generate combinations of ndarray

        Parameters
        ----------
        parameter : dict
            dictionary of the parameter with value_max, value_min, n_samples and path

        Returns
        -------
        set
            set of all the possible values
        """
        path = parameter["path"]
        combination_list = {}
        iteration_list = []
        if parameter["value_min"].size > 0 and parameter["value_max"].size > 0:
            for x in range(len(parameter["value_min"])):
                iteration_list.append(self.iterations(parameter["value_min"][x],
                                                      parameter["value_max"][x],
                                                      parameter["n_samples"][x]))
            combination_list[path] = self.set_ndArray(self.get_array_list(
                iteration_list, len(parameter["value_min"])))
        return combination_list

    def generate_timedelta_combinations(self, parameter):
        """Generate combinations of timedelta

        Parameters
        ----------
        parameter : dict
            dictionary of the parameter with value_max, value_min, n_samples and path

        Returns
        -------
        set
            set of all the possible values
        """
        path = parameter["path"]
        combination_list = {}
        iteration_list = self.iterations(parameter["value_min"],
                                         parameter["value_max"],
                                         parameter["n_samples"])
        combination_list[path] = [self.set_time_delta(x) for x in iteration_list]
        return combination_list

    def generate_tuple_list_combinations(self, parameter):
        """Generate combinations of tuple or list

        Parameters
        ----------
        parameter : dict
            dictionary of the parameter with value_max, value_min, n_samples and path

        Returns
        -------
        set
            set of all the possible values
        """
        path = parameter["path"]
        combination_list = {}
        iteration_list = []
        if len(parameter['value_min']) > 0 and len(parameter['value_max']) > 0:
            for x in range(len(parameter["value_min"])):
                iteration_list.append(self.iterations(parameter["value_min"][x],
                                                      parameter["value_max"][x],
                                                      parameter["n_samples"][x]))
            combination_list[path] = self.get_array_list(iteration_list,
                                                         len(parameter["value_min"]))

            if parameter["type"] == "Tuple":
                combination_list[path] = self.set_tuple(combination_list[path])
            if parameter["type"] == "list":
                combination_list[path] = [list(i) for i in combination_list[path]]
        return combination_list

    def generate_date_time_combinations(self, parameter):
        """Generate combinations of date time

        Parameters
        ----------
        parameter : dict
            dictionary of the parameter with value_max, value_min, n_samples and path

        Returns
        -------
        set
            set of all the possible values
        """
        path = parameter["path"]
        combination_list = {}
        min_date = datetime.strptime(parameter["value_min"], '%Y-%m-%d %H:%M:%S.%f')
        max_date = datetime.strptime(parameter["value_max"], '%Y-%m-%d %H:%M:%S.%f')
        iteration_list = self.iterations(min_date, max_date, parameter["n_samples"])
        combination_list[path] = iteration_list
        return combination_list

    def generate_covariance_combinations(self, parameter):
        """Generate combinations of covariance matrix

        Parameters
        ----------
        parameter : dict
            dictionary of the parameter with value_max, value_min, n_samples and path

        Returns
        -------
        set
            set of all the possible values
        """
        path = parameter["path"]
        combination_list = {}
        # iteration_list = []
        # n_samples = parameter["n_samples"]
        # n_samples_matrix = np.zeros((len(n_samples), len(n_samples)), dtype=int)
        # np.fill_diagonal(n_samples_matrix, n_samples)
        # min_val = parameter["value_min"]
        # covar_min_array = np.zeros((len(min_val), len(min_val)), dtype=int)
        # np.fill_diagonal(covar_min_array, min_val)
        # max_val = parameter["value_max"]
        # covar_max_array = np.zeros((len(max_val), len(max_val)), dtype=int)
        # np.fill_diagonal(covar_max_array, max_val)

        if len(parameter['value_min']) > 0 and len(parameter['value_max']) > 0:
            path = parameter["path"]
            iteration_list = []
            if type(parameter["n_samples"]) is list:
                for x in range(len(parameter['value_min'])):
                    iteration_list.append(self.iterations(parameter["value_min"][x],
                                                          parameter["value_max"][x],
                                                          parameter["n_samples"][x]))
            combination_list[path] = self.set_covariance(self.get_array_list(iteration_list,
                                                         len(parameter["value_min"])))
        return combination_list

    def generate_bool_combinations(self, parameter):
        """Generate combinations of bool

        Parameters
        ----------
        parameter : dict
            dictionary of the parameter with value_max, value_min, n_samples and path

        Returns
        -------
        set
            set of all the possible values
        """
        path = parameter["path"]
        combination_list = {}
        combination_list[path] = [True, False]
        return combination_list

    def generate_probability_combinations(self, parameter):
        """Generate combinations of probability

        Parameters
        ----------
        parameter : dict
            dictionary of the parameter with value_max, value_min, n_samples and path

        Returns
        -------
        set
            set of all the possible values
        """
        path = parameter["path"]
        combination_list = {}
        iteration_list = self.iterations(parameter["value_min"],
                                         parameter["value_max"],
                                         parameter["n_samples"])
        combination_list[path] = [Probability(x) for x in iteration_list]
        return combination_list

    def generate_combinations(self, parameter):
        """Generate combinations of float

        Parameters
        ----------
        parameter : dict
            dictionary of the parameter with value_max, value_min, n_samples and path

        Returns
        -------
        set
            set of all the possible values
        """
        # path = parameter["path"]
        # combination_list = {}
        iteration_list = self.iterations(parameter["value_min"],
                                         parameter["value_max"],
                                         parameter["n_samples"])

        return iteration_list

    def generate_int_combinations(self, parameter):
        """Generate combinations of int

        Parameters
        ----------
        parameter : dict
            dictionary of the parameter with value_max, value_min, n_samples and path

        Returns
        -------
        set
            set of all the possible values
        """
        path = parameter["path"]
        combination_list = {}
        # iteration_list = []
        iteration_list = self.iterations(parameter["value_min"],
                                         parameter["value_max"],
                                         parameter["n_samples"])
        combination_list[path] = [int(x) for x in iteration_list]
        return combination_list

    def generate_state_vector_combinations(self, parameter):
        """Generate combinations of state vector

        Parameters
        ----------
        parameter : dict
            dictionary of the parameter with value_max, value_min, n_samples and path

        Returns
        -------
        set
            set of all the possible values
        """
        combination_list = {}

        if len(parameter['value_min']) > 0 and len(parameter['value_max']) > 0:
            path = parameter["path"]
            iteration_list = []
            if type(parameter["n_samples"]) is list:
                for x in range(len(parameter['value_min'])):
                    iteration_list.append(self.iterations(parameter["value_min"][x],
                                                          parameter["value_max"][x],
                                                          parameter["n_samples"][x]))
            else:
                for x in range(parameter['value_min']):
                    iteration_list.append(self.iterations(parameter["value_min"][x],
                                                          parameter["value_max"][x],
                                                          parameter["n_samples"]))

            combination_list[path] = self.set_stateVector(
                        self.get_array_list(iteration_list, len(parameter["value_min"])))

        return combination_list

    def darray_navigator(self, val, val_min, val_max, iteration_list, n_samples):
        """Not used at the moment. Navigate inside the ndarray with a n depth and
        calculate all the iterations

        Parameters
        ----------
        val : [type]
            [description]
        val_min : [type]
            [description]
        val_max : [type]
            [description]
        iteration_list : [type]
            [description]
        n_samples : int
            number of parameter combinations
        """
        if(type(val) is list):
            for x in range(len(val)):
                new_iteration_list = []
                iteration_list.append(new_iteration_list)
                self.darray_navigator(val[x], val_min[x], val_max[x],
                                      new_iteration_list, n_samples)
        else:
            iteration_list.append(self.iterations(val_min, val_max, n_samples))

    # Calculate the steps for each item in a list
    def iterations(self, min_value, max_value, num_samples, index=0):
        """Calculates the step different between the min
            and max value given in the parameter file.
            If n_samples is 0 return 1 value, if it is >=1 return num_samples+2 values

        Parameters
        ----------
        min_value : Object
            Minimum parameter value
        max_value : Object
            Minimum parameter value
        num_samples : int
            number of parameter samples to calculate
        index : int, optional
            [description], by default 0

        Returns
        -------
        list
            list of steps required for the monte-carlo run
        """
        temp = []

        # If num_samples is 0 or less don't calculate any
        if num_samples <= 0 or min_value == max_value or num_samples is None:
            temp.append(min_value)
            if min_value != max_value:
                temp.append(max_value)
            return temp

        else:
            difference = max_value - min_value
            factor = difference / (num_samples+1)
            # Calculate n_samples different samples plus min_value and max_value
            for x in range(0, num_samples+2):
                temp.append(min_value + (x * factor))
            return temp

    def get_array_list(self, iterations_container_list, n):
        """Gets the combinations for one list of state vector and stores in list
           Once you have steps created from iterations, generate step combinations
           for one parameter

        Parameters:
            iterations_container_list (list): list all the possible values
            n (list): list of value min

        Returns:
            list: list all the possible combinations
        """

        array_list = []
        for x in range(0, n):
            array_list.append(iterations_container_list[x])

        list_combinations = list(itertools.product(*array_list))
        # Using a set to remove any duplicates
        set_combinations = list(set(list_combinations))
        return set_combinations

    def get_ndarray_trackers_list(self, iterations_container_list, n):
        """Gets the combinations for one list of ndarray and stores in list
           Once you have steps created from iterations, generate step combinations
           for one parameter

        Parameters:
            iterations_container_list (list): list all the possible values
            n (list): list of value min

        Returns:
            list: list all the possible combinations
        """
        array_list = []
        for x in range(0, n):
            array_list.append(iterations_container_list[x])

        list_combinations = [list(tup) for tup in itertools.product(*array_list)]
        # Using a set to remove any duplicates
        # set_combinations = list(set(list_combinations))

        return list_combinations

    def get_covar_trackers_list(self, iteration_list, n):
        """Gets the combinations for one list of ndarray and stores in list
           Once you have steps created from iterations, generate step combinations
           for one parameter

        Parameters:
            iteration_list (list): list all the possible values
            value_min ([type]): [description]

        Returns:
            list: list all the possible combinations
        """
        temp = []
        combinations = []
        for x in range(0, n):
            temp.append(iteration_list[x])
        list_combinations = list(itertools.product(*temp))
        set_combinations = np.array(list(set(list_combinations)))
        for y in set_combinations:
            temp_array = np.zeros((n, n), dtype=int)
            np.fill_diagonal(temp_array, y)
            combinations.append(temp_array)
        return combinations

    # Generates all of the combinations between different parameters
    def generate_all_combos(self, trackers_dict):
        """Generates all of the combinations between different parameters

        Parameters:
            trackers_dict (dict): Dictionary of all the parameters with all the possible values

        Returns:
            dict: Dictionary of all the parameters combined each other
        """
        keys = trackers_dict.keys()
        values = (trackers_dict[key] for key in keys)
        combinations = [dict(zip(keys, combination)) for combination in itertools.product(*values)]
        return combinations

    def logarithmic_range_gen(self, parameter):
        path = parameter["path"]
        combination_list = {}
        iteration_list = []
        if parameter["type"] == "StateVector":
            if type(parameter["n_samples"]) is list:
                for x in range(len(parameter['value_min'])):
                    iteration_list.append(np.logspace(np.log10(parameter["value_min"][x]),
                                                      np.log10(parameter["value_max"][x]),
                                                      parameter["n_samples"][x],
                                                      dtype=int, base=10))
                combination_list[path] = self.set_stateVector(self.get_array_list(
                                                            iteration_list,
                                                            len(parameter["value_min"])))
            else:
                for x in range(parameter['value_min']):
                    iteration_list.append(np.logspace(np.log10(parameter["value_min"][x]),
                                                      np.log10(parameter["value_max"][x]),
                                                      parameter["n_samples"],
                                                      dtype=int, base=10))
                combination_list[path] = self.set_stateVector(self.get_array_list(
                                                            iteration_list,
                                                            len(parameter["value_min"])))


        elif parameter["type"] == "int":
            iteration_list = np.logspace(np.log10(parameter["value_min"]),
                                         np.log10(parameter["value_max"]),
                                         parameter["n_samples"],
                                         dtype=int, base=10)
            combination_list[path] = iteration_list

        elif parameter["type"] == "float":
            iteration_list = np.logspace(np.log10(parameter["value_min"]),
                                         np.log10(parameter["value_max"]),
                                         parameter["n_samples"],
                                         dtype=float, base=10)
            combination_list[path] = iteration_list

        elif parameter["type"] == "Probability":
            iteration_list = np.logspace(np.log10(parameter["value_min"]),
                                         np.log10(parameter["value_max"]),
                                         parameter["n_samples"],
                                         dtype=Probability, base=10)
            combination_list[path] = iteration_list

        elif parameter["type"] == "bool":
            iteration_list = [True, False]
            combination_list[path] = iteration_list

        elif parameter["type"] == "CovarianceMatrix":
            if type(parameter["n_samples"]) is list:
                for x in range(len(parameter['value_min'])):
                    iteration_list.append(np.logspace(np.log10(parameter["value_min"][x]),
                                                      np.log10(parameter["value_max"][x]),
                                                      parameter["n_samples"][x],
                                                      dtype=int, base=10))
            combination_list[path] = self.set_covariance(self.get_array_list(
                                                         iteration_list,
                                                         len(parameter["value_min"])))

        elif parameter["type"] == "timedelta":
            iteration_list = np.logspace(np.log10(parameter["value_min"]),
                                         np.log10(parameter["value_max"]),
                                         parameter["n_samples"],
                                         dtype=timedelta, base=10)
            combination_list[path] = iteration_list

        return combination_list

    def variance_distribution(self, parameter):
        """Creates a list of random values within a 10% tolerance for each
        index within the list.

        Parameters
        ----------
        combination_list : dict
            Dictionary value of generated parameters

        Returns
        -------
        dict
            Returns a new dictionary of values with a random variation of 10%
        """
        combination_list = self.generate_combinations(parameter)
        key = parameter["path"]
        random_list = []
        for idx in combination_list:
            random_num = random.randrange(int(idx*0.9), int(idx*1.1))
            random_list.append(random_num)
        return random_list

    def variance_distribution_list(self, parameter):
        """Creates a list of random values within a 10% tolerance for each
        index within the list.

        Parameters
        ----------
        combination_list : dict
            Dictionary value of generated parameters

        Returns
        -------
        dict
            Returns a new dictionary of values with a random variation of 10%
        """
        combination_list = self.generate_combinations_list(parameter)
        for c_idx, c_value in enumerate(combination_list):
            for v_idx, v_value in enumerate(c_value):
                if v_idx == 0:
                    combination_list[c_idx][v_idx] = 0
                else:
                    random_num = random.randrange(int(v_value*0.9), int(v_value*1.1))
                    combination_list[c_idx][v_idx] = random_num
        return combination_list

    def generate_combinations_list(self, parameter):
            """Generate combinations for a list type from json

            Parameters
            ----------
            parameter : dict
                dictionary of the parameter with value_max, value_min, n_samples and path

            Returns
            -------
            set
                set of all the possible values
            """
            combination_list = {}

            if len(parameter['value_min']) > 0 and len(parameter['value_max']) > 0:
                path = parameter["path"]
                iteration_list = []
                if type(parameter["n_samples"]) is list:
                    #if n_samples is a list (changing each parameter individually)
                    for x in range(len(parameter['value_min'])):
                        iteration_list.append(self.iterations(parameter["value_min"][x],
                                                            parameter["value_max"][x],
                                                            parameter["n_samples"][x]))
                else:
                    # If n_samples is a single value
                    for x in range(parameter['value_min']):
                        iteration_list.append(self.iterations(parameter["value_min"][x],
                                                            parameter["value_max"][x],
                                                            parameter["n_samples"]))

            return iteration_list

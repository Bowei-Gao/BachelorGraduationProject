import random
from jmetal.core.problem import BinaryProblem
from jmetal.core.solution import BinarySolution


class Knapsack(BinaryProblem):
    """ Class representing Knapsack Problem. """

    def __init__(self, level_of_requirements: int, numbers_of_requirements: list, costs: list,
                 number_of_dependencies: int, dependencies: list, number_of_customers: int, profits: list
                 , numbers_of_requests: list, requests: list):
        super(Knapsack, self).__init__()

        self.level_of_requirements = level_of_requirements
        self.numbers_of_requirements = numbers_of_requirements
        self.costs = costs
        self.number_of_dependencies = number_of_dependencies
        self.dependencies = dependencies
        self.number_of_customers = number_of_customers
        self.profits = profits
        self.numbers_of_requests = numbers_of_requests
        self.requests = requests

        self.number_of_bits = sum(numbers_of_requirements)
        self.number_of_variables = 1
        self.obj_directions = [self.MAXIMIZE, self.MAXIMIZE]
        self.number_of_objectives = 2
        self.number_of_constraints = 1

    def evaluate(self, solution: BinarySolution) -> BinarySolution:
        total_profits = 0.0
        total_costs = 0.0

        customer_variable = self.number_of_customers * [True]
        requirement_variable = solution.variables[0]

        for i in range(self.number_of_dependencies):
            requirement_variable[self.dependencies[i][1] - 1] = \
                requirement_variable[self.dependencies[i][0] - 1] and requirement_variable[self.dependencies[i][1] - 1]

        for i in range(self.number_of_customers):
            for j in range(self.numbers_of_requests[i]):
                customer_variable[i] = customer_variable[i] and requirement_variable[self.requests[i][j] - 1]

        for index, bits in enumerate(requirement_variable):
            if bits:
                total_costs += self.costs[index]

        for index, bits in enumerate(customer_variable):
            if bits:
                total_profits += self.profits[index]

        solution.objectives[0] = -1.0 * total_profits
        solution.objectives[1] = total_costs
        return solution

    def create_solution(self) -> BinarySolution:
        new_solution = BinarySolution(number_of_variables=self.number_of_variables,
                                      number_of_objectives=self.number_of_objectives)

        new_solution.variables[0] = \
            [True if random.randint(0, 1) == 0 else False for _ in range(
                self.number_of_bits)]

        return new_solution

    def get_name(self):
        return 'Knapsack'

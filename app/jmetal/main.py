from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import SPXCrossover, BitFlipMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.solution import get_non_dominated_solutions
from app.nrp_instances.file_operations import read_file
from app.jmetal.problem import Knapsack
import datetime


def jmatal():
    start_time = datetime.datetime.now()
    level_of_requirements, numbers_of_requirements, costs, number_of_dependencies, dependencies, number_of_customers, \
        profits, numbers_of_requests, requests = read_file()

    problem = Knapsack(level_of_requirements, numbers_of_requirements, costs, number_of_dependencies, dependencies,
                       number_of_customers, profits, numbers_of_requests, requests)

    solutions = []

    for i in range(20):
        algorithm = NSGAII(
            problem=problem,
            population_size=500,
            offspring_population_size=500,
            mutation=BitFlipMutation(probability=1.0 / problem.number_of_variables),
            crossover=SPXCrossover(probability=1.0),
            termination_criterion=StoppingByEvaluations(max_evaluations=25000)
        )

        algorithm.run()
        solutions.extend(algorithm.get_result())

    front = get_non_dominated_solutions(solutions)

    solutions = []

    for i in range(len(front)):
        solutions.append([-front[i].objectives[0], front[i].objectives[1]])

    def calculate_evenness(solutions):
        d = []
        for i in range(len(solutions)):
            if i != 0:
                d1 = ((solutions[i][0] - solutions[i - 1][0]) ** 2 + (
                        solutions[i][1] - solutions[i - 1][1]) ** 2) ** 0.5
            else:
                d1 = 0
            if i != len(solutions) - 1:
                d2 = ((solutions[i][0] - solutions[i + 1][0]) ** 2 + (
                        solutions[i][1] - solutions[i + 1][1]) ** 2) ** 0.5
            else:
                d2 = 0
            d.append(max(d1, d2))
        average_d = sum(d) / len(d)
        sum_1 = 0
        for di in d:
            sum_1 += (average_d - di) ** 2
        evenness = (sum_1 / (len(solutions) - 1)) ** 2
        return evenness

    evenness = calculate_evenness(solutions)

    end_time = datetime.datetime.now()
    total_time = str((end_time - start_time).seconds) + "s"
    return total_time, evenness, len(solutions), solutions

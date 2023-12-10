from cplex import Cplex
from app.nrp_instances.file_operations import read_file
import datetime


def optimize_interval():
    start_time = datetime.datetime.now()

    level_of_requirements, number_of_requirements, cost, number_of_dependencies, dependencies, \
        number_of_customers, profit, number_of_requests, requests = read_file()

    # employ a cplex solver
    ilp_solver = Cplex()
    # disable output
    ilp_solver.set_results_stream(None)
    ilp_solver.set_warning_stream(None)
    ilp_solver.set_error_stream(None)
    # auto thread number
    ilp_solver.parameters.threads.set(0)
    # tolerance set 0 for exact solution
    ilp_solver.parameters.emphasis.mip.set(0)
    ilp_solver.parameters.mip.tolerances.absmipgap.set(0.0)
    ilp_solver.parameters.mip.tolerances.mipgap.set(0.0)

    # add variables
    sum_number_of_requirements = sum(number_of_requirements)
    types_x = ['B'] * sum_number_of_requirements  # 'B' for binary variables
    variables_x = ['x' + str(i) for i in range(sum_number_of_requirements)]  # variable names
    ilp_solver.variables.add(obj=None, lb=None, ub=None, types=types_x, names=variables_x)
    types_y = ['B'] * number_of_customers  # 'B' for binary variables
    variables_y = ['y' + str(i) for i in range(number_of_customers)]  # variable names
    ilp_solver.variables.add(obj=None, lb=None, ub=None, types=types_y, names=variables_y)

    # add constraint Sum xi wi <= cost
    rows = []
    vari = []
    coef = []
    rhs = 0
    for j in range(sum_number_of_requirements):
        vari.append('x' + str(j))
        coef.append(cost[j])
    rows.append([vari, coef])
    # L for <=, lin_expr <= rhs
    ilp_solver.linear_constraints.add(lin_expr=rows, senses='L', rhs=[rhs], names=['cost_constraint'])

    # add constraint yi <= xj (yi - xj <= 0)
    for i in range(number_of_customers):
        for j in range(number_of_requests[i]):
            rows = []
            vari = []
            coef = []
            rhs = 0
            vari.append('y' + str(i))
            coef.append(1)
            vari.append('x' + str(requests[i][j] - 1))
            coef.append(-1)
            rows.append([vari, coef])
            ilp_solver.linear_constraints.add(lin_expr=rows, senses='L', rhs=[rhs],
                                              names=['and_constraint' + str(i) + str(j)])

    # add constraint xi <= xj (xi - xj <= 0)
    for i in range(number_of_dependencies):
        rows = []
        vari = []
        coef = []
        rhs = 0
        vari.append('x' + str(dependencies[i][0] - 1))
        coef.append(-1)
        vari.append('x' + str(dependencies[i][1] - 1))
        coef.append(1)
        rows.append([vari, coef])
        # L for <=, lin_expr <= rhs
        ilp_solver.linear_constraints.add(lin_expr=rows, senses='L', rhs=[rhs],
                                          names=['dependency_constraint' + str(i)])

    # set objective Max Sum xi pi
    pairs = [('y' + str(i), v) for i, v in enumerate(profit)]  # [(yi, wi)]
    w = 1 / (0 - (-sum(cost)) + 1)
    pairs1 = [('x' + str(i), - w * c) for i, c in enumerate(cost)]
    pairs.extend(pairs1)
    ilp_solver.objective.set_linear(pairs)
    ilp_solver.objective.set_sense(ilp_solver.objective.sense.maximize)

    def CWMOIP(k, lk):
        solutions = []
        if k != 0:
            while lk >= 0:
                ilp_solver.linear_constraints.set_rhs('cost_constraint', lk)
                ME = CWMOIP(k - 1, lk)
                solutions.extend(ME)
                lk = ME[0][1]
                for XE in ME:
                    if lk < XE[1]:
                        lk = XE[1]
                lk = lk - 5
        elif k == 0:
            # solve
            ilp_solver.solve()
            # check solver status
            status = ilp_solver.solution.get_status_string()
            if 'optimal' in status:
                # get variables evaluation
                # get objective value
                variables_evaluation = ilp_solver.solution.get_objective_value()
                objective_value = ilp_solver.solution.get_values()
                solution_cost = 0
                for j in range(sum_number_of_requirements):
                    solution_cost += cost[j] * objective_value[j]
                solution = (int(variables_evaluation + 0.5), int(solution_cost + 0.5))
                solutions.append(solution)
        return solutions

    k = 1
    lk = sum(cost)
    solutions = CWMOIP(k, lk)

    end_time = datetime.datetime.now()
    total_time = str((end_time - start_time).seconds) + "s"

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

    return total_time, evenness, len(solutions), solutions

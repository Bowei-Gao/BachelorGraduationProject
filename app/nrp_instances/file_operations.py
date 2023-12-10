def read_file():
    number_of_requirements, cost, dependencies, profit, number_of_requests, requests = [], [], [], [], [], []
    f = open('./app/uploads/nrp1.txt')
    # f = open('./classic-nrp/nrp1.txt')
    level_of_requirements = int(f.readline())
    for i in range(level_of_requirements):
        number_of_requirements.append(int(f.readline()))
        line = f.readline()
        fields = line.split(' ')
        for j in range(number_of_requirements[i]):
            cost.append(int(fields[j]))
    number_of_dependencies = int(f.readline())
    for _ in range(number_of_dependencies):
        line = f.readline()
        fields = line.split(' ')
        dependencies.append([int(fields[0]), int(fields[1])])
    number_of_customers = int(f.readline())
    for i in range(number_of_customers):
        line = f.readline()
        fields = line.split(' ')
        profit.append(int(fields[0]))
        number_of_requests.append(int(fields[1]))
        request_by_customer = []
        for j in range(2, 2 + number_of_requests[i]):
            request_by_customer.append(int(fields[j]))
        requests.append(request_by_customer)
    f.close()
    return level_of_requirements, number_of_requirements, cost, number_of_dependencies, dependencies,\
        number_of_customers, profit, number_of_requests, requests

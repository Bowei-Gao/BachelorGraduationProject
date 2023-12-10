def read_file():
    numbers_of_requirements, costs, dependencies, profits, numbers_of_requests, requests = [], [], [], [], [], []
    f = open('./app/jmetal/classic-nrp/nrp1.txt')
    # f = open('./classic-nrp/nrp1.txt')
    level_of_requirements = int(f.readline())
    for i in range(level_of_requirements):
        numbers_of_requirements.append(int(f.readline()))
        line = f.readline()
        fields = line.split(' ')
        for j in range(numbers_of_requirements[i]):
            costs.append(int(fields[j]))
    number_of_dependencies = int(f.readline())
    for _ in range(number_of_dependencies):
        line = f.readline()
        fields = line.split(' ')
        dependencies.append([int(fields[0]), int(fields[1])])
    number_of_customers = int(f.readline())
    for i in range(number_of_customers):
        line = f.readline()
        fields = line.split(' ')
        profits.append(int(fields[0]))
        numbers_of_requests.append(int(fields[1]))
        request_by_customer = []
        for j in range(2, 2 + numbers_of_requests[i]):
            request_by_customer.append(int(fields[j]))
        requests.append(request_by_customer)
    f.close()
    return level_of_requirements, numbers_of_requirements, costs, number_of_dependencies, dependencies,\
        number_of_customers, profits, numbers_of_requests, requests

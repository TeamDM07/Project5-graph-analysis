import timeit
# import pandas as pd
start = timeit.default_timer()

# def read_data(path_to_file):
#     """
#     reads file
#     """
#     dataf = pd.read_csv(path_to_file)
#     return dataf
# pandas ефективніший для цього завдання, але пхд його не можна юзати

def read_data1(path_to_file):
    with open(path_to_file, 'r') as file:
        res = []
        for line in file:
            res.append(tuple(line.strip('\n').split()))
        return res

print(read_data1('graph_100000_4998622_1.csv')[:10])
stop = timeit.default_timer()
execution_time = stop - start

print("Program Executed in "+str(execution_time))
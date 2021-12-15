import timeit
import sys
# import pandas as pd
start = timeit.default_timer()
sys.setrecursionlimit(3000)
# def read_data(path_to_file):
#     """
#     reads file
#     """
#     dataf = pd.read_csv(path_to_file)
#     return dataf
# pandas ефективніший для цього завдання, але пхд його не можна юзати
components = []
uv_set = set()

def read_data1(path_to_file):
    """
    вертає список таплів зі стрінгами вершин ребра
    """
    with open(path_to_file, 'r') as file:
        res = []
        file.readline()
        for line in file:
            res.append(tuple(line.strip('\n').split()))
        return res


def creating_dict(res):
    """
    Створює словник з результату функції read_data1
    """
    res_dict = dict()
    for tpl in res:
        res_dict[int(tpl[0])] = res_dict.get(int(tpl[0]), []) + [int(tpl[1])]
    return res_dict


def connectivity_components(vertices_dict):
    def dfs(v, minv, depth):
        depth+=1
        uv_set.add(v)
        for new_v in vertices_dict[v]:
            if new_v not in uv_set and new_v in vertices_dict:
                # print(depth)
                minv = min(minv, new_v, dfs(new_v, minv, depth))
        return minv

    for key in vertices_dict:
        if key not in uv_set:
            components.append(dfs(key, key, 0))

    return len(components)


print(connectivity_components(creating_dict(read_data1('graph_100000_4998622_1.csv')[:110000])))
stop = timeit.default_timer()
execution_time = stop - start

print("Program Executed in "+str(execution_time))

import timeit

start = timeit.default_timer()

all_verticles = set()


def read_data1(path_to_file):
    """
    вертає список таплів зі стрінгами вершин ребра
    """
    with open(path_to_file, 'r') as file:
        res = []
        file.readline()
        for line in file:
            res.append(tuple(map(int, line.strip('\n').split())))
        return res
def components(lst):
    vertice_component = {}
    components = {}
    for tpl in lst:
        if tpl[0] not in vertice_component and tpl[1] not in vertice_component:
            vertice_component[tpl[0]] = tpl[0]
            vertice_component[tpl[1]] = tpl[0]
            components[tpl[0]] = {tpl[0], tpl[1]}
        elif tpl[0] in vertice_component and tpl[1] not in vertice_component:
            vertice_component[tpl[1]] = vertice_component[tpl[0]]
            components[vertice_component[tpl[0]]].add(tpl[1])
        elif tpl[1] in vertice_component and tpl[0] not in vertice_component:
            vertice_component[tpl[0]] = vertice_component[tpl[1]]
            components[vertice_component[tpl[1]]].add(tpl[0])
        elif tpl[1] in vertice_component and tpl[0] in vertice_component and \
                vertice_component[tpl[1]] != vertice_component[tpl[0]]:
                temp_comp_num = vertice_component[tpl[1]]
                components[vertice_component[tpl[0]]] = components[vertice_component[tpl[0]]].\
                    union(components[vertice_component[tpl[1]]])
                for verticle in components[vertice_component[tpl[1]]]:
                    vertice_component[verticle] = vertice_component[tpl[0]]
                del components[temp_comp_num]
    return components


comp = components(read_data1('graph_100000_4998622_1.csv'))

least_verticles_lst = []
for key in comp:
    least_verticles_lst.append(min(comp[key]))

print("LENGTH: " + str(len(comp)))
stop = timeit.default_timer()
execution_time = stop - start

print("Program Executed in "+str(execution_time))

import timeit

"""
Library for the work with graphs

Authors: DM-7 
Sofia Solodka, Oleksandr Kushnir, Dmytrii Mykytenko, Polyova Anna, Shchur Oleksandr
"""


def components(path):

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

    lst = read_data1(path)
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


def components_output_wrapper(path):
    start = timeit.default_timer()

    comp = components(path)

    least_verticles_lst = []
    for key in comp:
        least_verticles_lst.append(min(comp[key]))

    # print(comp)
    # print("LENGTH: " + str(len(comp)))
    print(least_verticles_lst)

    stop = timeit.default_timer()
    execution_time = stop - start

    print("Program Executed in " + str(execution_time))

    return least_verticles_lst


def strong_connectivity(path):

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
        Each vertex has its 'own' vertexes - it is a value of returned
        dict, when a key as verticle is passed.
        """
        res_dict = dict()
        for tpl in res:
            res_dict[int(tpl[0])] = res_dict.get(int(tpl[0]), []) + [int(tpl[1])]
            all_verticles.add(int(tpl[0]))
            all_verticles.add(int(tpl[1]))
        return res_dict

    all_verticles = set()
    arcs = creating_dict(read_data1(path))
    low_links = {num: num for num in all_verticles}
    id = {}
    components = {}
    count = 1
    visited = set()

    for verticle in all_verticles:
        if verticle not in visited:
            stack = [verticle]
            visited = {verticle}
            active = {verticle}

            while stack:
                if stack[-1] not in id:
                    id[stack[-1]] = count
                    count+=1
                    low_links[stack[-1]] = id[stack[-1]]

                visited.add(stack[-1])
                active.add(stack[-1])
                to_remove_from_active = set()
                check_visits = True

                if stack[-1] in arcs:
                    for adjacent_vertex in arcs[stack[-1]]:
                        if adjacent_vertex not in visited and adjacent_vertex not in active:
                            stack.append(adjacent_vertex)
                            check_visits = False

                if check_visits:
                    if stack[-1] in arcs:
                        m = [low_links[adjacent_vertex] for adjacent_vertex in arcs[stack[-1]] if adjacent_vertex in active]
                        m.append(low_links[stack[-1]])
                        low_links[stack[-1]] = min(m)

                    if low_links[stack[-1]] == id[stack[-1]]:
                        components[low_links[stack[-1]]] = set()
                        for vertex in active:
                            if low_links[vertex] == low_links[stack[-1]]:
                                components[low_links[stack[-1]]].add(vertex)
                                to_remove_from_active.add(vertex)
                        for vertex in to_remove_from_active:
                            active.remove(vertex)

                    stack.pop()

    return components


def strong_connectivity_output_wrapper(path):
    start = timeit.default_timer()

    comp = strong_connectivity(path)

    least_verticles_lst = []
    
    for key in comp:
        least_verticles_lst.append(min(comp[key]))

    # print(comp)
    # print("LENGTH: " + str(len(comp)))
    print(least_verticles_lst)

    stop = timeit.default_timer()
    execution_time = stop - start

    print("Program Executed in " + str(execution_time))

    return least_verticles_lst

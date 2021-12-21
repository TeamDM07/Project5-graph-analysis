"""
Library for the work with graphs
Authors: DM-7
Sofia Solodka, Oleksandr Kushnir, Dmytro Mykytenko, Polyova Anna, Shchur Oleksandr
"""
from timeit import default_timer
import logging
import networkx as nx  # comment if necessary
import sys
import csv

sys.setrecursionlimit(100000)  # just in case

logging.basicConfig(
    format="%(asctime)s  [%(levelname)s]  -  %(name)s  -  %(message)s",
    level=logging.ERROR,
)
logger = logging.getLogger()


def read_data(path: str, return_type: str, unoriented=True, get_vertices=False):
    logger.debug(f"Called {read_data.__name__}, path: {path}")
    try:
        with open(path, "r") as file:
            file.readline()
            logger.debug(f"type: {return_type}")
            if return_type == "tuple":
                res = []
                for line in file.read().splitlines():
                    res.append(tuple(map(int, line.split())))
            elif return_type == "dict":
                res = {}
                vertices = set()
                data = file.read().strip("\n").split()
                for i in range(0, len(data) - 1, 2):
                    node1 = int(data[i])
                    node2 = int(data[i + 1])
                    if get_vertices:
                        vertices.add(node1)
                        vertices.add(node2)
                    if node1 in res:
                        pass
                    else:
                        res[node1] = []
                    res[node1].append(node2)
                    if unoriented:
                        if node2 in res:
                            pass
                        else:
                            res[node2] = []
                        res[node2].append(node1)
                if get_vertices:
                    return res, vertices
            else:
                raise ValueError(
                    "Wrong selected type of return data. Only tuple list and dict are implemented."
                )
            return res
    except FileNotFoundError as not_found_e:
        logger.exception(f"Caught exception at {read_data.__name__}")
    except ValueError as val_e:
        logger.exception(f"Caught exception at {read_data.__name__}")


def write_csv(graph, path):
    try:
        with open(path, 'w') as file:
            for i in graph:
                file.write(str(i[0]) + " " + str(i[1]))
                file.write("\n")
    except IOError as io_e:
        logger.exception(f"Caught exception at {read_data.__name__}")


def connectivity(path):
    """
    Finds all components of the given undirected graph
    """

    lst = read_data(path, "tuple")
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
        elif (
            tpl[1] in vertice_component
            and tpl[0] in vertice_component
            and vertice_component[tpl[1]] != vertice_component[tpl[0]]
        ):
            temp_comp_num = vertice_component[tpl[1]]
            components[vertice_component[tpl[0]]] = components[
                vertice_component[tpl[0]]
            ].union(components[vertice_component[tpl[1]]])
            for verticle in components[vertice_component[tpl[1]]]:
                vertice_component[verticle] = vertice_component[tpl[0]]
            del components[temp_comp_num]

    return components


def connectivity_output_wrapper(path):
    """
    Function gets output of connectivity function and returns list of all components(each component is characterized by
    the least vertex in that component)
    """
    start = default_timer()

    comp = connectivity(path)

    least_verticles_lst = []
    for key in comp:
        least_verticles_lst.append(min(comp[key]))

    # print(comp)
    # print("LENGTH: " + str(len(comp)))
    # print(least_verticles_lst)

    stop = default_timer()
    execution_time = stop - start

    # print("Program Executed in " + str(execution_time))

    return least_verticles_lst


def strong_connectivity(path):
    """
    Finds all strongly connected components of the given directed graph
    """

    arcs, all_verticles = read_data(path, "dict", unoriented=False, get_vertices=True)
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
                    count += 1
                    low_links[stack[-1]] = id[stack[-1]]

                visited.add(stack[-1])
                active.add(stack[-1])
                to_remove_from_active = set()
                check_visits = True

                if stack[-1] in arcs:
                    for adjacent_vertex in arcs[stack[-1]]:
                        if (
                            adjacent_vertex not in visited
                            and adjacent_vertex not in active
                        ):
                            stack.append(adjacent_vertex)
                            check_visits = False

                if check_visits:
                    if stack[-1] in arcs:
                        m = [
                            low_links[adjacent_vertex]
                            for adjacent_vertex in arcs[stack[-1]]
                            if adjacent_vertex in active
                        ]
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
    """
    Function gets output of strong_connectivity function and returns list of all strong connectivity components
    (each component is characterized by the least vertex in that component)
    """
    start = default_timer()

    comp = strong_connectivity(path)

    least_verticles_lst = []

    for key in comp:
        least_verticles_lst.append(min(comp[key]))

    # print(comp)
    # print("LENGTH: " + str(len(comp)))
    # print(least_verticles_lst)

    stop = default_timer()
    execution_time = stop - start

    # print("Program Executed in " + str(execution_time))

    return least_verticles_lst


def articulation_points(path: str):
    data = read_data(path, "dict")
    root = list(data.keys())[0]
    used = []
    timer = 0
    time_in = {}
    fup = {}
    connection_p = set()

    def DFS(v, timer, p=None):
        used.append(v)
        time_in[v] = timer + 1
        fup[v] = timer + 1
        timer += 1
        children = 0
        for to in data[v]:
            if to == p:
                continue
            if to in used:
                fup[v] = min(fup.get(v), time_in[to])
            else:
                DFS(to, timer, v)
                fup[v] = min(fup[v], fup[to])
                if fup[to] >= time_in[v] and p:
                    connection_p.add(v)
                children += 1
        if not p and children > 1:
            connection_p.add(v)

    for vert in data:
        DFS(vert, timer)
    return connection_p


def bridge_finder(graph):
    size = len(graph)
    # print (size)
    index_tracker = [0] * size
    low_value = [0] * size
    visits_tracker = [False] * size
    bridges = []

    def depth_search(i, prev_node_id, bridges, appropriated_num=1):
        visits_tracker[i] = True
        low_value[i] = appropriated_num
        index_tracker[i] = appropriated_num
        appropriated_num += 1
        for nex in graph[i]:
            if nex == prev_node_id:
                continue
            if not visits_tracker[nex]:
                depth_search(nex, i, bridges, appropriated_num)
                low_value[i] = min(low_value[i], low_value[nex])
                # print(index_tracker[i], low_value[nex])
                if index_tracker[i] < low_value[nex]:
                    bridges.append([i, nex])
                    # print(bridges)
            else:
                low_value[i] = min(low_value[i], index_tracker[nex])

    for j in range(len(graph)):
        if not visits_tracker[j]:
            depth_search(j, -1, bridges)
    # print(bridges)
    return bridges


def biection(components, graph):
    for component in components:
        component = sorted([component] + list(components[component]))
        special_format = [[i] for i in range(len(component))]
        for node in component:
            node_index = component.index(node)
            for linked_node in graph[node]:
                next_node_index = component.index(linked_node)
                special_format[node_index].append(next_node_index)
        yield sorted(special_format), component


def executing_func_for_bridges(path):
    graph = read_data(path, "dict")
    components = connectivity(path)
    # print(graph, '\n\n', components)
    all_bridges = []
    for subgraph, component in biection(components, graph):
        # print(subgraph)
        bridges = bridge_finder(subgraph)
        for edge in bridges:
            all_bridges.append([component[edge[0]], component[edge[1]]])
        # all_bridges.append(bridges)
    return all_bridges


def _tests(line: str):
    """
    Tests for module
    """
    print(f"data {line}")
    start = default_timer()
    df = read_data(line, "tuple")
    end = default_timer() - start
    print(f"read in {end:.5f}")
    graph = nx.Graph(df)
    graph1 = nx.DiGraph(df)

    print("Connected component")
    start = default_timer()
    temp = connectivity(line)
    end = default_timer() - start
    print(f"module implementation:{end:.5f}")
    start = default_timer()
    temp2 = nx.number_connected_components(graph)
    end = default_timer() - start
    print(f"networkx implementation:{end:.5f}")
    print(f"Valid: {len(temp) == temp2}")

    print("Strong connectivity")
    start = default_timer()
    temp = strong_connectivity(line)
    end = default_timer() - start
    print(f"module implementation:{end:.5f}")
    start = default_timer()
    temp2 = nx.number_strongly_connected_components(graph1)
    end = default_timer() - start
    print(f"networkx implementation:{end:.5f}")
    print(f"Valid: {len(temp) == temp2}")

    print("Articulation points")
    start = default_timer()
    temp = list(articulation_points(line))
    end = default_timer() - start
    print(f"module implementation:{end:.5f}")
    start = default_timer()
    temp2 = list(nx.articulation_points(graph))
    end = default_timer() - start
    print(f"networkx implementation:{end:.5f}")
    print(f"Valid: {len(temp) == len(temp2)}")

    print("Bridges")
    start = default_timer()
    temp = list(executing_func_for_bridges(line))
    end = default_timer() - start
    print(f"module implementation:{end:.5f}")
    start = default_timer()
    temp2 = list(nx.bridges(graph))
    end = default_timer() - start
    print(f"networkx implementation:{end:.5f}")
    print(f"Valid: {len(temp) == len(temp2)}")

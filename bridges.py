def bridge_finder(graph):
    size = len(graph)
    print (size)
    index_tracker = [0]*size
    low_value = [0]*size
    visits_tracker = [False]*size
    bridges = []

    def depth_search(i, prev_node_id, bridges, appropriated_num = 1):
        visits_tracker[i] = True
        low_value[i] = appropriated_num
        index_tracker[i] = appropriated_num
        appropriated_num+=1
        for next in graph[i]:
            if next == prev_node_id:
                continue
            if not visits_tracker[next]:
                depth_search(next, i, bridges, appropriated_num)
                low_value[i] = min(low_value[i], low_value[next])
                if index_tracker[i]<low_value[next]:
                    bridges.append([i, next])
            else:
                low_value[i] = min(low_value[i], index_tracker[next])

    for j in range(len(graph)):
        if not visits_tracker[j]:
            depth_search(j, -1, bridges)
    return bridges

def biection(components, graph):
    for component in components:
        component=sorted([component]+list(components[component]))
        special_format = [[i] for i in range(len(component))]
        for node in component:
            node_index=component.index(node)
            for linked_node in graph[node]:
                next_node_index=component.index(linked_node)
                special_format[node_index].append(next_node_index)
                special_format[next_node_index].append(node_index)
        yield special_format, component

def executing_func(components, graph):
    all_bridges=[]
    for subgraph, component in biection(components, graph):
        bridges=bridge_finder(subgraph)
        for i, edge in enumerate[bridges]:
            bridges[i]=[component[edge[0]], component[edge[1]]]
        all_bridges.append(bridges)
    return all_bridges



# print(bridge_finder(sorted([[0,1,2,0,2,3,2,2],[1,2,1,0],[3,5,4],[2,1,0,4,0,0],[4,3,2],[5,3]])))

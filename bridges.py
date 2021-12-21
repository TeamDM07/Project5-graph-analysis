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

def biection(component):
    pass

print(bridge_finder(sorted([[0,1,2],[1,2,0],[3,5,4],[2,1,0,4],[4,3,2],[5,3]])))

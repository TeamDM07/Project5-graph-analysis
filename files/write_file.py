import csv

def write_csv(graph,path):
    with open(path, 'w') as f:
        for i in graph:
            f.write(str(i[0]) + " " + str(i[1]))
            f.write("\n")

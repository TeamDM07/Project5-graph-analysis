import pandas as pd
import logging
from timeit import default_timer

logging.basicConfig(format='%(asctime)s  [%(levelname)s]  -  %(name)s  -  %(message)s', level=logging.DEBUG)
logger = logging.getLogger('analysis.py')


def return_data(path):
    import os
    return [f'{path}\\{x}' for x in os.listdir(path)]


def read_data(path: str, get_type: str):
    logger.debug(f'Called {read_data.__name__}, path: {path}')
    try:
        with open(path, 'r') as file:
            # pandas
            if get_type == 'pandas':
                return pd.read_csv(names=['node', 'connection'], delim_whitespace=True)
            # tuples
            elif get_type == 'tuple':
                res = []
                for line in file.read().splitlines():
                    res.append(tuple(line.split()))
            # dict
            elif get_type == 'dict':
                logger.debug(f'type: {get_type}')
                res = {}
                data = file.read().strip('\n').split()
                for i in range(0, len(data) - 1, 2):
                    node1 = int(data[i])
                    node2 = int(data[i + 1])
                    if node1 in res:
                        pass
                    else:
                        res[node1] = []
                    if node2 in res:
                        pass
                    else:
                        res[node2] = []
                    res[node1].append(node2)
                    res[node2].append(node1)
                    logger.debug(f'{node1} - {node2}')
            return res
    except FileNotFoundError as e:
        logger.exception(f'Caught exception at {read_data.__name__}')

"""
rewrite for dict and tuples


def write_data(path: str, data: pd.DataFrame):
    logger.debug(f'Called {write_data.__name__}, path: {path}, data: {data.info}')
    try:
        data.to_csv(path, sep=' ', header=False, index=False)
        logger.info('Wrote data successfully!')
    except IOError as e:
        logger.exception(f'Caught exception at {write_data.__name__}')
"""

def connection_points(data:dict):
    root = list(data.keys())[0]
    used = []
    timer = 0
    time_in = {}
    fup = {}
    connection_p = set()
    def DFS(v, timer, p = None):
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
                fup[v] = min (fup[v], fup[to])
                if fup[to] >= time_in[v] and p:
                    connection_p.add(v)
                children += 1
        if not p and children > 1:
            connection_p.add(v)
        #logger.debug(connection_p)
    for vert in data:
        DFS(vert, timer)
    logger.debug('finished')
    return connection_p



def main():
    for i, line in enumerate(return_data('data')):
        print(f'data {i}')
        start = default_timer()
        df = read_data(line, 'dict')
        print(connection_points(df))
        # logger.debug(df)
        # write_data(line, df)
        end = default_timer() - start
        print(f'finished in {end}')
        input()


if __name__ == '__main__':
    main()

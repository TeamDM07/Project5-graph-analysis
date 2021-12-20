import pandas as pd
import logging
from timeit import default_timer
from itertools import islice

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
                    temp = int(data[i])
                    if temp in res:
                        pass
                    else:
                        res[temp] = []
                    res[temp].append(int(data[i + 1]))
                    logger.debug(f'{temp} - {data[i + 1]}')
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



"""
    dont work
"""
def connected_comp(data):
    overall_comp = []
    used = []
    comp = []
    """
    void dfs (int v) {
	    used[v] = true;
	    comp.push_back (v);
	    for (size_t i=0; i<g[v].size(); ++i) {
		    int to = g[v][i];
		    if (!used[to])
			    dfs (to);
    """
    def dfs(v):
        used.append(v)
        comp.append(v)
        for elem in data[v]:
            if elem in used:
                pass
            else:
                dfs(elem)
    for vertice in data:
        if vertice not in used:
            comp = []
            dfs(vertice)
            overall_comp.append(min(comp))
            logger.debug(min(overall_comp))
    logger.debug(comp)
    return min(comp)


def strong_component(data):
    pass


def main():
    for i, line in enumerate(return_data('data')[2:]):
        print(f'data {i}')
        start = default_timer()
        df = read_data(line, 'dict')
        print(connected_comp(df))
        # logger.debug(df)
        # write_data(line, df)
        end = default_timer() - start
        print(f'finished in {end}')
        input()


if __name__ == '__main__':
    main()

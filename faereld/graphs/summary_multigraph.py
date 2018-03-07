# -*- coding: utf-8 -*-

"""
faereld.graphs.summary_multigraph
---------------------------------
"""

from .. import utils
from . import SummaryGraph

# Summary MultiGraph is a graph that expects values map of the form
# { key:
#         { graph_key1: graph_value,
#           graph_key2: graph_value
#         },
#
#   key2: { graph2_key1: graph_value,
#           graph2_key2: graph_value
#         }
# }
# It will build a Summary graph for each of the graph definitions in the map
# and sequentially display them, given the column width and max width.

class SummaryMultiGraph(object):

    graph_seperator = '   '

    def __init__(self, values_map, column_width):
        self.values_map = values_map
        self.column_width = column_width
        self.max_width = utils.terminal_width()
        self.exclude_list = []
        self.key_transform_func = None
        self.sort = False
        self.reverse_sort = None
        self.header_transform_func = str

    def set_max_width(self, max_width):
        self.max_width = max_width
        return self

    def set_exclude_list(self, exclude_list):
        self.exclude_list = exclude_list
        return self

    def set_key_transform_function(self, key_transform_func):
        self.key_transform_func = key_transform_func
        return self

    def sort_graph(self, reverse=False):
        self.sort = True
        self.reverse_sort = reverse
        return self

    def set_header_transform_function(self, header_transform_func):
        self.header_transform_func = header_transform_func
        return self

    def generate(self):

        graph_map = {}

        for k, v in self.values_map.items():
            graph = SummaryGraph(v) \
                  .set_max_width(self.column_width) \
                  .set_exclude_list(self.exclude_list) \
                  .set_key_transform_function(self.key_transform_func) \
                  .set_graph_header(self.header_transform_func(k)) \
                  .generate()
            graph_map[k] = graph

        # Calculate the number of graphs that should appear on each row
        n, r = divmod(self.max_width, self.column_width + len(self.graph_seperator))
        if r >= self.column_width:
            n += 1
        graph_keys = list(self.values_map.keys())

        combined_graphs = []

        while len(graph_keys) != 0:
            row_keys = graph_keys[:n]
            del graph_keys[:n]

            graphs = list(map(lambda x: graph_map[x], row_keys))
            zipped_graphs = list(zip(*graphs))

            for g in zipped_graphs:
                combined_graphs.append(self.graph_seperator.join(g))

            if len(graph_keys) > 0:
                combined_graphs.append('')

        return combined_graphs

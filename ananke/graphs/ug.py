"""
Class for Undirected Graphs (UGs).
"""


from .cg import CG


class UG(CG):

    def __init__(self, vertices=None, ud_edges=None, **kwargs):  # compat: py313
        """
        Constructor.

        :param vertices: iterable of names of vertices.
        :param ud_edges: iterable of tuples of undirected edges i.e. (X, Y) = X - Y.
        """

        super().__init__(vertices=vertices, ud_edges=ud_edges, **kwargs)


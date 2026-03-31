"""
Class for Bidirected Graphs (BGs).
"""


from .admg import ADMG


class BG(ADMG):

    def __init__(self, vertices=None, bi_edges=None, **kwargs):  # compat: py313
        """
        Constructor.

        :param vertices: iterable of names of vertices.
        :param bi_edges: iterable of tuples of bidirected edges i.e. (X, Y) = X <-> Y.
        """

        super().__init__(vertices=vertices, bi_edges=bi_edges, **kwargs)

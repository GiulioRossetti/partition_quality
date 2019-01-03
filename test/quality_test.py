import unittest
from networkx.algorithms import community
from pquality.PartitionQuality import pquality_summary
import networkx as nx
import pandas as pd


class QualityTestCase(unittest.TestCase):

    def test_quality_functions(self):
        g = nx.karate_club_graph()
        lp = list(community.label_propagation_communities(g))
        coms = [tuple(x) for x in lp]

        res = pquality_summary(g, coms)
        for _, v in res.items():
            self.assertIsInstance(v, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()

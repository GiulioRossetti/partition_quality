import unittest
import demon as d
from pquality.PartitionQuality import pquality_summary
import networkx as nx
import pandas as pd


class QualityTestCase(unittest.TestCase):

    def test_quality_functions(self):
        g = nx.karate_club_graph()
        D = d.Demon(graph=g, epsilon=0.3)
        coms = D.execute()
        res = pquality_summary(g, coms)
        for _, v in res.items():
            self.assertIsInstance(v, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()

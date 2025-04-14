import unittest
from assignment1 import intercept

class TestInterceptEdgeCases(unittest.TestCase):
    def test_never(self):
        roads = [(0, 1, 1, 1), (1, 0, 1, 1), (2, 1, 5, 1)]
        stations = [(0, 1), (1, 1)]
        start = 2
        friendStart = 0
        expected_output = (5, 1, [2, 1])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

    def test_gonna(self):
        roads = [(0, 1, 35, 3), (1, 0, 1, 1), (2, 0, 10, 5)]
        stations = [(0, 3), (1, 2)]
        start = 2
        friendStart = 0
        expected_output = (10, 5, [2, 0])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

    def test_give(self):
        roads = [(0, 1, 1, 2), (1, 2, 1, 3), (2, 0, 1, 5), (3, 0, 10, 10)]
        stations = [(0, 2), (1, 3), (2, 5)]
        start = 3
        friendStart = 0
        expected_output = (10, 10, [3, 0])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

    def test_you(self):
        roads = [(0, 1, 1, 1), (1, 0, 5, 2)]
        stations = [(0, 1), (1, 1)]
        start = 1
        friendStart = 0
        expected_output = (5, 2, [1, 0])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

    def test_up(self):
        roads = [(0, 1, 1, 2), (1, 2, 1, 3), (2, 0, 1, 5), (3, 2, 10, 5), (3, 0, 5, 1)]
        stations = [(0, 2), (1, 3), (2, 5)]
        start = 3
        friendStart = 0
        expected_output = (10, 5, [3, 2])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

    def test_never_(self):
        roads = [(0, 1, 1, 1), (1, 2, 1, 2), (2, 0, 1, 3), (3, 2, 10, 3), (3, 0, 5, 1)]
        stations = [(0, 1), (1, 2), (2, 3)]
        start = 3
        friendStart = 0
        expected_output = (10, 3, [3, 2])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

    def test_gonna_(self):
        roads = [(3, 2, 5, 2), (0, 1, 1, 1), (1, 2, 1, 1), (2, 0, 1, 1), (3, 0, 10, 1)]
        stations = [(0, 1), (1, 1), (2, 1)]
        start = 3
        friendStart = 0
        expected_output = (5, 2, [3, 2])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

class TestAdditionalInterceptions(unittest.TestCase):
    def test_let_(self):
        roads = [(0, 1, 3, 1), (1, 2, 3, 1), (2, 0, 3, 1), (0, 3, 10, 5), (2, 4, 2, 1), (3, 4, 1, 1), (4, 0, 5, 2)]
        stations = [(3, 2), (4, 2)]
        start = 0
        friendStart = 3
        expected_output = (11, 6, [0, 3, 4])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

    def test_you_(self):
        roads = [(0, 1, 1, 1), (1, 2, 1, 1), (2, 0, 5, 2), (1, 0, 2, 1), (2, 1, 2, 1)]
        stations = [(1, 2), (2, 3)]
        start = 0
        friendStart = 1
        expected_output = (2, 2, [0, 1, 2])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

    def test_down_(self):
        roads = [(0, 1, 3, 2), (1, 2, 3, 2), (2, 3, 3, 2), (0, 4, 6, 3), (4, 5, 1, 1), (5, 3, 1, 1), (3, 0, 10, 2)]
        stations = [(3, 2), (5, 1)]
        start = 0
        friendStart = 5
        expected_output = (26, 12, [0, 1, 2, 3, 0, 4, 5])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

    def test_never_(self):
        roads = [(0, 1, 10, 2), (0, 2, 100, 1), (1, 2, 5, 1), (2, 3, 10, 2), (1, 3, 50, 5), (3, 4, 2, 1), (2, 4, 30, 2), (4, 0, 5, 2)]
        stations = [(3, 2), (4, 2)]
        start = 0
        friendStart = 3
        expected_output = (27, 6, [0, 1, 2, 3, 4])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

    def test_gonna_(self):
        roads = [(0, 1, 2, 1), (1, 2, 2, 1), (2, 3, 2, 1), (3, 1, 1, 1), (3, 4, 2, 1), (4, 5, 2, 1), (5, 0, 10, 3), (2, 5, 5, 2)]
        stations = [(3, 2), (5, 1)]
        start = 0
        friendStart = 3
        expected_output = (6, 3, [0, 1, 2, 3])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

    def test_tell_(self):
        roads = [(0, 1, 5, 2), (1, 2, 5, 2), (2, 3, 5, 2), (3, 0, 5, 2), (3, 4, 1, 1), (4, 0, 10, 3), (1, 3, 10, 4)]
        stations = [(3, 2), (4, 3)]
        start = 0
        friendStart = 3
        expected_output = (16, 7, [0, 1, 3, 4])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()

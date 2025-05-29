import unittest
from assignment1cal import intercept

# Group 1: TestInterceptEdgeCases
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

# Group 2: TestAdditionalInterceptions
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

# Group 3: TestAdditionalInterceptCases
class TestAdditionalInterceptCases(unittest.TestCase):

    def test1(self):
        roads = []
        stations = [(0, 5), (1, 5)]
        start = 0
        friendStart = 0
        output = (0, 0, [0])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, output)

    def test2(self):
        roads = [
            (0, 1, 1, 3), (0, 2, 1, 5), (1, 3, 2, 3), (2, 3, 2, 2)
        ]
        stations = [(3, 2), (0, 2)]
        start = 0
        friendStart = 3
        result = intercept(roads, stations, start, friendStart)
        self.assertIsNone(result)

    def test3(self):
        roads = [(0, 1, 5, 5)]
        stations = [(1, 3), (0, 3)]
        start = 0
        friendStart = 1
        result = intercept(roads, stations, start, friendStart)
        self.assertIsNone(result)

    def test4(self):
        roads = [(0, 1, 2, 2), (1, 2, 2, 2), (2, 0, 2, 2)]
        stations = [(2, 3), (0, 3)]
        start = 0
        friendStart = 0
        output = (0, 0, [0])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, output)

    def test5(self):
        roads = [(0, 1, 2, 2)]
        stations = [(3, 1), (4, 1)]
        start = 0
        friendStart = 3
        result = intercept(roads, stations, start, friendStart)
        self.assertIsNone(result)

    def test6(self):
        roads = [(0, 1, 2, 2), (1, 2, 2, 2)]
        stations = [(5, 2), (6, 2)]
        start = 0
        friendStart = 5
        result = intercept(roads, stations, start, friendStart)
        self.assertIsNone(result)

    def test7(self):
        roads = [(0, 1, 2, 2)]
        stations = [(1, 5), (0, 5)]
        start = 0
        friendStart = 1
        result = intercept(roads, stations, start, friendStart)
        self.assertIsNone(result)

    def test8(self):
        roads = [(0, 1, 3, 6)]
        stations = [(1, 2), (2, 2), (0, 2)]
        start = 0
        friendStart = 1
        output = (3, 6, [0, 1])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, output)

    def test9(self):
        roads = [
            (0, 1, 2, 2), (1, 2, 3, 2), (2, 3, 1, 2), (3, 4, 2, 4), (4, 5, 1, 5),
            (0, 6, 10, 4), (6, 7, 1, 1), (7, 8, 1, 1), (8, 5, 1, 1),
            (1, 9, 5, 2), (9, 10, 2, 1), (10, 5, 2, 1),
            (2, 11, 3, 1), (11, 12, 2, 1), (12, 13, 3, 1), (13, 5, 4, 1),
            (3, 14, 2, 1), (14, 5, 2, 1), (0, 10, 20, 6), (6, 12, 15, 4)
        ]
        stations = [(5, 3), (13, 3), (10, 3), (0, 3), (1, 3)]
        start = 0
        friendStart = 5

        output = (9, 15, [0, 1, 2, 3, 4, 5])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, output)

# Group 4: TestOneOne
class TestOneOne(unittest.TestCase):

    def test_1(self):
        roads = [(0, 2, 10, 3), (1, 2, 5, 2), (2, 1, 15, 5), (2, 0, 12, 10)]
        stations = [(0, 5), (1, 5)]
        start = 2
        friendStart = 0
        expected_output = (12, 10, [2, 0])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

    def test_2(self):
        stations_input = [(i, 2) for i in range(20)]
        start_input = 20
        friendStart_input = 0
        roads_input = [(20, 2, 7, 4), (20, 18, 30, 36)] + \
                      [(i, (i+1)%20, 1, 2) for i in range(20)]
        expected_output = (7, 4, [20, 2])
        result = intercept(roads_input, stations_input, start_input, friendStart_input)
        self.assertEqual(result, expected_output)

    def test_3(self):
        stations_input = [(i, 5) for i in range(20)]
        start_input = 20
        friendStart_input = 0
        roads_input = [(20, 5, 30, 25), (20, 0, 40, 100)] + \
                      [(i, (i+1)%20, 1, 1) for i in range(20)]
        expected_output = (30, 25, [20, 5])
        result = intercept(roads_input, stations_input, start_input, friendStart_input)
        self.assertEqual(result, expected_output)

    def test_4(self):
        roads = [(0, 1, 1, 1), (1, 0, 1, 1),
                 (2, 3, 1, 1), (3, 2, 1, 1)]
        stations = [(0, 5), (1, 5)]
        start = 2
        friendStart = 0
        result = intercept(roads, stations, start, friendStart)
        self.assertIsNone(result)

    def test_5(self):
        roads = [(0, 1, 10, 3), (1, 2, 20, 10), (2, 0, 8, 4)]
        stations = [(0, 5), (1, 5), (2, 5)]
        start = 1
        friendStart = 0
        expected_output = (20, 10, [1, 2])
        result = intercept(roads, stations, start, friendStart)
        self.assertEqual(result, expected_output)

class Test(unittest.TestCase):
  def test_simple(self):
    roads = [(6,0,3,1), (6,7,4,3), (6,5,6,2), (5,7,10,5), (4,8,8,5), (5,4,8,2),
             (8,9,1,2), (7,8,1,3), (8,3,2,3), (1,10,5,4), (0,1,10,3), (10,2,7,2),
             (3,2,15,2), (9,3,2,2), (2,4,10,5)]
    stations = [(0,1), (5,1), (4,1), (3,1), (2,1), (1,1)]
    start = 6
    friendStart = 0

    self.assertEqual(intercept(roads, stations, start, friendStart), (7, 9, [6,7,8,3]))

  def test_unsolvable(self):
    roads = [(0,1,35,3), (1,2,5,2), (2,0,35,4), (0,4,10,1), (4,1,22,2),
             (1,5,65,1), (5,2,70,1), (2,3,10,1), (3,0,20,3)]
    stations = [(4,3), (5,2), (3,4)]
    start = 0
    friendStart = 4

    self.assertIsNone(intercept(roads, stations, start, friendStart))

  def test_repeated(self):
    roads = [(0,1,35,7), (1,2,5,4), (2,0,35,6), (0,4,10,5), (4,1,22,3),
             (1,5,60,4), (5,3,70,2), (3,0,10,7)]
    stations = [(4,2), (5,1), (3,4)]
    start = 0
    friendStart = 3

    self.assertEqual(intercept(roads, stations, start, friendStart), (160, 39, [0,1,2,0,1,2,0,4]))

  def test_samecost_difftime(self):
    roads = [(0,1,10,7), (0,2,10,3), (2,0,1,4), (1,0,1,7)]
    stations = [(2,4), (1,3)]
    start = 0
    friendStart = 1

    self.assertEqual(intercept(roads, stations, start, friendStart), (10, 3, [0,2]))

# Group 5: SimpleTestCases
class SimpleTestCases(unittest.TestCase):
    def test_linear_path(self):
        roads = [(0,1,5,2), (1,2,5,2), (2,3,5,2), (3,4,5,2), (1,4,30,2), (4,0,5,2)]
        stations = [(4,2), (2,2)]
        start = 0
        friend_start = 4
        expected_output = (20, 8, [0,1,2,3,4])
        self.assertEqual(intercept(roads, stations, start, friend_start), expected_output)


# Run all tests
if __name__ == '__main__':
    unittest.main()

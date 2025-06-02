import unittest
from assignment2 import crowdedCampus

class TestCrowdedCampus(unittest.TestCase):
    def check(self, n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation):
        self.assertIsInstance(allocation, list)
        self.assertEqual(len(allocation), n)
        for a in allocation:
            self.assertTrue(0 <= a < m)
        counts = [0] * m
        for a in allocation:
            counts[a] += 1
        for j, (_, min_cap, max_cap) in enumerate(proposed_classes):
            self.assertTrue(min_cap <= counts[j] <= max_cap)
        satisfied = 0
        for i, a in enumerate(allocation):
            time_slot = proposed_classes[a][0]
            if time_slot in time_preferences[i][:5]:
                satisfied += 1
        self.assertGreaterEqual(satisfied, minimum_satisfaction)

    def validate_allocation(self, n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation):
        # Check correct type and length
        self.assertIsInstance(allocation, list)
        self.assertEqual(len(allocation), n)

        # Class counts and satisfaction count
        counts = [0] * m
        satisfied = 0

        for i in range(n):
            class_id = allocation[i]
            self.assertTrue(0 <= class_id < m)
            counts[class_id] += 1
            time_slot = proposed_classes[class_id][0]
            if time_slot in time_preferences[i][:5]:
                satisfied += 1

        # Check class capacity constraints
        for j in range(m):
            min_cap, max_cap = proposed_classes[j][1], proposed_classes[j][2]
            self.assertGreaterEqual(counts[j], min_cap)
            self.assertLessEqual(counts[j], max_cap)

        # Check minimum satisfaction
        self.assertGreaterEqual(satisfied, minimum_satisfaction)

    def test1(self):
        n = 10
        m = 2
        time_preferences = [[5] + [t for t in range(20) if t != 5] for _ in range(n)]
        proposed_classes = [[5, 1, 6], [5, 1, 6]]
        minimum_satisfaction = 10
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, minimum_satisfaction)
        self.check(n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation)

    def test2(self):
        import random
        random.seed(1337)
        n = 50
        m = 5
        time_preferences = [random.sample(list(range(20)), 20) for _ in range(n)]
        proposed_classes = []
        for j in range(m):
            slot = j * 4
            min_cap = 5
            max_cap = 15
            proposed_classes.append([slot, min_cap, max_cap])
        minimum_satisfaction = 20
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, minimum_satisfaction)
        if allocation is not None:
            self.check(n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation)

    def test3(self):
        n = 5
        m = 2
        time_preferences = [
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20))
        ]
        proposed_classes = [[19, 2, 3], [19, 2, 3]]
        minimum_satisfaction = 1
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, minimum_satisfaction)
        self.assertIsNone(allocation)
        
    def test4(self):
        n = 10
        m = 2
        time_preferences = [list(range(20)) for _ in range(n)]
        proposed_classes = [[0, 1, 4], [1, 1, 4]]
        minimum_satisfaction = 0
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, minimum_satisfaction)
        self.assertIsNone(allocation)

    def test5(self):
        n = 10
        m = 2
        time_preferences = [list(range(20)) for _ in range(n)]
        proposed_classes = [[0, 5, 5], [1, 5, 5]]
        minimum_satisfaction = 0
        allocation = crowdedCampus(n, m, time_preferences, proposed_classes, minimum_satisfaction)
        self.check(n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation)

    def test6(self):
        n = 1
        m = 1
        prefs = [list(range(20))]
        classes = [[0, 1, 1]]
        min_sat = 1
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test7(self):
        n = 2
        m = 1
        prefs = [list(range(20))]*2
        classes = [[0, 2, 2]]
        min_sat = 2
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test8(self):
        n = 2
        m = 2
        prefs = [[1, 0] + list(range(2, 20)), list(range(20))]
        classes = [[1, 1, 1], [0, 1, 1]]
        min_sat = 2
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test9(self):
        n = 3
        m = 2
        prefs = [[0, 1] + list(range(2, 20)),
            [1, 0] + list(range(2, 20)),
            [0, 1] + list(range(2, 20))]
        classes = [[0, 2, 2], [1, 1, 2]]
        min_sat = 2
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)
        
    def test10(self):
        n = 4
        m = 2
        prefs = [[0, 1] + list(range(2, 20)) for _ in range(2)] + [[1, 0] + list(range(2, 20)) for _ in range(2)]
        classes = [[0, 2, 2], [1, 2, 2]]
        min_sat = 4
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test11(self):
        n = 4
        m = 2
        prefs = [list(range(20)) for _ in range(4)]
        classes = [[0, 2, 2], [0, 2, 2]]
        min_sat = 4
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)
        
    def test12_bfs_order(self):
        n = 2
        m = 2
        prefs = [[0,1,2,4,5,3] + list(range(6, 20)), [0,1,2,3,5,4] + list(range(8, 20)) + [0]]
        classes = [[0, 1, 1], [4, 1, 1]]
        min_sat = 2
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)
        
    def test13_min_unfilled(self):
        n = 5
        m = 2
        prefs = [list(range(0, 20))] * 5
        classes = [[0, 3, 10], [4, 2, 10]]
        min_sat = 3
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)
        
    def test14_no_satisfaction_allocation(self):
        n = 1
        m = 1
        prefs = [list(range(20))]
        classes = [[21, 1, 1]]
        min_sat = 0
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)
        
    def test15_one_unsatisfied_allocation(self):
        n = 2
        m = 2
        prefs = [list(range(20))] * 2
        classes = [[21, 1, 1], [0, 1, 1]]
        min_sat = 1
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)


if __name__ == "__main__":
    unittest.main()
    
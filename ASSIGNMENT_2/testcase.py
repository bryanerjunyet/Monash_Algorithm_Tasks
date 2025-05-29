import unittest
from assignment25 import crowdedCampus
# test initial commit
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

if __name__ == "__main__":
    unittest.main()
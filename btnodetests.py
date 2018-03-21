import unittest
from btnode import *
from behaviortree import *

class SelectorTests(unittest.TestCase):
    def setUp(self):
        self.tree = None
        self.bt = TestBehaviorTree()

    def test_selector_both_true(self):
        self.tree = [(Selector, 1), (TestNode, 2), (TestNode, 4)]
        self.bt.buildTree(self.tree)
        self.bt.start()
        go_on = True
        iterations = 0

        while go_on and iterations < 100:
            iterations += 1
            result = self.bt.update(0)
            if result is not None:
                go_on = False
        
        self.assertTrue(result)

    def test_selector_left_true(self):
        self.tree = [(Selector, 1), (TestNode, 2), (TestNode, 3)]
        self.bt.buildTree(self.tree)
        self.bt.start()
        go_on = True
        iterations = 0

        while go_on and iterations < 100:
            iterations += 1
            result = self.bt.update(0)
            if result is not None:
                go_on = False
        self.assertTrue(result)

    def test_selector_right_true(self):
        self.tree = [(Selector, 1), (TestNode, 3), (TestNode, 4)]
        self.bt.buildTree(self.tree)
        self.bt.start()
        go_on = True
        iterations = 0

        while go_on and iterations < 100:
            iterations += 1
            result = self.bt.update(0)
            if result is not None:
                go_on = False
        self.assertTrue(result)

    def test_selector_both_false(self):
        self.tree = [(Selector, 1), (TestNode, 3), (TestNode, 5)]
        self.bt.buildTree(self.tree)
        self.bt.start()
        go_on = True
        iterations = 0

        while go_on and iterations < 100:
            iterations += 1
            result = self.bt.update(0)
            if result is not None:
                go_on = False
        self.assertFalse(result)

class SequenceTests(unittest.TestCase):
    def setUp(self):
        self.tree = None
        self.bt = TestBehaviorTree()

    def test_sequence_both_true(self):
        self.tree = [(Sequence, 1), (TestNode, 2), (TestNode, 4)]
        self.bt.buildTree(self.tree)
        self.bt.start()
        go_on = True
        iterations = 0

        while go_on and iterations < 100:
            iterations += 1
            result = self.bt.update(0)
            if result is not None:
                go_on = False
        
        self.assertTrue(result)

    def test_sequence_left_true(self):
        self.tree = [(Sequence, 1), (TestNode, 2), (TestNode, 3)]
        self.bt.buildTree(self.tree)
        self.bt.start()
        go_on = True
        iterations = 0

        while go_on and iterations < 100:
            iterations += 1
            result = self.bt.update(0)
            if result is not None:
                go_on = False
        self.assertFalse(result)

    def test_sequence_right_true(self):
        self.tree = [(Sequence, 1), (TestNode, 3), (TestNode, 4)]
        self.bt.buildTree(self.tree)
        self.bt.start()
        go_on = True
        iterations = 0

        while go_on and iterations < 100:
            iterations += 1
            result = self.bt.update(0)
            if result is not None:
                go_on = False
        self.assertFalse(result)

    def test_sequence_both_false(self):
        self.tree = [(Sequence, 1), (TestNode, 3), (TestNode, 5)]
        self.bt.buildTree(self.tree)
        self.bt.start()
        go_on = True
        iterations = 0

        while go_on and iterations < 100:
            iterations += 1
            result = self.bt.update(0)
            if result is not None:
                go_on = False
        self.assertFalse(result)



if __name__ == "__main__":
    selector_tests = unittest.TestLoader().loadTestsFromTestCase(SelectorTests)
    unittest.TextTestRunner(verbosity=1).run(selector_tests)
    sequence_tests = unittest.TestLoader().loadTestsFromTestCase(SequenceTests)
    unittest.TextTestRunner(verbosity=1).run(sequence_tests)
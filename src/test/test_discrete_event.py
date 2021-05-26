import unittest

from discrete_event import *


class DiscreteEventTest(unittest.TestCase):
    def test_logic_not(self):
        m = DiscreteEvent("logic_not")
        m.input_port("A", latency=1)
        m.output_port("B", latency=1)
        n = m.add_node("not", lambda a: not a if isinstance(a, bool) else None)
        n.input("A", latency=1)
        n.output("B", latency=1)
        m.execute(
            source_event("A", True, 0),
            source_event("A", False, 5),
        )
        self.assertEqual(m.state_history, [
            (0, {'A': None}),
            (2, {'A': True}),
            (4, {'A': True, 'B': False}),
            (7, {'A': False, 'B': False}),
            (9, {'A': False, 'B': True}),
        ])
        self.assertListEqual(m.event_history, [
            event(clock=2, node=n, var='A', val=True),
            event(clock=4, node=None, var='B', val=False),
            event(clock=7, node=n, var='A', val=False),
            event(clock=9, node=None, var='B', val=True),
        ])


class NodeTest(unittest.TestCase):
    def test_logic_not(self):
        n = Node("not", lambda a: not a if isinstance(a, bool) else None)
        n.input("A", 1)
        n.output("B", 1)
        test_data = [
            (False, True),
            (False, True),
        ]
        for a, b in test_data:
            self.assertEqual(n.activate({"A": a}), [source_event("B", b, 1)])


if __name__ == '__main__':
    unittest.main()
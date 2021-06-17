import logging
from typing import Tuple, Union
from common import arg_callable, arg_type

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

from collections import OrderedDict, namedtuple
import copy

event = namedtuple("event", "clock node var val")
source_event = namedtuple("source_event", "var val latency")


class Node(object):
    @arg_type(1, str)
    @arg_callable(2)
    def __init__(self, name: str, function):
        self.function = function
        self.name = name
        self.inputs: OrderedDict = OrderedDict()
        self.outputs: OrderedDict = OrderedDict()

    def __repr__(self):
        return "{} inputs: {} outputs: {}".format(self.name, self.inputs, self.outputs)

    @arg_type(1, str)
    def input(self, name: str, latency: int = 1) -> None:
        assert name not in self.inputs
        self.inputs[name] = latency

    @arg_type(1, str)
    def output(self, name: str, latency: int = 1) -> None:
        assert name not in self.outputs
        self.outputs[name] = latency

    @arg_type(1, dict)
    def activate(self, state: dict) -> list:
        args = []

        for v in self.inputs:
            if state.get(v, None) is not None:
                args.append(state.get(v, None))
        if not args:
            args.append(None)
        res = self.function(*args)
        output_events = []
        if res is not None:
            if not isinstance(res, tuple):
                res_tuple = (res,)
                for i in range(len(self.outputs) - 1):
                    res_tuple = res_tuple + (res,) # type: ignore

            for var, val in zip(self.outputs, res_tuple):
                latency = self.outputs[var]
                output_events.append(
                    source_event(var, val, latency)
                )
        return output_events


class DiscreteEvent(object):
    @arg_type(1, str)
    def __init__(self, name: str = "anonymous"):
        self.name = name
        self.inputs: OrderedDict = OrderedDict()
        self.outputs: OrderedDict = OrderedDict()
        self.nodes: list = []
        self.state_history: list = []
        self.event_history: list = []

    @arg_type(1, str)
    def input_port(self, name: str, latency: int = 1) -> None:
        self.inputs[name] = latency

    @arg_type(1, str)
    def output_port(self, name: str, latency: int = 1) -> None:
        self.outputs[name] = latency

    @arg_type(1, str)
    def add_node(self, name: str, function) -> Node:
        node = Node(name, function)
        self.nodes.append(node)
        return node

    @arg_type(2, int)
    def _source_events2events(self, source_events: Union[list, tuple], clock: int) -> list:
        logging.info('_source_events2events. clock: {}'.format(clock))
        events = []
        for se in source_events:
            source_latency = clock + se.latency + self.inputs.get(se.var, 0)
            if se.var in self.outputs:
                target_latency = self.outputs[se.var]
                events.append(event(
                    clock=source_latency + target_latency,
                    node=None,
                    var=se.var,
                    val=se.val))
                logging.info('_source_events2events. event: {}'.format(event(clock=source_latency + target_latency,
                                                                             node=None, var=se.var, val=se.val)))
            for node in self.nodes:
                if se.var in node.inputs:
                    target_latency = node.inputs[se.var]
                    events.append(event(
                        clock=clock + source_latency + target_latency,
                        node=node,
                        var=se.var,
                        val=se.val))
                    logging.info(
                        '_source_events2events. event: {}'.format(event(clock=clock + source_latency + target_latency,
                                                                        node=node, var=se.var, val=se.val)))
        return events

    @arg_type(1, list)
    def _pop_next_event(self, events: list) -> Tuple[event, list]:
        assert len(events) > 0
        events = sorted(events, key=lambda e: e.clock)
        event = events.pop(0)
        logging.info('_pop_next_event. event: {}'.format(event))
        return event, events

    def _state_initialize(self) -> dict:
        env: dict = {}
        for var in self.inputs:
            env[var] = None
        return env

    def execute(self, *source_events: Union[tuple, list], limit: int = 10000) -> dict:
        events: list = []
        state = self._state_initialize()
        state_record = self._state_initialize()
        clock = 0
        self.state_history = [(clock, copy.copy(state))]
        while (len(events) > 0 or len(source_events) > 0) and limit > 0:
            limit -= 1
            new_events = self._source_events2events(source_events, clock)
            events.extend(new_events)
            if len(events) == 0: break
            event, events = self._pop_next_event(events)
            state.clear()
            state[event.var] = event.val
            clock = event.clock

            if event.node:
                source_events = event.node.activate(state)
            else:
                source_events = [] # type: ignore
            logging.info('execute. state: {}'.format(state))
            state_record.update(state)
            self.state_history.append((clock, copy.copy(state_record)))
            self.event_history.append(event)
            if 'Output' in state_record and state_record['Output'] == '': break
        if limit == 0: print("limit reached")
        return state_record

    def visualize(self) -> str:
        res = []
        res.append("digraph G {")
        res.append("  rankdir=LR;")
        for v in self.inputs:
            res.append("  {}[shape=rarrow];".format(v))
        for v in self.outputs:
            res.append("  {}[shape=rarrow];".format(v))
        for i, n in enumerate(self.nodes):
            res.append('  n_{}[label="{}"];'.format(i, n.name))
        for i, n in enumerate(self.nodes):
            for v in n.inputs:
                if v in self.inputs:
                    res.append('  {} -> n_{};'.format(v, i))
            for j, n2 in enumerate(self.nodes):
                if i == j: continue
                for v in n.inputs:
                    if v in n2.outputs:
                        res.append('  n_{} -> n_{}[label="{}"];'.format(j, i, v))
            for v in n.outputs:
                if v in self.outputs:
                    res.append('  n_{} -> {};'.format(i, v))
        res.append("}")
        return "\n".join(res)

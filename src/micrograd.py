# import math
# import numpy as np
# import matplotlib.pyplot as plt
from graphviz import Digraph

class Value:
    def __init__(self, value, _children=(), _op='', label=''):
        self.data = value
        self._prev = set(_children)
        self._op = _op
        self.label = label

    def __repr__(self):
        return f"Value(data={self.data})"

    def __add__(self, other):
        return Value(self.data + other.data, (self, other), '+')

    def __mul__(self, other):
        return Value(self.data * other.data, (self, other), '*')

# def f(x):
#     return 3*x**2 - 4*x + 5

def trace(root):
    # builds a set of all nodes and edges in the graph
    nodes, edges = set(), set()
    def build(n):
        if n not in nodes:
            nodes.add(n)
            for child in n._prev:
                edges.add((child, n))
                build(child)
    build(root)
    return nodes, edges

def draw_dot(root):
    dot = Digraph(format='svg', graph_attr={'rankdir': 'LR'}) # LR = left to right

    nodes, edges = trace(root)
    for n in nodes:
        uid = str(id(n))
        # for any value in the graph, create a rectangular ('record') node for it
        dot.node(name=uid, label="{ %s | data %.4f }" % (n.label, n.data), shape='record')
        if n._op:
            # if this value is a result of some operation, create an op node for it
            dot.node(name=uid + n._op, label=n._op)
            # and connect this node to it
            dot.edge(uid + n._op, uid)

    for n1, n2, in edges:
        # connect n1 to the op node of n2
        dot.edge(str(id(n1)), str(id(n2)) + n2._op)

    return dot

def playing_with_derivatives():
    # print("f(3.0)")
    # print(f(3.0))

    # xs = np.arange(-5, 5, 0.25)
    # print("xs")
    # print(xs)

    # ys = f(xs)
    # print("ys")
    # print(ys)

    # print("plotting")
    # plt.plot(xs, ys)
    # plt.show()

    h = 0.00000001
    # x = 2/3
    # print((f(x + h) - f(x))/h)

    a = 2.0
    b = -3.0
    c = 10.0
    d1 = a*b + c
    da2 = (a+h)*b + c
    db2 = a*(b+h) + c
    dc2 = a*b + (c+h)
    print('d1', d1)
    print('d2', da2)
    print('slope w/ respect to a', (da2 - d1)/h)
    print('slope w/ respect to b', (db2 - d1)/h)
    print('slope w/ respect to c', (dc2 - d1)/h)

if __name__ == "__main__":
    a = Value(2.0, label='a')
    b = Value(-3.0, label='b')
    c = Value(10.0, label='c')
    e = a*b
    e.label = 'e'
    d = e + c
    d.label = 'd'
    f = Value(-2.0, label='f')
    L = d * f
    L.label = 'L'

    dot = draw_dot(L)
    dot.render('graph_output', view=True)

    # pick back up at 31:04


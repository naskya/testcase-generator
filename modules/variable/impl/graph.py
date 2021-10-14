from __future__ import annotations

import queue
import random

from modules.utility.colorizer import Color, colorize
from modules.utility.exit_failure import exit_failure
from modules.utility.printer import error
from modules.variable.definition import Number, String, Variable
from modules.variable.impl.definition import number_of_trial


class union_find:
    def __init__(self, number_of_vertices: int) -> None:
        self.n = number_of_vertices
        self.parent_or_size = [-1] * number_of_vertices

    def leader(self, u: int) -> int:
        if self.parent_or_size < 0:
            return u
        else:
            self.parent_or_size[u] = self.leader(self.parent_or_size[u])

    def merge(self, u: int, v: int) -> None:
        u = self.leader(u)
        v = self.leader(v)

        if u == v:
            return

        if self.parent_or_size[u] > self.parent_or_size[v]:
            u, v = v, u

        self.parent_or_size[u] += self.parent_or_size[v]
        self.parent_or_size[v] = u

    def same(self, u: int, v: int) -> bool:
        return self.leader(u) == self.leader(v)


# directed | must be connected | must be acyclic | must not have multiple edge | must not have self loop


# * | may be disconnected | may have cycle | may have multiple edge | may have self loop
def generate_graph_00000_10000(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if (number_of_vertices == 0) and (number_of_edges != 0):
        error('Graph with {} vertices and {} edges does not exist.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    return True, [[random.randint(0, number_of_vertices - 1) + n_indexed, random.randint(0, number_of_vertices - 1) + n_indexed] for _ in range(number_of_edges)]


# * | may be disconnected | may have cycle | may have multiple edge | no self loop
def generate_graph_00001_10001(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if (number_of_vertices == 0) and (number_of_edges != 0):
        error('Graph with {} vertices and {} edges does not exist.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result: list[list[int]] = []

    for _ in range(number_of_edges):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1) + n_indexed
            v = random.randint(0, number_of_vertices - 1) + n_indexed

            if u != v:
                result.append([u, v])
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    return True, result


# undirected | may be disconnected | may have cycle | no multiple edge | may have self loop
def generate_graph_00010(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if (number_of_vertices == 0) and (number_of_edges != 0):
        error('Graph with {} vertices and {} edges does not exist.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges > (number_of_vertices * (number_of_vertices + 1) // 2):
        error('An undirected graph with {} vertices and {} edges must have a multiple edge.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result: list[list[int]] = []

    for _ in range(number_of_edges):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1) + n_indexed
            v = random.randint(0, number_of_vertices - 1) + n_indexed

            if ([u, v] not in result) and ([v, u] not in result):
                result.append([u, v])
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    return True, result


# undirected | may be disconnected | may have cycle | no multiple edge | no self loop
def generate_graph_00011(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if (number_of_vertices == 0) and (number_of_edges != 0):
        error('Graph with {} vertices and {} edges does not exist.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges > (number_of_vertices * (number_of_vertices - 1) // 2):
        error('Undirected graph with {} vertices and {} edges cannot be simple.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result: list[list[int]] = []

    for _ in range(number_of_edges):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1) + n_indexed
            v = random.randint(0, number_of_vertices - 1) + n_indexed

            if (u != v) and ([u, v] not in result) and ([v, u] not in result):
                result.append([u, v])
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    return True, result


# undirected | may be disconnected | acyclic | no multiple edge | no self loop
def generate_graph_00100_00101_00110_00111(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if (number_of_vertices == 0) and (number_of_edges != 0):
        error('Graph with {} vertices and {} edges does not exist.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_vertices <= number_of_edges:
        error('Undirected simple graph with {} vertices and {} edges cannot be acyclic.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges > (number_of_vertices * (number_of_vertices - 1) // 2):
        error('Undirected graph with {} vertices and {} edges cannot be simple.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result: list[list[int]] = []
    uf = union_find(number_of_vertices)

    for _ in range(number_of_edges):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1) + n_indexed
            v = random.randint(0, number_of_vertices - 1) + n_indexed

            if (not uf.same(u, v)) and ([u, v] not in result) and ([v, u] not in result):
                result.append([u, v])
                uf.merge(u, v)
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    return True, result


# undirected | connected | may have cycle | may have multiple edge | may have self loop
def generate_graph_01000(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if (number_of_vertices == 0) and (number_of_edges != 0):
        error('Graph with {} vertices and {} edges does not exist.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges < (number_of_vertices - 1):
        error('Graph with {} vertices and {} edges cannot be connected.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result = generate_tree(number_of_vertices, n_indexed, False)

    for _ in range(number_of_edges - number_of_vertices + 1):
        result.append([random.randint(0, number_of_vertices - 1) + n_indexed,
                      random.randint(0, number_of_vertices - 1) + n_indexed])

    return True, result


# undirected | connected | may have cycle | may have multiple edge | no self loop
def generate_graph_01001(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if (number_of_vertices == 0) and (number_of_edges != 0):
        error('Graph with {} vertices and {} edges does not exist.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges < (number_of_vertices - 1):
        error('Graph with {} vertices and {} edges cannot be connected.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result = generate_tree(number_of_vertices, n_indexed, False)

    for _ in range(number_of_edges - number_of_vertices + 1):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1) + n_indexed
            v = random.randint(0, number_of_vertices - 1) + n_indexed

            if u != v:
                result.append([u, v])
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    return True, result


# undirected | connected | may have cycle | no multiple edge | may have self loop
def generate_graph_01010(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if (number_of_vertices == 0) and (number_of_edges != 0):
        error('Graph with {} vertices and {} edges does not exist.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges < (number_of_vertices - 1):
        error('Graph with {} vertices and {} edges cannot be connected.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges > (number_of_vertices * (number_of_vertices + 1) // 2):
        error('An undirected graph with {} vertices and {} edges must have a multiple edge.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result = generate_tree(number_of_vertices, n_indexed, False)

    for _ in range(number_of_edges - number_of_vertices + 1):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1) + n_indexed
            v = random.randint(0, number_of_vertices - 1) + n_indexed

            if ([u, v] not in result) and ([v, u] not in result):
                result.append([u, v])
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    return True, result


# undirected | connected | may have cycle | no multiple edge | no self loop
def generate_graph_01011(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if (number_of_vertices == 0) and (number_of_edges != 0):
        error('Graph with {} vertices and {} edges does not exist.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges < (number_of_vertices - 1):
        error('Graph with {} vertices and {} edges cannot be connected.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges > (number_of_vertices * (number_of_vertices - 1) // 2):
        error('Undirected graph with {} vertices and {} edges cannot be simple.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result = generate_tree(number_of_vertices, n_indexed, False)

    for _ in range(number_of_edges - number_of_vertices + 1):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1) + n_indexed
            v = random.randint(0, number_of_vertices - 1) + n_indexed

            if (u != v) and ([u, v] not in result) and ([v, u] not in result):
                result.append([u, v])
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    return True, result


# undirected | connected | acyclic | may have multiple edge | no self loop
def generate_graph_01100_01101(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if (number_of_vertices == 0) and (number_of_edges != 0):
        error('Graph with {} vertices and {} edges does not exist.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges < (number_of_vertices - 1):
        error('Graph with {} vertices and {} edges cannot be connected.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges > number_of_vertices:
        error('Undirected graph with {} vertices and {} edges cannot be acyclic.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result = generate_tree(number_of_vertices, n_indexed, False)

    for _ in range(number_of_edges - number_of_vertices + 1):
        result.append(result[random.randint(0, number_of_vertices - 2)])

    return True, result


# directed | may be disconnected | may have cycle | no multiple edge | may have self loop
def generate_graph_10010(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if (number_of_vertices == 0) and (number_of_edges != 0):
        error('Graph with {} vertices and {} edges does not exist.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result: list[list[int]] = []

    for _ in range(number_of_edges):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1) + n_indexed
            v = random.randint(0, number_of_vertices - 1) + n_indexed

            if [u, v] not in result:
                result.append([u, v])
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    return True, result


# directed | may be disconnected | may have cycle | no multiple edge | no self loop
def generate_graph_10011(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if (number_of_vertices == 0) and (number_of_edges != 0):
        error('Graph with {} vertices and {} edges does not exist.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges > (number_of_vertices * (number_of_vertices - 1)):
        error('Directed graph with {} vertices and {} edges cannot be simple.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result: list[list[int]] = []

    for _ in range(number_of_edges):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1) + n_indexed
            v = random.randint(0, number_of_vertices - 1) + n_indexed

            if (u != v) and ([u, v] not in result):
                result.append([u, v])
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    return True, result


# directed | may be disconnected | acyclic | may have multiple edge | no self loop
def generate_graph_10100_10101(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if number_of_vertices == 0:
        if number_of_edges == 0:
            return True, []
        else:
            error('Graph with {} vertices and {} edges does not exist.'.format(
                colorize(Color.CODE, number_of_vertices),
                colorize(Color.CODE, number_of_edges)
            ))
            exit_failure()

    result: list[list[int]] = []

    for _ in range(number_of_edges):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1)
            v = random.randint(0, number_of_vertices - 1)

            if (u == v) or ([v, u] in result):
                continue

            is_valid = True

            bfs = queue.SimpleQueue()
            bfs.put([-1, v])

            while is_valid and (not bfs.empty()):
                prev_node, current_node = bfs.get()

                for from_node, to_node in result:
                    if from_node != current_node:
                        continue
                    elif to_node == prev_node:
                        continue
                    elif to_node == u:
                        is_valid = False
                        break

                    bfs.put([from_node, to_node])

            if is_valid:
                result.append([u, v])
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    for i in range(number_of_edges):
        result[i][0] += n_indexed
        result[i][1] += n_indexed

    return True, result


# directed | may be disconnected | acyclic | no multiple edge | no self loop
def generate_graph_10110_10111(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if number_of_vertices == 0:
        if number_of_edges == 0:
            return True, []
        else:
            error('Graph with {} vertices and {} edges does not exist.'.format(
                colorize(Color.CODE, number_of_vertices),
                colorize(Color.CODE, number_of_edges)
            ))
            exit_failure()
    elif number_of_edges > (number_of_vertices * (number_of_vertices - 1) // 2):
        error('Directed acyclic graph with {} vertices and {} edges cannot be simple.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result: list[list[int]] = []

    for _ in range(number_of_edges):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1)
            v = random.randint(0, number_of_vertices - 1)

            if (u == v) or ([u, v] in result) or ([v, u] in result):
                continue

            is_valid = True

            bfs = queue.SimpleQueue()
            bfs.put([-1, v])

            while is_valid and (not bfs.empty()):
                prev_node, current_node = bfs.get()

                for from_node, to_node in result:
                    if from_node != current_node:
                        continue
                    elif to_node == prev_node:
                        continue
                    elif to_node == u:
                        is_valid = False
                        break

                    bfs.put([from_node, to_node])

            if is_valid:
                result.append([u, v])
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    for i in range(number_of_edges):
        result[i][0] += n_indexed
        result[i][1] += n_indexed

    return True, result


# directed | connected | may have cycle | may have multiple edge | may have self loop
def generate_graph_11000(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if number_of_vertices == 0:
        if number_of_edges == 0:
            return True, []
        else:
            error('Graph with {} vertices and {} edges does not exist.'.format(
                colorize(Color.CODE, number_of_vertices),
                colorize(Color.CODE, number_of_edges)
            ))
            exit_failure()
    elif number_of_edges < (number_of_vertices - 1):
        error('Graph with {} vertices and {} edges cannot be connected.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result = generate_tree(number_of_vertices, n_indexed, True)

    for _ in range(number_of_edges - number_of_vertices + 1):
        result.append([random.randint(0, number_of_vertices - 1) + n_indexed,
                      random.randint(0, number_of_vertices - 1) + n_indexed])

    return True, result


# directed | connected | may have cycle | may have multiple edge | no self loop
def generate_graph_11001(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if number_of_vertices == 0:
        if number_of_edges == 0:
            return True, []
        else:
            error('Graph with {} vertices and {} edges does not exist.'.format(
                colorize(Color.CODE, number_of_vertices),
                colorize(Color.CODE, number_of_edges)
            ))
            exit_failure()
    elif number_of_edges < (number_of_vertices - 1):
        error('Graph with {} vertices and {} edges cannot be connected.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges > (number_of_vertices * (number_of_vertices - 1)):
        error('Directed graph with {} vertices and {} edges cannot be simple.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result = generate_tree(number_of_vertices, n_indexed, True)

    for _ in range(number_of_edges - number_of_vertices + 1):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1) + n_indexed
            v = random.randint(0, number_of_vertices - 1) + n_indexed

            if (u != v):
                result.append([u, v])
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    return True, result


# directed | connected | may have cycle | no multiple edge | may have self loop
def generate_graph_11010(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if number_of_vertices == 0:
        if number_of_edges == 0:
            return True, []
        else:
            error('Graph with {} vertices and {} edges does not exist.'.format(
                colorize(Color.CODE, number_of_vertices),
                colorize(Color.CODE, number_of_edges)
            ))
            exit_failure()
    elif number_of_edges < (number_of_vertices - 1):
        error('Graph with {} vertices and {} edges cannot be connected.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges > (number_of_vertices * number_of_vertices):
        error('A directed graph with {} vertices and {} edges must have a multiple edge.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result = generate_tree(number_of_vertices, n_indexed, True)

    for _ in range(number_of_edges - number_of_vertices + 1):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1) + n_indexed
            v = random.randint(0, number_of_vertices - 1) + n_indexed

            if [u, v] not in result:
                result.append([u, v])
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    return True, result


# directed | connected | may have cycle | no multiple edge | no self loop
def generate_graph_11011(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if number_of_vertices == 0:
        if number_of_edges == 0:
            return True, []
        else:
            error('Graph with {} vertices and {} edges does not exist.'.format(
                colorize(Color.CODE, number_of_vertices),
                colorize(Color.CODE, number_of_edges)
            ))
            exit_failure()
    elif number_of_edges < (number_of_vertices - 1):
        error('Graph with {} vertices and {} edges cannot be connected.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()
    elif number_of_edges > (number_of_vertices * (number_of_vertices - 1)):
        error('Directed graph with {} vertices and {} edges cannot be simple.'.format(
            colorize(Color.CODE, number_of_vertices),
            colorize(Color.CODE, number_of_edges)
        ))
        exit_failure()

    result = generate_tree(number_of_vertices, n_indexed, True)

    for _ in range(number_of_edges - number_of_vertices + 1):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1) + n_indexed
            v = random.randint(0, number_of_vertices - 1) + n_indexed

            if (u != v) and ([u, v] not in result):
                result.append([u, v])
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    return True, result


# directed | connected | acyclic | may have multiple edge | no self loop
def generate_graph_11100_11101(number_of_vertices: int, number_of_edges: int, n_indexed: int) -> tuple[bool, list[list[int]]]:
    if number_of_vertices == 0:
        if number_of_edges == 0:
            return True, []
        else:
            error('Graph with {} vertices and {} edges does not exist.'.format(
                colorize(Color.CODE, number_of_vertices),
                colorize(Color.CODE, number_of_edges)
            ))
            exit_failure()

    result = generate_tree(number_of_vertices, 0, True)

    for _ in range(number_of_edges - number_of_vertices + 1):
        edge_appended = False

        for _ in range(number_of_trial):
            u = random.randint(0, number_of_vertices - 1)
            v = random.randint(0, number_of_vertices - 1)

            if (u == v) or ([v, u] in result):
                continue

            is_valid = True

            bfs = queue.SimpleQueue()
            bfs.put([-1, v])

            while is_valid and (not bfs.empty()):
                prev_node, current_node = bfs.get()

                for from_node, to_node in result:
                    if from_node != current_node:
                        continue
                    elif to_node == prev_node:
                        continue
                    elif to_node == u:
                        is_valid = False
                        break

                    bfs.put([from_node, to_node])

            if is_valid:
                result.append([u, v])
                edge_appended = True
                break

        if not edge_appended:
            return False, []

    for i in range(number_of_edges):
        result[i][0] += n_indexed
        result[i][1] += n_indexed

    return True, result


def generate_binary_tree(number_of_vertices: int, n_indexed: int, is_directed: bool) -> list[list[int]]:
    random.shuffled_index = [(i + n_indexed) for i in range(number_of_vertices)]
    random.shuffle(random.shuffled_index)

    result: list[list[int]] = []

    if is_directed:
        for i in range(number_of_vertices - 1):
            result.append([random.shuffled_index[(i + 1) >> 1], random.shuffled_index[i + 1]])
    else:
        for i in range(number_of_vertices - 1):
            if random.random() < 0.5:
                result.append([random.shuffled_index[(i + 1) >> 1], random.shuffled_index[i + 1]])
            else:
                result.append([random.shuffled_index[i + 1], random.shuffled_index[(i + 1) >> 1]])

    random.shuffle(result)
    return result


def generate_star_tree(number_of_vertices: int, n_indexed: int, is_directed: bool) -> list[list[int]]:
    random.shuffled_index = [(i + n_indexed) for i in range(number_of_vertices)]
    random.shuffle(random.shuffled_index)

    result: list[list[int]] = [[random.shuffled_index[-1]] for _ in range(number_of_vertices - 1)]

    if is_directed:
        for i in range(number_of_vertices - 1):
            result[i].append(random.shuffled_index[i])
    else:
        for i in range(number_of_vertices - 1):
            result[i].append(random.shuffled_index[i])
            if random.random() < 0.5:
                result[i][0], result[i][1] = result[i][1], result[i][0]

    return result


def generate_path_tree(number_of_vertices: int, n_indexed: int, is_directed: bool) -> list[list[int]]:
    random.shuffled_index = [(i + n_indexed) for i in range(number_of_vertices)]
    random.shuffle(random.shuffled_index)

    result: list[list[int]] = []

    if is_directed:
        for i in range(number_of_vertices - 1):
            result.append([random.shuffled_index[i], random.shuffled_index[i + 1]])
    else:
        for i in range(number_of_vertices - 1):
            if random.random() < 0.5:
                result.append([random.shuffled_index[i], random.shuffled_index[i + 1]])
            else:
                result.append([random.shuffled_index[i + 1], random.shuffled_index[i]])

    random.shuffle(result)
    return result


def generate_random_tree(number_of_vertices: int, n_indexed: int, is_directed: bool) -> list[list[int]]:
    random.shuffled_index = [(i + n_indexed) for i in range(number_of_vertices)]
    random.shuffle(random.shuffled_index)
    result: list[list[int]] = []

    if is_directed:
        for i in range(number_of_vertices - 1):
            result.append([random.shuffled_index[random.randint(0, i)], random.shuffled_index[i + 1]])
    else:
        for i in range(number_of_vertices - 1):
            if random.random() < 0.5:
                result.append([random.shuffled_index[random.randint(0, i)], random.shuffled_index[i + 1]])
            else:
                result.append([random.shuffled_index[i + 1], random.shuffled_index[random.randint(0, i)]])

    random.shuffle(result)
    return result


# undirected tree: 01110, 01111
#   directed tree: 11110, 11111
def generate_tree(number_of_vertices: int, n_indexed: int, is_directed: bool) -> list[list[int]]:
    r = random.random()
    if r < 0.7:
        return generate_random_tree(number_of_vertices, n_indexed, is_directed)
    elif r < 0.8:
        return generate_path_tree(number_of_vertices, n_indexed, is_directed)
    elif r < 0.9:
        return generate_star_tree(number_of_vertices, n_indexed, is_directed)
    else:
        return generate_binary_tree(number_of_vertices, n_indexed, is_directed)


def generate_graph_impl(variable_name: str, variables: dict[str, Variable],
                        is_generated: list[bool], generated_values: list[list]) -> bool:
    from modules.variable.generator import generate_value

    id = variables[variable_name].id

    number_of_vertices_evaluable_expr = ''

    for token in variables[variable_name].number_of_vertices_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the number of vertices in {colorize(Color.CODE, variable_name)}.')
                exit_failure()
            elif not generate_value(token, variables, is_generated, generated_values):
                return False

            if isinstance(variables[token], (Number, String)):
                number_of_vertices_evaluable_expr += f'({generated_values[variables[token].id][0]}) '
            else:
                number_of_vertices_evaluable_expr += f'({generated_values[variables[token].id]}) '
        else:
            number_of_vertices_evaluable_expr += f'{token} '

    number_of_vertices_v: int

    try:
        number_of_vertices_v = round(eval(number_of_vertices_evaluable_expr))
    except:
        error('Failed to evaluate the number of vertices in {} (= {}).'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, number_of_vertices_evaluable_expr)
        ))
        exit_failure()

    # is it a tree?
    if variables[variable_name].is_tree:
        generated_values[id] = generate_tree(number_of_vertices_v,
                                             variables[variable_name].n_indexed,
                                             variables[variable_name].is_directed)
        is_generated[id] = True
        return True

    number_of_edges_evaluable_expr = ''

    for token in variables[variable_name].number_of_edges_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the number of edges in {colorize(Color.CODE, variable_name)}.')
                exit_failure()
            elif not generate_value(token, variables, is_generated, generated_values):
                return False

            if isinstance(variables[token], (Number, String)):
                number_of_edges_evaluable_expr += f'({generated_values[variables[token].id][0]}) '
            else:
                number_of_edges_evaluable_expr += f'({generated_values[variables[token].id]}) '
        else:
            number_of_edges_evaluable_expr += f'{token} '

    number_of_edges_v: int

    try:
        number_of_edges_v = round(eval(number_of_edges_evaluable_expr))
    except:
        error('Failed to evaluate the number of edges in {} (= {}).'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, number_of_edges_evaluable_expr)
        ))
        exit_failure()

    mask = 0
    mask += (variables[variable_name].no_self_loop)
    mask += (variables[variable_name].no_multiple_edge << 1)
    mask += (variables[variable_name].is_acyclic << 2)
    mask += (variables[variable_name].is_connected << 3)

    # is it a tree? (again)
    if (number_of_edges_v == (number_of_vertices_v - 1)) and (mask == 0b1111):
        generated_values[id] = generate_tree(number_of_vertices_v,
                                             variables[variable_name].n_indexed,
                                             variables[variable_name].is_directed)
        is_generated[id] = True
        return True

    if variables[variable_name].is_directed:
        is_generated[id], generated_values[id] = [
            generate_graph_00000_10000,
            generate_graph_00001_10001,
            generate_graph_10010,
            generate_graph_10011,
            generate_graph_10100_10101,
            generate_graph_10100_10101,
            generate_graph_10110_10111,
            generate_graph_10110_10111,
            generate_graph_11000,
            generate_graph_11001,
            generate_graph_11010,
            generate_graph_11011,
            generate_graph_11100_11101,
            generate_graph_11100_11101,
        ][mask](number_of_vertices_v, number_of_edges_v, variables[variable_name].n_indexed)
    else:
        is_generated[id], generated_values[id] = [
            generate_graph_00000_10000,
            generate_graph_00001_10001,
            generate_graph_00010,
            generate_graph_00011,
            generate_graph_00100_00101_00110_00111,
            generate_graph_00100_00101_00110_00111,
            generate_graph_00100_00101_00110_00111,
            generate_graph_00100_00101_00110_00111,
            generate_graph_01000,
            generate_graph_01001,
            generate_graph_01010,
            generate_graph_01011,
            generate_graph_01100_01101,
            generate_graph_01100_01101
        ][mask](number_of_vertices_v, number_of_edges_v, variables[variable_name].n_indexed)

    return is_generated[id]


def generate_graph(variable_name: str, variables: dict[str, Variable],
                   is_generated: list[bool], generated_values: list[list]) -> bool:
    for _ in range(number_of_trial):
        if generate_graph_impl(variable_name, variables, is_generated, generated_values):
            return True

    return False

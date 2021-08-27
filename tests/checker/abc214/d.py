import queue


def main() -> None:
    N = int(input())
    adjacency_list = [[] for _ in range(N)]

    for _ in range(N - 1):
        u, v, w = map(int, input().split())

        assert 1 <= u <= N
        assert 1 <= v <= N
        assert 1 <= w <= 10**7

        u -= 1
        v -= 1

        adjacency_list[u].append(v)
        adjacency_list[v].append(u)

    q = queue.SimpleQueue()
    q.put((0, -1))

    visited = [False] * N

    while not q.empty():
        cur_node, prev_node = q.get()
        visited[cur_node] = True

        for next_node in adjacency_list[cur_node]:
            if next_node == prev_node:
                continue

            assert not visited[next_node]

            q.put((next_node, cur_node))

    assert all(visited)


if __name__ == '__main__':
    main()

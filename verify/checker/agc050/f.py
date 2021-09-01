import queue


def main() -> None:
    N = int(input())
    assert 2 <= N <= 100

    adjacency_list = [[] for _ in range(N)]

    for _ in range(N - 1):
        a, b = map(int, input().split())
        assert 1 <= a <= N
        assert 1 <= b <= N

        a -= 1
        b -= 1

        adjacency_list[a].append(b)
        adjacency_list[b].append(a)

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

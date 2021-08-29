import queue


def main() -> None:
    N, K = map(int, input().split())
    adjacency_list = [[] for _ in range(N)]
    assert 2 <= N <= 100
    assert 1 <= K <= N - 1

    for _ in range(N - 1):
        A, B = map(int, input().split())
        assert 1 <= A <= N
        assert 1 <= B <= N

        A -= 1
        B -= 1

        adjacency_list[A].append(B)
        adjacency_list[B].append(A)

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

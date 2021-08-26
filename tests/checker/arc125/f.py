import queue


def main() -> None:
    N = int(input())
    adjacency_list = [[] for _ in range(N)]

    assert 2 <= N <= 2*(10**5)

    for _ in range(N - 1):
        a, b = map(int, input().split())
        assert 1 <= a < b <= N

        a -= 1
        b -= 1
        adjacency_list[a].append(b)
        adjacency_list[b].append(a)

    Q = queue.SimpleQueue()
    Q.put((0, -1))

    visited = [False] * N

    while not Q.empty():
        cur_node, prev_node = Q.get()
        visited[cur_node] = True

        for next_node in adjacency_list[cur_node]:
            if next_node == prev_node:
                continue
            assert not visited[next_node]
            Q.put((next_node, cur_node))

    assert all(visited)


if __name__ == '__main__':
    main()

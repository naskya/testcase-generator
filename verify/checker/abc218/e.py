def main() -> None:
    N, M = map(int, input().split())
    adjacency_list = [[] for _ in range(N)]

    assert 2 <= N <= 100
    assert N - 1 <= M <= 100

    for _ in range(M):
        a, b, c = map(int, input().split())

        assert 1 <= a <= N
        assert 1 <= b <= N
        assert -10**9 <= c <= 10**9

        a -= 1
        b -= 1

        adjacency_list[a].append(b)
        adjacency_list[b].append(a)

    stk = [0]
    visited = [False] * N

    while stk:
        cur_node = stk.pop()
        visited[cur_node] = True

        for next_node in adjacency_list[cur_node]:
            if not visited[next_node]:
                stk.append(next_node)

    assert all(visited)


if __name__ == '__main__':
    main()

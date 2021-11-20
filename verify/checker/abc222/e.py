def main() -> None:
    N, M, K = map(int, input().split())
    A = list(map(int, input().split()))

    assert 2 <= N <= 1000
    assert 2 <= M <= 1000
    assert abs(K) <= 10**5
    assert len(A) == M

    graph = [[] for _ in range(N)]

    for _ in range(N - 1):
        u, v = map(int, input().split())
        assert 1 <= u <= N
        assert 1 <= v <= N

        u -= 1
        v -= 1

        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * N
    stk = [0]

    while stk:
        cur = stk.pop()
        visited[cur] = True

        for nxt in graph[cur]:
            if not visited[nxt]:
                stk.append(nxt)

    assert all(visited)


if __name__ == '__main__':
    main()

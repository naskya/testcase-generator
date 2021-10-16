def main() -> None:
    N = int(input())
    assert 2 <= N <= 2000

    graph = [[] for _ in range(N)]

    for _ in range(N - 1):
        u, v = map(int, input().split())
        assert 1 <= u < v <= N

        u -= 1
        v -= 1

        graph[u].append(v)
        graph[v].append(u)

    stk = [0]
    vis = [False] * N

    while stk:
        cur = stk.pop()
        vis[cur] = True

        for nxt in graph[cur]:
            if not vis[nxt]:
                stk.append(nxt)

    assert all(vis)


if __name__ == '__main__':
    main()

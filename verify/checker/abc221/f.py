def main() -> None:
    N = int(input())
    assert 2 <= N <= 100

    graph = [[] for _ in range(N)]

    for _ in range(N - 1):
        u, v = map(int, input().split())

        assert 1 <= u <= N
        assert 1 <= v <= N
        assert u != v

        u -= 1
        v -= 1

        graph[u].append(v)
        graph[v].append(u)

    stk = [0]
    vis = [False] * N

    while stk:
        cnode = stk.pop()
        vis[cnode] = True

        for nnode in graph[cnode]:
            if not vis[nnode]:
                stk.append(nnode)

    assert all(vis)


if __name__ == '__main__':
    main()

def main() -> None:
    N = int(input())
    assert 2 <= N <= 100

    tree = [[] for _ in range(N)]

    for _ in range(N - 1):
        u, v = map(int, input().split())
        assert 1 <= u < v <= N

        u -= 1
        v -= 1

        tree[u].append(v)
        tree[v].append(u)

    stk = [0]
    visited = [False] * N

    while stk:
        current = stk.pop()
        visited[current] = True

        for next in tree[current]:
            if not visited[next]:
                stk.append(next)

    assert all(visited)


if __name__ == '__main__':
    main()

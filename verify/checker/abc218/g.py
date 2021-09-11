def main() -> None:
    N = int(input())
    A = list(map(int, input().split()))

    assert 2 <= N <= 100
    assert len(A) == N
    assert all(2 <= A_i <= 10**9 for A_i in A)

    adjacency_list = [[] for _ in range(N)]

    for _ in range(N - 1):
        u, v = map(int, input().split())
        assert 1 <= u < v <= N

        u -= 1
        v -= 1

        adjacency_list[u].append(v)
        adjacency_list[v].append(u)

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

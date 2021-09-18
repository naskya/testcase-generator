def main() -> None:
    N, M, Q = map(int, input().split())
    assert 1 <= N <= 2*(10**5)
    assert 0 <= M <= min(100, N * (N - 1) // 2)
    assert 1 <= Q <= 100

    graph = []

    for _ in range(M):
        edge = tuple(map(int, input().split()))
        assert len(edge) == 2
        assert edge[0] != edge[1]
        assert 1 <= edge[0] <= N
        assert 1 <= edge[1] <= N
        assert not edge in graph

        graph.append(edge)

    x = list(map(int, input().split()))
    assert len(x) == Q
    assert all(1 <= x_i <= N for x_i in x)


if __name__ == '__main__':
    main()

def main() -> None:
    N, M = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(M)]

    assert 2 <= N <= 50
    assert 1 <= M <= N * (N - 1)
    assert all(len(edge) == 2 for edge in edges)
    assert all(1 <= edge[0] <= N and 1 <= edge[1] <= N for edge in edges)
    assert all(edge[0] != edge[1] for edge in edges)
    assert all(edges[i] != edges[j] for i in range(M) for j in range(i + 1, M))


if __name__ == '__main__':
    main()

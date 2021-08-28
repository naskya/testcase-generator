def main() -> None:
    N, M = map(int, input().split())
    graph = [(0, 0)] * M

    for i in range(M):
        graph[i] = tuple(map(int, input().split()))
        assert 1 <= graph[i][0] < graph[i][1] <= N

    assert 2 <= N <= 17
    assert 0 <= M <= N * (N - 1) // 2
    assert len(set(graph)) == M


if __name__ == '__main__':
    main()

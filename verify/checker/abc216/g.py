def main() -> None:
    N, M = map(int, input().split())
    assert 1 <= N <= 2*(10**5)
    assert 1 <= M <= min(100, N * (N-1) // 2)

    L = [0] * M
    R = [0] * M
    X = [0] * M

    for i in range(M):
        L[i], R[i], X[i] = map(int, input().split())
        assert 1 <= L[i] <= R[i] <= N
        assert 1 <= X[i] <= R[i] - L[i] + 1

    for i in range(M):
        for j in range(i + 1, M):
            assert (L[i] != L[j]) or (R[i] != R[j])


if __name__ == '__main__':
    main()

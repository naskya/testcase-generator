def main() -> None:
    N, M, K = map(int, input().split())

    A = [0] * M
    B = [0] * M

    for i in range(M):
        A[i], B[i] = map(int, input().split())

    X = list(map(int, input().split()))

    assert 2 <= N <= 50
    assert 1 <= M <= (N * (N - 1))
    assert 1 <= K <= 10
    assert len(X) == N
    assert all(1 <= A_i <= N for A_i in A)
    assert all(1 <= B_i <= N for B_i in B)
    assert all(A[i] != B[i] for i in range(M))
    assert all(1 <= X_i <= 100 for X_i in X)

    for i in range(M):
        for j in range(i + 1, M):
            assert (A[i] != A[j]) or (B[i] != B[j])


if __name__ == '__main__':
    main()

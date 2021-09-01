def main() -> None:
    N, L = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert N <= L <= 10**9
    assert len(A) == N
    assert len(B) == N
    assert 1 <= A[0]
    assert 1 <= B[0]
    assert A[-1] <= L
    assert B[-1] <= L

    for i in range(N - 1):
        assert A[i] < A[i + 1]
        assert B[i] < B[i + 1]


if __name__ == '__main__':
    main()

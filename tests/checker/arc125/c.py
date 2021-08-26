def main() -> None:
    N, K = map(int, input().split())
    A = list(map(int, input().split()))

    assert 1 <= K <= N <= 2*(10**5)
    assert len(A) == K
    assert 1 <= A[0]
    assert A[-1] <= N

    for i in range(1, K):
        assert A[i - 1] < A[i]


if __name__ == '__main__':
    main()

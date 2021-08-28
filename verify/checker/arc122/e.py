def main() -> None:
    N = int(input())
    A = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert len(A) == N
    assert 2 <= A[0]
    assert A[-1] <= 10**18

    for i in range(1, N):
        assert A[i - 1] < A[i]


if __name__ == '__main__':
    main()

def main() -> None:
    N = int(input())
    A = list(map(int, input().split()))

    assert 2 <= N <= 100
    assert len(A) == N
    assert 0 <= A[0]
    assert A[-1] <= 10**9
    assert all(A[i] < A[i + 1] for i in range(N - 1))
    assert all(A_i % 2 == 0 for A_i in A)


if __name__ == '__main__':
    main()

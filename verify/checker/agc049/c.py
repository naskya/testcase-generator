def main() -> None:
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert len(A) == N
    assert len(B) == N
    assert 1 <= A[0]
    assert A[-1] <= 10**9

    for i in range(N - 1):
        assert A[i] < A[i + 1]

    assert all(1 <= B_i <= 10**9 for B_i in B)


if __name__ == '__main__':
    main()

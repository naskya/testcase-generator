def main() -> None:
    N, X = map(int, input().split())
    A = list(map(int, input().split()))

    assert 2 <= N <= 100
    assert 1 <= X <= N
    assert len(A) == N
    assert all(1 <= A[i] <= N and A[i] != i for i in range(N))


if __name__ == '__main__':
    main()

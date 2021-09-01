def main() -> None:
    N, K = map(int, input().split())
    A = list(map(int, input().split()))

    assert 2 <= N <= 100
    assert 1 <= K <= 10**18
    assert len(A) == N
    assert all(1 <= A_i <= N for A_i in A)


if __name__ == '__main__':
    main()

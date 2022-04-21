def main() -> None:
    N, K, M = map(int, input().split())
    A = list(map(int, input().split()))

    assert 2 <= N <= 100
    assert 1 <= M <= K <= 100
    assert len(A) == N - 1
    assert all(0 <= A_i <= K for A_i in A)


if __name__ == '__main__':
    main()

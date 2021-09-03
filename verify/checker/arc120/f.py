def main() -> None:
    N, K, D = map(int, input().split())
    A = list(map(int, input().split()))

    assert D == 2
    assert 2 <= N <= 100
    assert 1 <= K <= (N + D - 1) // D
    assert len(A) == N
    assert all(1 <= A_i < 998244353 for A_i in A)


if __name__ == '__main__':
    main()

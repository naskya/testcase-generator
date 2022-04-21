def main() -> None:
    N, K = map(int, input().split())
    A = list(map(int, input().split()))
    assert 1 <= K <= N <= 100
    assert len(A) == N
    assert all(abs(A_i) <= 10**9 for A_i in A)


if __name__ == '__main__':
    main()

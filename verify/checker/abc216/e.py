def main() -> None:
    N, K = map(int, input().split())
    A = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert 1 <= K <= 2*(10**9)
    assert len(A) == N
    assert all(1 <= A_i <= 2*(10**9) for A_i in A)


if __name__ == '__main__':
    main()
